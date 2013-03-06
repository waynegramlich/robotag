The robotag software is based on some code that was originally written
by Michael Thompson for recognizing fiducials.  The following files are
present:

In operation, there are up to 4 processes running:

  gui.py:	Graphical control/mapping program
     ^
     |
     v
  Host_Control.ezc:	Command line host control program
     ^			Also provides a server to fetch files from
     |    Host laptop/desktop
  ----------------------------------------
     |    Robot linux boxen
     v
  Brain.ezc:	Main path planning and robot control process
     ^
     |
     v
  Video_Extract.ezc:  Connected to camera and does fiducial recognition
     
In addition, Brain.ezc has a serial connection that connects to the
embedded ARM processor on the robot.

Additional files are:

  Map.ezc:
	The code that manages the map data structures.
	This code can read/write tags.xml.  This code is
	present in all three processes (except gui.py).

  Extractor.ezc:
	The code that extracts information from fidicuials
	in camera images.

  FEC.ezc:
	Performs forward error correction code processing.

  V4L2.ezc:
	Performs video support services.

  OpenCV.ezc:
	Provides interface with OpenCV.  Used in Extractor and V4L2.

Lastly, there is Tags.ezc which is used to generate tags,
and do testing.

---------------

In order to run everything do the following:

  1)	Type "make" to get everything built.

  2)	Type "make iConnect.tar" to get all the code compiled for ARM.

  3)	Type "Host_Control" to get the host control program running.

  4)	In another window/tab, type "gui.py" to get the GUI running.
	It will crash if Host_Control is not running.

  5)	Power up robot.

  6)	Remotely log into robot as root via:

		prompt> ssh root@192.168.1.52
		Passward: {usual system password}

  7)	Run /etc/robot.sh to connect to Host_Control, upload software,
	get fire off robot processes, and connect to camera and Robus.

  8)	Use either Host_Control or gui.py to control robot.

----------------

The code can debugged locally with a UVC web cam is plugged in and
a serial cable is plugged in.  Fire up Brain as follows:

       prompt> Brain /dev/video1 /dev/ttyUSB0

where the two arguments specify the correct video camera and
serial port connection.

