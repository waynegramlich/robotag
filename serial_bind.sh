#!/bin/sh
serial0=$( udevadm info -a -p /class/tty/ttyUSB0 2>&1 | \
  grep ATTRS{serial} | head -n 1 | sed 's,^.*=="',,g | sed 's,",,g' )
serial1=$( udevadm info -a -p /class/tty/ttyUSB1 2>&1 | \
  grep ATTRS{serial} | head -n 1 | sed 's,^.*=="',,g | sed 's,",,g' )
serial2=$( udevadm info -a -p /class/tty/ttyUSB2 2>&1 | \
  grep ATTRS{serial} | head -n 1 | sed 's,^.*=="',,g | sed 's,",,g' )
echo serial0=$serial0
echo serial1=$serial1
echo serial2=$serial2
#serial_number="A800I7X0"
#serial_number="FTEZYGNB"
serial_number="A800I4BP"
#echo sn=$serial_number
if [ "$serial0" = "$serial_number" ] ;
   then	sudo rm -f /dev/flyswatter /dev/ftdi_serial
	echo /dev/ftdi_serial "=>" /dev/ttuUSB0
	sudo ln -s /dev/ttyUSB0 /dev/ftdi_serial
	echo /dev/flyswatter "=>" /dev/ttyUSB1
	sudo ln -s /dev/ttyUSB1 /dev/flyswatter
elif [ "$serial2" = "$serial_number" ]
   then sudo rm -f /dev/flyswatter /dev/ftdi_serial
	echo /dev/flyswatter "=>" /dev/ttyUSB0
	sudo ln -s /dev/ttyUSB0 /dev/flyswatter
	echo /dev/ftdi_serial "=>" /dev/ttyUSB2
	sudo ln -s /dev/ttyUSB2 /dev/ftdi_serial
   else echo "Something is wrong"
	echo serial0 = $serial0
	echo serial1 = $serial1
	echo serial2 = $serial2
   fi




