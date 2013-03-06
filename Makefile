PROJECTS_DIRECTORY := ..
CV_DIRECTORY := $(PROJECTS_DIRECTORY)/cv
EZCC_DIRECTORY := $(PROJECTS_DIRECTORY)/easyc
EZCC := $(EZCC_DIRECTORY)/ezcc.ez -d -I $(CV_DIRECTORY)
EZCC_GPROF := $(EZCC_DIRECTORY)/ezcc.ez -p -O -I $(CV_DIRECTORY)
ARM_ROOT :=      /home/wayne/download/eldk/arm
ARM_BIN :=       $(ARM_ROOT)/bin
ARM_LIB := 	 $(ARM_ROOT)/lib

#ARM_GDB :=       $(ARM_BIN)/gdb
#ARM_LIBEXPAT :=  $(ARM_LIB)/libexpat.so
#ARM_GDBTUI :=    $(ARM_BIN)/gdbtui
#ARM_GDBSERVER := $(ARM_BIN)/gdbserver
#ARM_CC :=        $(ARM_ROOT)/usr/bin/arm-linux-gnueabi-gcc

ARM_GDB :=       /home/wayne/download/eldk/arm/usr/bin/gdb
ARM_LIBEXPAT :=  /home/wayne/download/eldk/arm/usr/lib/libexpat.so
ARM_GDBTUI :=    /home/wayne/download/eldk/arm/usr/bin/gdbtui
ARM_GDBSERVER := /home/wayne/download/eldk/arm/usr/bin/gdbserver
ARM_CC := /home/wayne/download/eldk/usr/bin/arm-linux-gnueabi-gcc

#ARM_CC := /home/wayne/download/eldk/usr/arm-linux/bin/gcc
#ARM_CC := $(ICONNECT_TOOLS)gcc
EZCC_ARM := $(EZCC) -C "$(ARM_CC)"
CC := gcc

ARM_OPENCV_ROOT := /home/wayne/download/opencv/arm-O3-shared-V4L
ARM_OPENCV_LIB := $(ARM_OPENCV_ROOT)/lib
ARM_OPENCV_LIBS :=	\
    libcvaux.so		\
    libcvaux.so.2.1	\
    libcvaux.so.2.1.0	\
    libcv.so		\
    libcv.so.2.1	\
    libcv.so.2.1.0	\
    libcxcore.so	\
    libcxcore.so.2.1	\
    libcxcore.so.2.1.0	\
    libml.so		\
    libml.so.2.1	\
    libml.so.2.1.0

foo :=			\
    libhighgui.so	\
    libhighgui.so.2.1	\
    libhighgui.so.2.1.0	\

#ARM_V4L_ROOT := /home/wayne/download/libv4l/libv4l-0.6.4
#ARM_LIBV4L2_LIB := $(ARM_V4L_ROOT)/libv4l2
#ARM_LIBV4L2_LIBS := 	\
#    v4l2convert.so	\
#    libv4l2.so		\
#    v4l2convert.so.0	\
#   libv4l2.so.0
#ARM_LIBV4L1_LIB := $(ARM_V4L_ROOT)/libv4l1
#ARM_LIBV4L1_LIBS :=	\
#    v4l1compat.so.0	\
#    libv4l1.so		\
#    libv4l1.so.0	\
#    v4l1compat.so
#ARM_LIBV4LCONVERT_LIB := $(ARM_V4L_ROOT)/libv4lconvert
#ARM_LIBV4LCONVERT_LIBS := \
#    libv4lconvert.so.0	\
#    libv4lconvert.so

CC := g++
LIBS := -lm -lcv -lhighgui
INCLUDES := \
    -I/usr/include/opencv

# Lists:
PROGRAMS :=		\
    ttyshare		\
    femtocom		\
    Brain		\
    Host_Control	\
    Hello		\
    Hello_arm		\
    Image_Extract	\
    Tags		\
    video		\
    Video_Extract	\
    ${ARM_PROGRAMS}

ARM_PROGRAMS :=		\
    Brain_arm		\
    Image_Extract_arm	\
    Video_Extract_arm	\
    gdb_arm		\
    openocd_arm		\
    femtocom_arm	\
    ttyshare_arm	\
    video_arm


# House keeping:
.PHONY: all clean

all: ${PROGRAMS}

clean:
	rm -f ${PROGRAMS}
	rm -f femtocom.c~ ttyshare.c~ hello.ezc~
	rm -f Hello.c Hello.ezc~ Hello.h Hello.o
	rm -f CV.c CV.h CV.o
	rm -f CV.ezg CV_C.o
	rm -f Easy_C.c Easy_C.h Easy_C.o Easy_C.ezg
	rm -f Easy_C_C.o
	rm -f Extractor.c Extractor.ezg Extractor.h Extractor.o
	rm -f Extractor.ezc~
	rm -f Image_Extract.c Image_Extract.ezg Image_Extract.h Image_Extract.o
	rm -f Image_Extract.ezc~
	rm -f FEC.o FEC.h FEC.c
	rm -f FEC_C.o
	rm -f High_GUI.c High_GUI.ezg High_GUI.h High_GUI.o
	rm -f High_GUI_C.o
	rm -f Math.c Math.h Math.o
	rm -f Makefile~
	rm -f Tags.c Tags.ezg Tags.h Tags.o
	rm -f Tags_gprof
	rm -f Tags.ezc~
	rm -f Unix.c Unix_C.o Unix.ezg Unix.h Unix.o
	rm -f V4L2.c V4L2.h V4L2.o V4L2.ezg V4L2.ezc~
	rm -f V4L2_C.o V4L2_C.c~ V4L2_C.h~
	rm -f video.c~
	rm -f Video_Extract.c Video_Extract.h Video_Extract.o
	rm -f Video_Extract.ezc~
	rm -f arm.tar.gz
	rm -rf temporary
	rm -f foo.tga
	rm -f gmon.out
	rm -f iConnect.tar


