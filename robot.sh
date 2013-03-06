#!/bin/sh

# Make sure we have a video node:
if [ ! -c /dev/video0 ] ; 			\
   then	rm -f /dev/video0 ;			\
	/bin/mknod /dev/video0 c 81 0 ;	\
   fi

# Fetch everything:
(cd /tmp ; nc 192.168.1.5 4321 | tar xf - )

(cd /tmp ; rm -f Video_Extract ; ln -s Video_Extract_arm Video_Extract)

(cd /tmp ; /tmp/Brain_arm )


