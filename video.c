#include <math.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include <fcntl.h>
#include <getopt.h>             /* getopt_long() */
#include <unistd.h>
#include <errno.h>
#include <malloc.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/mman.h>
#include <sys/ioctl.h>

#include <linux/videodev2.h>

#define CLEAR(x) memset(&(x), 0, sizeof(x))

typedef enum {
	IO_METHOD_READ,
	IO_METHOD_MMAP,
	IO_METHOD_USERPTR,
} io_method;

struct buffer {
        void *                  start;
        size_t                  length;
};

static const char *     dev_name        = NULL;
static io_method	io		= IO_METHOD_MMAP;
static int              fd              = -1;
struct buffer *         buffers         = NULL;
static unsigned int     n_buffers       = 0;

static int format_ids[] = {
  V4L2_PIX_FMT_SBGGR8,
  //V4L2_PIX_FMT_SBGGR16,
  V4L2_PIX_FMT_RGB332,
  V4L2_PIX_FMT_RGB444,
  V4L2_PIX_FMT_RGB555,
  V4L2_PIX_FMT_RGB565,
  V4L2_PIX_FMT_RGB555X,
  V4L2_PIX_FMT_RGB565X,
  V4L2_PIX_FMT_BGR24,
  V4L2_PIX_FMT_RGB24,
  V4L2_PIX_FMT_BGR32,
  V4L2_PIX_FMT_YUV444,
  V4L2_PIX_FMT_YUV555,
  V4L2_PIX_FMT_YUV565,
  V4L2_PIX_FMT_YUV32,
  //V4L2_PIX_FMT_Y16,
  V4L2_PIX_FMT_YUYV,
  V4L2_PIX_FMT_Y41P,
  V4L2_PIX_FMT_YVU420,
  V4L2_PIX_FMT_YUV420,
  V4L2_PIX_FMT_YVU410,
  V4L2_PIX_FMT_YUV410,
  V4L2_PIX_FMT_YUV422P,
  V4L2_PIX_FMT_YUV411P,
  V4L2_PIX_FMT_NV12,
  V4L2_PIX_FMT_NV21,
  V4L2_PIX_FMT_JPEG,
  V4L2_PIX_FMT_MPEG,
  -1,
};

static void
errno_exit(const char *s)
{
    (void)fprintf(stderr, "%s error %d, %s\n", s, errno, strerror(errno));
    exit(EXIT_FAILURE);
}

static int
xioctl(int fd, int request, void *arg)
{
    int r;

    do {
	r = ioctl(fd, request, arg);
    } while (-1 == r && EINTR == errno);

    return r;
}

static void
byte_write(FILE* fp, unsigned char byte)
// Write byte to fp as one byte.
{
	(void)fputc(byte, fp);
}

static void
short_write(FILE* fp, short value)
// Write value to fp as two little endian bytes.
{
	byte_write(fp, (unsigned char)(value & 0xff));		// Low byte
	byte_write(fp, (unsigned char)((value >> 8) & 0xff));	// High byte
}

