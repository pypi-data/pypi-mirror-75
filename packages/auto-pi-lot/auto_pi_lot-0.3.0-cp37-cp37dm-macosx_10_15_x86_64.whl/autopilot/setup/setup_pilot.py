"""
Run as a module as root.

Creates a :class:`npyscreen.SplitForm` to prompt the user in the command line
for parameters to set up a :class:`~.pilot.Pilot`'

Prompts user to create a run script or a systemd service.

Sets the following params:

* **NAME** - The name used by networking objects to address this Pilot
* **BASEDIR** - The base directory for autopilot files (/usr/autopilot)
* **PUSHPORT** - Router port used by the Terminal we connect to.
* **TERMINALIP** - IP Address of our upstream Terminal.
* **MSGPORT** - Port used by our own networking object
* **HARDWARE** - Any hardware and its mapping to GPIO pins. No pins are required to be set, instead each
  task defines which pins it needs. Currently the default configuration asks for

    * POKES - :class:`.hardware.Beambreak`
    * LEDS - :class:`.hardware.LED_RGB`
    * PORTS - :class:`.hardware.Solenoid`

* **AUDIOSERVER** - Which type, if any, audio server to use (`'jack'`, `'pyo'`, or `'none'`)
* **NCHANNELS** - Number of audio channels
* **FS** - Sampling rate of audio output
* **JACKDSTRING** - string used to start the jackd server, see `the jack manpages <https://linux.die.net/man/1/jackd>`_ eg::

    jackd -P75 -p16 -t2000 -dalsa -dhw:sndrpihifiberry -P -rfs -n3 -s &

* **PIGPIOMASK** - Binary mask of pins for pigpio to control, see `the pigpio docs <http://abyz.me.uk/rpi/pigpio/pigpiod.html>`_ , eg::

    1111110000111111111111110000

* **PULLUPS** - Pin (board) numbers to pull up on boot
* **PULLDOWNS** - Pin (board) numbers to pull down on boot.


"""

import argparse
import npyscreen as nps
from collections import OrderedDict as odict
import pprint
import json
import os
import subprocess
LOG_LEVELS= ("DEBUG", "INFO", "WARNING", "ERROR")
class PilotSetupForm(nps.Form):
    def create(self):
        self.input = odict({
            'NAME': self.add(nps.TitleText, name="Pilot Name:", value=""),
            'BASEDIR': self.add(nps.TitleText, name="Base Directory:", value="/usr/autopilot"),
            'LINEAGE': self.add(nps.TitleText, name="Are we a parent or a child?", value=""),
            'CONFIG': self.add(nps.TitleSelectOne,max_height=4,value=[0,], name="Configuration:",
                                   values=["AUDIO", "VISUAL", "NONE"], scroll_exit=True),
            'CHILDID': self.add(nps.TitleText, name="Child ID:", value=""),
            'PARENTID': self.add(nps.TitleText, name="Parent ID:", value=""),
            'PARENTIP': self.add(nps.TitleText, name="Parent IP:", value=""),
            'PARENTPORT': self.add(nps.TitleText, name="Parent Port:", value=""),
            'PUSHPORT': self.add(nps.TitleText, name="Push Port - Router port used by the Terminal:", value="5560"),
            'MSGPORT': self.add(nps.TitleText, name="Message Port - Our router port:", value="5565"),
            'TERMINALIP': self.add(nps.TitleText, name="Terminal IP:", value="192.168.0.100"),
            'AUDIOSERVER':self.add(nps.TitleSelectOne,max_height=4,value=[0,], name="Audio Server:",
                                   values=["jack", "pyo", "none"], scroll_exit=True),
            'NCHANNELS':self.add(nps.TitleText, name="N Audio Channels", value="1"),
            'OUTCHANNELS': self.add(nps.TitleText, name="List of output ports for jack audioserver to connect to", value="[1]"),
            'FS': self.add(nps.TitleText, name="Audio Sampling Rate", value="192000"),
            'JACKDSTRING': self.add(nps.TitleText, name="Command used to launch jackd - note that \'fs\' will be replaced with above FS",
                                    value="jackd -P75 -p16 -t2000 -dalsa -dhw:sndrpihifiberry -P -rfs -n3 -s &"),
            'PIGPIOMASK': self.add(nps.TitleText, name="Binary mask to enable pigpio to access pins according to the BCM numbering",
                                    value="1111110000111111111111110000"),
            'LOGLEVEL': self.add(nps.TitleSelectOne, max_height=5, value=[0, ], name="Log Level:",
                               values=LOG_LEVELS, scroll_exit=True),


        })
        #self.inName = self.add(nps.)


    # after we're done editing, close the input program
    def afterEditing(self):
        self.parentApp.setNextForm('HARDWARE')