# PROGRAM build targets:
ttyshare: ttyshare.c
	gcc -o $@ ttyshare.c

ttyshare_arm: ttyshare.c
	$(ARM_CC) -o $@ ttyshare.c

femtocom: femtocom.c
	gcc -o $@ femtocom.c

femtocom_arm: femtocom.c
	$(ARM_CC) -o $@ femtocom.c

openocd_arm: ../openocd/cross_compile/output/bin/openocd
	cp ../openocd/cross_compile/output/bin/openocd $@

tcl.tar:
	echo Making $@
	cd ../openocd/openocd-0.5.0/; tar cvf /tmp/tcl.tar tcl
	mv /tmp/tcl.tar $@

Brain: Brain.ezc Extractor.ezc Map.ezc
	$(EZCC) -o $@ Brain

Brain_arm: Brain
	$(EZCC_ARM) -o $@ -d Brain

Hello: Hello.ezc
	$(EZCC) -o $@ Hello

Hello_arm: Hello
	$(EZCC_ARM) -o $@ Hello

Host_Control: Host_Control.ezc Map.ezc
	$(EZCC) -o $@ -d Host_Control

Video_Extract: Video_Extract.ezc V4L2.ezc V4L2_C.c V4L2_C.h \
   Extractor.ezc Map.ezc
	$(EZCC) -o $@ -d Video_Extract

Video_Extract_arm: Video_Extract
	$(EZCC_ARM) -o $@ -d Video_Extract

Image_Extract: Image_Extract.ezc FEC.ezc FEC_C.h FEC_C.c Extractor.ezc
	$(EZCC) Image_Extract

Image_Extract_arm: Image_Extract
	$(EZCC_ARM) -o $@ Image_Extract

Tags: Tags.ezc FEC.ezc FEC_C.h FEC_C.c Extractor.ezc Map.ezc
	$(EZCC) Tags

.PHONY: arm_libs

arm_libs: ${ARM_OPENCV_LIBS:%=$(ARM_OPENCV_LIB)/%}
	rm -f ${ARM_OPENCV_LIBS}
	(cd ${ARM_OPENCV_LIB} ; tar cf - ${ARM_OPENCV_LIBS}) | tar xvf -


gdb_arm: $(ARM_GDB)
	cp $(ARM_GDB) $@

libexpat.so.0: $(ARM_LIBEXPAT)
	cp $(ARM_LIBEXPAT) $@

iConnect.tar: ${ARM_PROGRAMS} tcl.tar arm_libs robot.sh Host_Control.ezc \
    Video_Extract.ezc Brain.ezc femtocom.c ttyshare.c gdb_arm libexpat.so.0
	tar cvf $@ ${ARM_OPENCV_LIBS} ${ARM_PROGRAMS} tcl.tar robot.sh \
	    gdb_arm libexpat.so.0

OCVGPL := /home/wayne/download/opencv/intel-gprof/lib
OCVG3PL := /home/wayne/download/opencv/intel-gprof/3rdparty/lib
Tags_gprof: Tags.ezc FEC.ezc FEC_C.h FEC_C.c Extractor.ezc
	@echo Supressing 1st compile output:
	$(EZCC_GPROF) -c Tags > /dev/null 2>&1 > /dev/null
	gcc -c -o /tmp/Tags.o -I $(CV_DIRECTORY) /tmp/Tags.c
	g++ -O2 -o $@ -pg \
	    /tmp/Tags.o 			\
	    Tags.o				\
	    Easy_C.o 				\
	    CV.o				\
	    Math.o				\
	    High_GUI.o				\
	    Extractor.o				\
	    FEC.o				\
	    CV_C.o				\
	    Easy_C_C.o 				\
	    FEC_C.o				\
	    High_GUI_C.o 			\
	    -Bstatic 				\
	    $(OCVGPL)/libhighgui.a		\
	    $(OCVGPL)/libcv.a			\
	    $(OCVGPL)/libcxcore.a 		\
	    $(OCVGPL)/libml.a 			\
	    $(OCVGPL)/libcvaux.a  		\
	    $(OCVG3PL)/libopencv_lapack.a	\
	    -Bdynamic 				\
	    -pthread -lz -lrt -lm

video: video.c
	$(CC) -o $@ video.c

video_arm: video.c
	$(ARM_CC) -o $@ video.c

arm.tar.gz:
	rm -rf temp
	mkdir temp
	rm -f /tmp/arm_opencv_libs.tar
	cd temp; (cd $(ARM_OPENCV_LIB) ; tar cf - ${ARM_OPENCV_LIBS} ) | tar xvf -
	cp Image_Extract_arm temp
	cp test8n.tga test8s.tga test8e.tga test8w.tga temp
	cd temp; tar cvf ../arm.tar *
	gzip --best arm.tar
	rm -rf temp