void
write_tga(
  const char *base_name,
  unsigned int width,
  unsigned int height,
  unsigned int image_type,	/* 2=>color; 3=>b&w */
  unsigned int bpp,		/* Bits per Pixel */
  unsigned char *buffer)
{
    char file_name[2000];
    unsigned int buffer_size;
    FILE *tga_file;

    /* Append suffix to {base_name}: */
    (void)sprintf(file_name, "%s.tga", base_name);

    /* Open {base_name}.tga file for writing: */
    tga_file = fopen(file_name, "wb");
    if (tga_file == (FILE *)0) {
	(void)fprintf(stderr,
	  "Could not open '%s' for writing.\n", file_name);
	exit(EXIT_FAILURE);
    }

    /* Write .tga header :*/
    byte_write(tga_file, 0);		/* identsize */
    byte_write(tga_file, 0);		/* colourmaptype */
    byte_write(tga_file, image_type);	/* imagetype (3=>raw b&w) */
    short_write(tga_file, 0);		/* colourmapstart */
    short_write(tga_file, 0);		/* colourmaplength */
    byte_write(tga_file, 0);		/* colourmapbits */
    short_write(tga_file, 0);		/* xstart */
    short_write(tga_file, 0);		/* ystart */
    short_write(tga_file, width);	/* width */
    short_write(tga_file, height);	/* height */
    byte_write(tga_file, bpp);		/* bits per pixel*/
    byte_write(tga_file, 0);		/* descriptor */

    /* Write out the .tga file data: */
    buffer_size = height * width * (bpp>>3);
    if (fwrite(buffer, 1, buffer_size, tga_file) != buffer_size) {
	(void)fprintf(stderr, "Error writing '%s'\n", file_name);
	exit(EXIT_FAILURE);
    }

    /* Close the .tga file: */
    if (fclose(tga_file) != 0) {
	(void)fprintf(stderr, "Could not close '%s'\n", file_name);
	exit(EXIT_FAILURE);
    }
}


static int
crunch(
  unsigned int width,
  unsigned int height,
  unsigned char *cameraBuffer,
  void *tracker)
{
    (void)fprintf(stderr, ".");
    return 0;
}

static void
convert_yuv_to_rgb_pixel(
  int y,
  int u,
  int v,
  unsigned char *ra,
  unsigned char *ga,
  unsigned char *ba)
{
    int r, g, b;
    int c, d, e;

    c = y - 16;
    d = u - 128;
    e = v - 128;

    /* These formulas came from:
     *   http://msdn.microsoft.com/en-us/library/ms893078
     */

    r = (298 * c           + 409 * e + 128) >> 8;
    g = (298 * c - 100 * d + 208 * e + 128) >> 8;
    b = (298 * c + 516 * d           + 128) >> 8;

    if (r > 255) {
	r = 255;
    } else if (r < 0) {
	r = 0;
    }
    if (g > 255) {
	g = 255;
    } else if (g < 0) {
	g = 0;
    }
    if (b > 255) {
	b = 255;
    } else if (b < 0) {
	b = 0;
    }

    *ra = (unsigned char)r;
    *ga = (unsigned char)g;
    *ba = (unsigned char)b;
}

static void
convert_yuv_to_rgb_buffer(
  unsigned char *yuv,
  unsigned char *rgb,
  unsigned int width,
  unsigned int height)
{
    unsigned char y0, u, y1, v;
    unsigned char r, g, b;
    unsigned char *yuv_pointer;
    unsigned char *rgb_pointer;
    unsigned row;
    unsigned column;
    unsigned int yuv_row_span;
    unsigned int rgb_row_span;

    /* This code both converts the YUYU image to a RGB image: */
    yuv_row_span = width * 2;
    rgb_row_span = width * 3;
    for (row = 0; row < height; row++) {
	yuv_pointer = &yuv[row * yuv_row_span];
	rgb_pointer = &rgb[row * rgb_row_span];

	/* Now process two pixels at a time: */
	for (column = 0; column < width; column += 2) {
	    /* Grab Y0, U, Y1, and V values: */
	    y0 = *yuv_pointer++;
	    u = *yuv_pointer++;
	    y1 = *yuv_pointer++;
	    v = *yuv_pointer++;

	    /* Convert and store first pixel: */
	    convert_yuv_to_rgb_pixel(y0, u, v, &r, &g, &b);
	    *rgb_pointer++ = b;
	    *rgb_pointer++ = g;
	    *rgb_pointer++ = r;

	    /* Convert and store second pixel: */
	    convert_yuv_to_rgb_pixel(y1, u, v, &r, &g, &b);
	    *rgb_pointer++ = b;
	    *rgb_pointer++ = g;
	    *rgb_pointer++ = r;
	}
    }
}