class HardwareForm(nps.Form):
    def create(self):
        self.input = odict({
            'HARDWARE':{
                'POKES':{
                    'L':self.add(nps.TitleText, name="HARDWARE - POKES - L", value="24"),
                    'C': self.add(nps.TitleText, name="HARDWARE - POKES - C", value="8"),
                    'R': self.add(nps.TitleText, name="HARDWARE - POKES - R", value="10"),
                },
                'LEDS': {
                    'L': self.add(nps.TitleText, name="HARDWARE - LEDS - L", value="[11, 13, 15]"),
                    'C': self.add(nps.TitleText, name="HARDWARE - LEDS - C", value="[22, 18, 16]"),
                    'R': self.add(nps.TitleText, name="HARDWARE - LEDS - R", value="[19, 21, 23]"),
                },
                'PORTS': {
                    'L': self.add(nps.TitleText, name="HARDWARE - PORTS - L", value="31"),
                    'C': self.add(nps.TitleText, name="HARDWARE - PORTS - C", value="33"),
                    'R': self.add(nps.TitleText, name="HARDWARE - PORTS - R", value="37"),
                },
                'FLAGS': {
                    'L': self.add(nps.TitleText, name="HARDWARE - FLAGS - L", value=""),
                    'R': self.add(nps.TitleText, name="HARDWARE - FLAGS - R", value="")
                }},
            'PULLUPS': self.add(nps.TitleText, name="Pins to pull up on boot",
                                value="[7]"),
            'PULLDOWNS': self.add(nps.TitleText, name="Pins to pull down on boot",
                                  value="[]")
        })
        #self.inName = self.add(nps.)


    # after we're done editing, close the input program
    def afterEditing(self):
        self.parentApp.setNextForm(None)

class SetupApp(nps.NPSAppManaged):
    def onStart(self):
        self.form = self.addForm('MAIN', PilotSetupForm, name='Setup Pilot')
        self.hardware = self.addForm('HARDWARE', HardwareForm, name='Setup Pilot Hardware')


def unfold_values(v):
    """
    Unfold nested values from the SetupForm. Called recursively.

    Args:
        v (dict): unfolded values
    """
    if isinstance(v, dict):
        # recurse
        v = {k: unfold_values(v) for k, v in v.items()}
    else:
        try:
            v = int(v.value)
        except:
            v = v.value
    return v


def make_dir(adir):
    """
    Make a directory if it doesn't exist and set its permissions to `0777`

    Args:
        adir (str): Path to the directory
    """
    if not os.path.exists(adir):
        os.makedirs(adir)
        os.chmod(adir, 0o777)