static void
convert_yuv_to_grey_buffer(
  unsigned char *yuv,
  unsigned char *grey,
  unsigned int width,
  unsigned int height)
{
    unsigned char y0, y1;
    unsigned char *yuv_pointer;
    unsigned char *grey_pointer;
    unsigned row;
    unsigned column;
    unsigned int yuv_row_span;
    unsigned int grey_row_span;

    /* This code both converts the YUYU image to a Grey image: */
    yuv_row_span = width * 2;
    grey_row_span = width * 1;
    for (row = 0; row < height; row++) {
	yuv_pointer = &yuv[row * yuv_row_span];
	grey_pointer = &grey[row * grey_row_span];

	/* Now process two pixels at a time: */
	for (column = 0; column < width; column += 2) {
	    /* Grab Y0, U, Y1, and V values: */
	    y0 = *yuv_pointer++;
	    yuv_pointer++;	/* u */
	    y1 = *yuv_pointer++;
	    yuv_pointer++;	/* v */
	    *grey_pointer++ = y0;
	    *grey_pointer++ = y1;
	}
    }
}


static void
process_image(
  struct buffer *buf,
  unsigned int width,
  unsigned int height,
  void *tracker)
{
    unsigned int grey_size;
    unsigned char *grey;
    unsigned int rgb_size;
    unsigned char *rgb;

    /* Allocate {grey} buffer: */
    grey_size = height * width * 1;
    grey = (unsigned char *)malloc(grey_size);
    if (grey == (unsigned char *)0) {
	(void)fprintf(stderr, "Malloc error\n");
	exit(EXIT_FAILURE);
    }

    /* Allocate {grey} buffer: */
    rgb_size = height * width * 3;
    rgb = (unsigned char *)malloc(rgb_size);
    if (rgb == (unsigned char *)0) {
	(void)fprintf(stderr, "Malloc error\n");
	exit(EXIT_FAILURE);
    }

    /* Perform the conversion: */
    convert_yuv_to_grey_buffer((unsigned char *)buf->start,
      grey, width, height);
    convert_yuv_to_rgb_buffer((unsigned char *)buf->start,
      rgb, width, height);

    /* Write out the .tga file: */
    write_tga("rgb", width, height, 2, 24, rgb);
    write_tga("grey", width, height, 3, 8, grey);

    crunch(width, height, grey, tracker);

    /* Release buffer: */
    free(grey);
}

static const char *
format_to_string(
  int format_id)
{
    const char *result = "unknown format";

    switch (format_id) {
      case V4L2_PIX_FMT_SBGGR8:
	result = "BA81";
	break;
      //case V4L2_PIX_FMT_SBGGR16:
	//result = "BA82";
	//break;
      case V4L2_PIX_FMT_RGB332:
	result = "RGB1";
	break;
      case V4L2_PIX_FMT_RGB444:
	result = "R444";
	break;
      case V4L2_PIX_FMT_RGB555:
	result = "RGBO";
	break;
      case V4L2_PIX_FMT_RGB565:
	result = "RGBP";
	break;
      case V4L2_PIX_FMT_RGB555X:
	result = "RGBQ";
	break;
      case V4L2_PIX_FMT_RGB565X:
	result = "RGBR";
	break;
      case V4L2_PIX_FMT_BGR24:
	result = "BGR3";
	break;
      case V4L2_PIX_FMT_RGB24:
	result = "RGB3";
	break;
      case V4L2_PIX_FMT_BGR32:
	result = "BGR4";
	break;
      case V4L2_PIX_FMT_YUV444:
	result = "Y444";
	break;
      case V4L2_PIX_FMT_YUV555:
	result = "YUVO";
	break;
      case V4L2_PIX_FMT_YUV565:
	result = "YUVP";
	break;
      case V4L2_PIX_FMT_YUV32:
	result = "YUV4";
	break;
      //case V4L2_PIX_FMT_Y16:
	//result = "Y16";
	//break;
      case V4L2_PIX_FMT_YUYV:
	result = "YUYV";
	break;
      case V4L2_PIX_FMT_Y41P:
	result = "Y41P";
	break;
      case V4L2_PIX_FMT_YVU420:
	result = "YV12";
	break;
      case V4L2_PIX_FMT_YUV420:
	result = "YU12";
	break;
      case V4L2_PIX_FMT_YVU410:
	result = "YVV9";
	break;
      case V4L2_PIX_FMT_YUV410:
	result = "YUV9";
	break;
      case V4L2_PIX_FMT_YUV422P:
	result = "422P";
	break;
      case V4L2_PIX_FMT_YUV411P:
	result = "411P";
	break;
      case V4L2_PIX_FMT_NV12:
	result = "NV12";
	break;
      case V4L2_PIX_FMT_NV21:
	result = "NV21";
	break;
      case V4L2_PIX_FMT_JPEG:
	result = "JPEG";
	break;
      case V4L2_PIX_FMT_MPEG:
	result = "MPEG";
	break;
    }
    return result;
}

static int
read_frame(
  unsigned int width,
  unsigned int height,
  void *tracker)
{
    struct v4l2_buffer buf;
    unsigned int i;
    int r;

    switch (io) {
      case IO_METHOD_READ:
	if (-1 == read(fd, buffers[0].start, buffers[0].length)) {
            switch errno {
              case EAGAIN:
		return 0;
	      case EIO:
		/* Could ignore EIO, see spec. */
		/* fall through */
	      default:
		errno_exit("read");
	    }
	}
	process_image(&buffers[0], width, height, tracker);
	break;

      case IO_METHOD_MMAP:
	CLEAR(buf);

        buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
        buf.memory = V4L2_MEMORY_MMAP;

	r = xioctl(fd, VIDIOC_DQBUF, &buf);
    	if (-1 == r) {
	    switch errno {
              case EAGAIN:
  		return 0;

	      case EIO:
		/* Could ignore EIO, see spec. */
		/* fall through */

	      default:
		errno_exit("VIDIOC_DQBUF");
	    }
	}
	(void)fprintf(stderr, "r=%d err=%d\n", r, errno);

        assert(buf.index < n_buffers);

	process_image(&buffers[buf.index], width, height, tracker);

	if (-1 == xioctl(fd, VIDIOC_QBUF, &buf)) {
	    errno_exit("VIDIOC_QBUF");
	}
	break;

      case IO_METHOD_USERPTR:
	CLEAR(buf);

    	buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    	buf.memory = V4L2_MEMORY_USERPTR;

	if (-1 == xioctl(fd, VIDIOC_DQBUF, &buf)) {
	    switch errno {
	      case EAGAIN:
		return 0;

	      case EIO:
		/* Could ignore EIO, see spec. */

		/* fall through */

	      default:
		errno_exit("VIDIOC_DQBUF");
	    }
	}

	for (i = 0; i < n_buffers; ++i){
	    if (buf.m.userptr == (unsigned long) buffers[i].start &&
	      buf.length == buffers[i].length) {
		break;
	    }
	}
	assert(i < n_buffers);

    	/* process_image((void *) buf.m.userptr); */
	(void)fprintf(stderr, "fix this\n");
	exit(EXIT_FAILURE);

	if (-1 == xioctl(fd, VIDIOC_QBUF, &buf)) {
	    errno_exit("VIDIOC_QBUF");
	}

	break;
    }

    return 1;
}