if __name__ == "__main__":
    # Check for sudo
    if os.getuid() != 0:
        raise Exception("Need to run as root")

    # TODO: Load existing prefs
    #
    # # parse args
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--pfile', help="path to prefs.json to pre-populate fields. default looks for /usr/autopilot/prefs.json")
    # args = parser.parse_args()
    #
    # pfile = None
    # if args.pfile:
    #     pfile = str(args.pfile)
    #     print('using passed prefs file {}'.format(pfile))
    # elif os.path.exists('/usr/autopilot/prefs.json'):
    #     print('found existing prefs file at default location "/usr/autopilot/prefs.json"')
    #     usepfile = raw_input("\nUse found prefs (y) or start with defaults (n)? > ")
    #     if usepfile == "y":
    #         print('Using found prefs')
    #         pfile = '/usr/autopilot/prefs.json'
    #     else:
    #         print('Starting with default prefs')






    setup = SetupApp()
    setup.run()

    # extract params
    params = {k:unfold_values(v) for k, v in setup.form.input.items()}
    hardware_params = {k:unfold_values(v) for k, v in setup.hardware.input.items()}

    # combine
    params.update(hardware_params)

    ############################
    # some inelegant manual formatting

    # we are known as a pilot
    params['AGENT'] = "pilot"

    # convert numerical audio server index to string
    params['AUDIOSERVER'] = ['jack', 'pyo', 'none'][params['AUDIOSERVER'][0]]
    params['CONFIG'] = ['AUDIO', 'VISUAL', 'NONE'][params['CONFIG'][0]]
    params['LOGLEVEL'] = LOG_LEVELS[params['LOGLEVEL'][0]]



    # convert string LED pin specifier to list
    for k, v in params['HARDWARE']['LEDS'].items():
        params['HARDWARE']['LEDS'][k] = json.loads(v)

    # replace fs in jackd string
    params['JACKDSTRING'] = params['JACKDSTRING'].replace('fs', str(params['FS']))

    # pigpio should be a string
    params['PIGPIOMASK'] = str(params['PIGPIOMASK'])

    # make the string a dict
    # print(params['PULLHARDWARE'])
    params['PULLUPS'] = json.loads(params['PULLUPS'])
    params['PULLDOWNS'] = json.loads(params['PULLDOWNS'])

    # make outputs a list
    params['OUTCHANNELS'] = json.loads(params['OUTCHANNELS'])


    ##############################
    # Compute derived values
    pigpio_string = '-t 0 -l -x {}'.format(params['PIGPIOMASK'])
    params['PIGPIO_STRING'] = pigpio_string

    # define and make directory structure
    params['DATADIR'] = os.path.join(params['BASEDIR'], 'data')
    params['SOUNDDIR'] = os.path.join(params['BASEDIR'], 'sounds')
    params['LOGDIR'] = os.path.join(params['BASEDIR'], 'logs')

    for adir in [params['BASEDIR'], params['DATADIR'], params['SOUNDDIR'], params['LOGDIR']]:
        make_dir(adir)

    # Get repo dir
    file_loc = os.path.realpath(__file__)
    file_loc = file_loc.split(os.sep)[:-2]
    params['REPODIR'] = os.path.join(os.sep, *file_loc)

    # save prefs
    prefs_file = os.path.join(params['BASEDIR'], 'prefs.json')
    with open(prefs_file, 'w') as prefs_file_open:
        json.dump(params, prefs_file_open, indent=4, separators=(',', ': '), sort_keys=True)
    os.chmod(prefs_file, 0o775)

    print('params saved to {}\n'.format(prefs_file))

    ###############################
    # Install -  create runfile and optionally make service

    launch_file = os.path.join(params['BASEDIR'], 'launch_pilot.sh')
    if params['CONFIG'] == 'AUDIO':
        with open(launch_file, 'w') as launch_file_open:
            launch_file_open.write('#!/bin/sh\n')
            launch_file_open.write('killall jackd\n')  # Try to kill any existing jackd processes
            launch_file_open.write('sudo killall pigpiod\n')
            launch_file_open.write('sudo mount -o remount,size=128M /dev/shm\n') # refresh shared memory
            #launch_file_open.write('sudo ' + pigpio_string + '\n')
            #launch_file_open.write(params['JACKDSTRING'] + '\n')  # Then launch ours
            #launch_file_open.write('sleep 2\n')  # We wait a damn second to let jackd start up
            launch_string = "python -m autopilot.core.pilot -f " + prefs_file
            launch_file_open.write(launch_string)

    elif params['CONFIG'] == 'VISUAL':
        with open(launch_file, 'w') as launch_file_open:
            launch_file_open.write('#!/bin/sh\n')
            launch_file_open.write('sudo killall python\n')  # Try to kill any existing jackd processes
            launch_file_open.write('sudo killall pigpiod\n')
            launch_file_open.write('sudo mount -o remount,size=128M /dev/shm\n') # refresh shared memory
            #launch_file_open.write('sudo ' + pigpio_string + '\n')
            #launch_file_open.write('sleep 2\n')  # We wait a damn second to let jackd start up
            launch_string = "python -m autopilot.core.pilot -f " + prefs_file
            launch_file_open.write(launch_string)

    else:
        with open(launch_file, 'w') as launch_file_open:
            launch_file_open.write('#!/bin/sh\n')
            launch_file_open.write('sudo killall python\n')  # Try to kill any existing jackd processes
            launch_file_open.write('sudo killall pigpiod\n')
            launch_file_open.write('sudo mount -o remount,size=128M /dev/shm\n')  # refresh shared memory
            #launch_file_open.write('sudo ' + pigpio_string + '\n')
            launch_string = "python -m autopilot.core.pilot -f " + prefs_file
            launch_file_open.write(launch_string)


    os.chmod(launch_file, 0o775)

    print('executable file created:\n     {}\n'.format(launch_file))

    answer = str(input('Install as Systemd service? (y/n)> '))

    if answer == 'y':
        # open pilot on startup using systemd
        systemd_string = '''[Unit]
Description=autopilot
After=multi-user.target

[Service]
Type=idle
ExecStart={launch_pi}

Restart=on-failure

[Install]
WantedBy=multi-user.target'''.format(launch_pi=launch_file)

        unit_loc = '/lib/systemd/system/autopilot.service'
        with open(unit_loc, 'w') as autopilot_service:
            autopilot_service.write(systemd_string)

        # enable the service
        subprocess.call(['sudo', 'systemctl', 'daemon-reload'])
        subprocess.call(['sudo', 'systemctl', 'enable', 'autopilot.service'])
        print('\nautopilot service installed and enabled, unit file located at:\n     {}\n'.format(unit_loc))


    disable_services = {'hciuart': ""}

    pp = pprint.PrettyPrinter(indent=4)
    print('Pilot set up with prefs:\r')
    pp.pprint(params)