static void
mainloop(
  unsigned int width,
  unsigned int height)
{
    unsigned int count;
    // switch this between true and false to test
    // simple-id versus BCH-id markers
    //const bool useBCH = true;
    const int bpp = 1;
    size_t numPixels;
    //size_t numBytesRead;
    //    const char *fName = useBCH ? "data/image_320_240_8_marker_id_bch_nr0100.raw"
    //            : "data/image_320_240_8_marker_id_simple_nr031.raw";

    numPixels = width * height * bpp;

    //unsigned char cameraBuffer[numPixels];

#if 0
    // try to load a test camera image.
    // these images files are expected to be simple 8-bit raw pixel
    // data without any header. the images are expetected to have a
    // size of 320x240.
    if (FILE* fp = fopen(fName, "rb")) {
        numBytesRead = fread(cameraBuffer, 1, numPixels, fp);
        fclose(fp);
    } else {
        printf("Failed to open %s\n", fName);
        return -1;
    }

    if (numBytesRead != numPixels) {
        printf("Failed to read %s\n", fName);
        return -1;
    }

#endif

    // create a tracker that does:
    //  - 6x6 sized marker images (required for binary markers)
    //  - samples at a maximum of 6x6
    //  - works with luminance (gray) images
    //  - can load a maximum of 0 non-binary pattern
    //  - can detect a maximum of 8 patterns in one imagege
    void *tracker = (void *)0;

    count = 100;

    while (count-- > 0) {
        for (;;) {
 	    fd_set fds;
            struct timeval tv;
            int r;

            FD_ZERO(&fds);
            FD_SET(fd, &fds);

            /* Timeout. */
            tv.tv_sec = 2;
            tv.tv_usec = 0;

            r = select(fd + 1, &fds, NULL, NULL, &tv);

            if (-1 == r) {
	        if (EINTR == errno) {
	            continue;
	        }
                errno_exit("select");
            }

            if (0 == r) {
	        (void)fprintf(stderr, "select timeout\n");
                exit(EXIT_FAILURE);
            }

	    if (read_frame(width, height, tracker)) {
                break;
	    }

	    /* EAGAIN - continue select loop. */
        }
    }
    (void)printf("\n");
}

static void
stop_capturing(void)
{
    enum v4l2_buf_type type;

    switch (io) {
      case IO_METHOD_READ:
	/* Nothing to do. */
	break;

      case IO_METHOD_MMAP:
      case IO_METHOD_USERPTR:
	type = V4L2_BUF_TYPE_VIDEO_CAPTURE;

	if (-1 == xioctl(fd, VIDIOC_STREAMOFF, &type))
	    errno_exit("VIDIOC_STREAMOFF");

	    break;
    }
}

static void
start_capturing(void)
{
    unsigned int i;
    enum v4l2_buf_type type;

    switch (io) {
      case IO_METHOD_READ:
	/* Nothing to do. */
	break;

      case IO_METHOD_MMAP:
	for (i = 0; i < n_buffers; ++i) {
	    struct v4l2_buffer buf;

	    CLEAR(buf);

	    buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	    buf.memory = V4L2_MEMORY_MMAP;
	    buf.index = i;

	    if (-1 == xioctl(fd, VIDIOC_QBUF, &buf)) {
		 errno_exit("VIDIOC_QBUF");
	    }
	}
		
	type = V4L2_BUF_TYPE_VIDEO_CAPTURE;

	if (-1 == xioctl(fd, VIDIOC_STREAMON, &type)) {
	    errno_exit("VIDIOC_STREAMON");
	}

	break;

      case IO_METHOD_USERPTR:
	for (i = 0; i < n_buffers; ++i) {
	    struct v4l2_buffer buf;

	    CLEAR(buf);

	    buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	    buf.memory = V4L2_MEMORY_USERPTR;
	    buf.index = i;
	    buf.m.userptr = (unsigned long) buffers[i].start;
	    buf.length = buffers[i].length;

	    if (-1 == xioctl(fd, VIDIOC_QBUF, &buf)) {
		errno_exit("VIDIOC_QBUF");
	    }
	}

	type = V4L2_BUF_TYPE_VIDEO_CAPTURE;

	if (-1 == xioctl(fd, VIDIOC_STREAMON, &type)) {
	    errno_exit("VIDIOC_STREAMON");
	}

	break;
    }
}

static void
uninit_device(void)
{
    unsigned int i;

    switch (io) {
      case IO_METHOD_READ:
	free(buffers[0].start);
	break;

      case IO_METHOD_MMAP:
	for (i = 0; i < n_buffers; ++i) {
	    if (-1 == munmap(buffers[i].start, buffers[i].length)) {
		errno_exit("munmap");
	    }
	}
	break;

      case IO_METHOD_USERPTR:
	for (i = 0; i < n_buffers; ++i) {
	    free(buffers[i].start);
	}
	break;
    }

    free(buffers);
}

static void
init_read(unsigned int buffer_size)
{
    buffers = (struct buffer *)calloc(1, sizeof(*buffers));

    if (!buffers) {
	(void)fprintf(stderr, "Out of memory\n");
	exit(EXIT_FAILURE);
    }

    buffers[0].length = buffer_size;
    buffers[0].start = malloc(buffer_size);

    if (!buffers[0].start) {
	(void)fprintf(stderr, "Out of memory\n");
	exit(EXIT_FAILURE);
    }
}

static void
init_mmap(void)
{
    struct v4l2_requestbuffers req;

    CLEAR(req);

    req.count = 16;
    req.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    req.memory = V4L2_MEMORY_MMAP;

    if (-1 == xioctl(fd, VIDIOC_REQBUFS, &req)) {
	if (EINVAL == errno) {
	    (void)fprintf(stderr,
	      "%s does not support memory mapping\n", dev_name);
	    exit(EXIT_FAILURE);
	} else {
	    errno_exit("VIDIOC_REQBUFS");
	}
    }

    if (req.count < 2) {
	(void)fprintf(stderr,
	  "Insufficient buffer memory on %s\n", dev_name);
	exit(EXIT_FAILURE);
    }

    buffers = (struct buffer *)calloc(req.count, sizeof(*buffers));

    if (!buffers) {
	(void)fprintf(stderr, "Out of memory\n");
	exit(EXIT_FAILURE);
    }

    for (n_buffers = 0; n_buffers < req.count; ++n_buffers) {
	struct v4l2_buffer buf;

	CLEAR(buf);

	buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	buf.memory = V4L2_MEMORY_MMAP;
	buf.index = n_buffers;

	if (-1 == xioctl(fd, VIDIOC_QUERYBUF, &buf)) {
	    errno_exit("VIDIOC_QUERYBUF");
	}
	(void)printf("buf:index:%d type:%d used:%d flags:0x%x len:%d off:%d\n",
	  buf.index, buf.type, buf.bytesused,
	  buf.flags, buf.length, buf.m.offset);

	buffers[n_buffers].length = buf.length;
	buffers[n_buffers].start =
	  mmap(NULL /* start anywhere */,
	        buf.length,
	        PROT_READ | PROT_WRITE /* required */,
	        MAP_SHARED /* recommended */,
	        fd, buf.m.offset);
	(void)printf("buffer[%d]=0x%x, len=%d off=%d\n",
	  n_buffers, buffers[n_buffers].start, buf.length, buf.m.offset);

	if (MAP_FAILED == buffers[n_buffers].start) {
	    errno_exit("mmap");
	}
    }
}

static void
init_userp(unsigned int	buffer_size)
{
    struct v4l2_requestbuffers req;
    unsigned int page_size;

    page_size = getpagesize();
    buffer_size = (buffer_size + page_size - 1) & ~(page_size - 1);

    CLEAR(req);

    req.count = 4;
    req.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    req.memory = V4L2_MEMORY_USERPTR;

    if (-1 == xioctl(fd, VIDIOC_REQBUFS, &req)) {
        if (EINVAL == errno) {
            fprintf(stderr, "%s does not support "
                   "user pointer i/o\n", dev_name);
            exit(EXIT_FAILURE);
        } else {
            errno_exit("VIDIOC_REQBUFS");
        }
    }

    buffers = (struct buffer *)calloc(4, sizeof(*buffers));

    if (!buffers) {
        fprintf(stderr, "Out of memory\n");
        exit(EXIT_FAILURE);
    }

    for (n_buffers = 0; n_buffers < 4; ++n_buffers) {
        buffers[n_buffers].length = buffer_size;
        buffers[n_buffers].start =
	  memalign(/* boundary */ page_size, buffer_size);

        if (!buffers[n_buffers].start) {
    	    fprintf(stderr, "Out of memory\n");
            exit(EXIT_FAILURE);
	}
    }
}

static void
init_device(
  unsigned int width,
  unsigned int height)
{
    struct v4l2_capability cap;
    struct v4l2_cropcap cropcap;
    struct v4l2_crop crop;
    struct v4l2_format fmt;
    unsigned int min;
    unsigned int i;
    int format_id;

    if (-1 == xioctl(fd, VIDIOC_QUERYCAP, &cap)) {
	if (EINVAL == errno) {
	    (void)fprintf(stderr,
	      "%s is not a V4L2 device\n", dev_name);
	    exit(EXIT_FAILURE);
	} else {
	    errno_exit("VIDIOC_QUERYCAP");
	}
    }

    if (!(cap.capabilities & V4L2_CAP_VIDEO_CAPTURE)) {
	(void)fprintf(stderr,
	  "%s is not a video capture device\n", dev_name);
	exit(EXIT_FAILURE);
    }

    switch (io) {
      case IO_METHOD_READ:
	if (!(cap.capabilities & V4L2_CAP_READWRITE)) {
	    (void)fprintf(stderr,
	      "%s does not support read i/o\n", dev_name);
	    exit(EXIT_FAILURE);
	}
	break;

      case IO_METHOD_MMAP:
      case IO_METHOD_USERPTR:
	if (!(cap.capabilities & V4L2_CAP_STREAMING)) {
	    (void)fprintf(stderr,
	      "%s does not support streaming i/o\n", dev_name);
	    exit(EXIT_FAILURE);
	}
	break;
    }

    /* Select video input, video standard and tune here. */

    CLEAR(cropcap);

    cropcap.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;

    if (0 == xioctl(fd, VIDIOC_CROPCAP, &cropcap)) {
	crop.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	crop.c = cropcap.defrect; /* reset to default */

	if (-1 == xioctl(fd, VIDIOC_S_CROP, &crop)) {
	    switch errno {
	      case EINVAL:
		/* Cropping not supported. */
		break;
	      default:
		/* Errors ignored. */
		break;
	    }
	}
    } else {	
	/* Errors ignored. */
    }

    i = 0;
    while (1) {
	format_id = format_ids[i];
	if (format_id == -1) {
	    break;
	}
	(void)printf("[%d]=%x ('%s')",
	  i, format_id, format_to_string(format_id));

	CLEAR(fmt);
	fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	fmt.fmt.pix.width = width; 
	fmt.fmt.pix.height = height;
	fmt.fmt.pix.pixelformat = format_id;
	fmt.fmt.pix.field = V4L2_FIELD_ANY;
	if (-1 == xioctl(fd, VIDIOC_TRY_FMT, &fmt)) {
	    (void)printf(" no\n");
	} else {
	    (void)printf(" yes field=%d %d x %d\n",
	      fmt.fmt.pix.field, width, height);
	}
 	i++;
    }

    CLEAR(fmt);

    fmt.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    fmt.fmt.pix.width = width;
    fmt.fmt.pix.height = height;
    fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_YUYV;
    /* fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_BGR32; */
    fmt.fmt.pix.field = V4L2_FIELD_INTERLACED;

    (void)printf("width=%d height=%d format=%x field=%d\n",
		 fmt.fmt.pix.width, fmt.fmt.pix.height,
		 fmt.fmt.pix.pixelformat, fmt.fmt.pix.field);

    if (-1 == xioctl(fd, VIDIOC_S_FMT, &fmt)) {
	errno_exit("VIDIOC_S_FMT");
    }

    /* Note VIDIOC_S_FMT may change width and height. */

    /* Buggy driver paranoia. */
    min = fmt.fmt.pix.width * 2;
    if (fmt.fmt.pix.bytesperline < min) {
	fmt.fmt.pix.bytesperline = min;
    }
    (void)printf("bytes_per_line=%d\n", fmt.fmt.pix.bytesperline);
    min = fmt.fmt.pix.bytesperline * fmt.fmt.pix.height;
    if (fmt.fmt.pix.sizeimage < min) {
	fmt.fmt.pix.sizeimage = min;
    }

    (void)printf("size_image=%d\n", fmt.fmt.pix.sizeimage);

    switch (io) {
      case IO_METHOD_READ:
	init_read(fmt.fmt.pix.sizeimage);
	break;

      case IO_METHOD_MMAP:
	init_mmap();
	break;

      case IO_METHOD_USERPTR:
	init_userp(fmt.fmt.pix.sizeimage);
	break;
    }
}

static void
close_device(void)
{
    if (-1 == close(fd)) {
	errno_exit("close");
    }

    fd = -1;
}

static void
open_device(void)
{
    struct stat st; 

    if (-1 == stat(dev_name, &st)) {
	(void)fprintf(stderr, "Cannot identify '%s': %d, %s\n",
          dev_name, errno, strerror(errno));
        exit(EXIT_FAILURE);
    }

    if (!S_ISCHR(st.st_mode)) {
	(void)fprintf(stderr, "%s is not character device\n", dev_name);
        exit(EXIT_FAILURE);
    }

    fd = open(dev_name, O_RDWR /* required */ | O_NONBLOCK, 0);

    if (-1 == fd) {
	(void)fprintf(stderr, "Cannot open '%s': %d, %s\n",
                      dev_name, errno, strerror(errno));
        exit(EXIT_FAILURE);
    }
}

static void
usage(FILE *fp, int argc, char **argv)
{
    (void)fprintf(fp,
      "Usage: %s [options]\n\n"
      "Options:\n"
      "-d | --device name   Video device name [/dev/video]\n"
      "-h | --help          Print this message\n"
      "-m | --mmap          Use memory mapped buffers\n"
      "-r | --read          Use read() calls\n"
      "-u | --userp         Use application allocated buffers\n"
      "",
      argv[0]);
}

static const char short_options [] = "d:hmru";

static const struct option
long_options [] = {
    { "device",     required_argument,      NULL,           'd' },
    { "help",       no_argument,            NULL,           'h' },
    { "mmap",       no_argument,            NULL,           'm' },
    { "read",       no_argument,            NULL,           'r' },
    { "userp",      no_argument,            NULL,           'u' },
    { 0, 0, 0, 0 }
};

int
main(int argc, char **argv)
{
    dev_name = "/dev/video0";
    int height;
    int width;

    for (;;) {
	int index;
	int c;
                
	c = getopt_long(argc, argv,
	  short_options, long_options, &index);

	if (-1 == c) {
	    break;
	}

	switch (c) {
	  case 0: /* getopt_long() flag */
	    break;

	  case 'd':
	    dev_name = optarg;
	    break;

	  case 'h':
	    usage(stdout, argc, argv);
	    exit(EXIT_SUCCESS);

	  case 'm':
	    io = IO_METHOD_MMAP;
	    break;

	  case 'r':
	    io = IO_METHOD_READ;
	    break;

	  case 'u':
	    io = IO_METHOD_USERPTR;
	    break;

	  default:
	    usage(stderr, argc, argv);
	    exit(EXIT_FAILURE);
	}
    }

    width = 320;
    height = 240;

    open_device();

    init_device(width, height);

    start_capturing();

    mainloop(width, height);

    stop_capturing();

    uninit_device();

    close_device();

    exit(EXIT_SUCCESS);

    return 0;
}
