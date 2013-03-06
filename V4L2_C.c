/*
 * Copyright (c) 2010 by Wayne C. Gramlich
 * All rights reserved.
 */

/* System header files: */
#include <errno.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/mman.h>
#include <sys/ioctl.h>
	
/* Other header files: */
#include "CV.h"
#include "CV_C.h"
#include "Easy_C.h"
#include "Easy_C_C.h"
#include "V4L2.h"
#include "V4L2_C.h"

/* {V4L2} stuff: */

Integer
V4L2__stream_on(
  Integer file_descriptor,
  V4L2_Buffer_Type type)
{
    Integer result;

    do {
      (void)fprintf(stderr, "stream_on:type=%d\n", type); 
      result = ioctl(file_descriptor, VIDIOC_STREAMON, (void *)&type);
    } while (result == -1 && errno == EINTR);
    return result;
}


/* {V4L2_Buffer} stuff: */

struct v4l2_buffer V4L2_Buffer__Initial;
V4L2_Buffer V4L2_Buffer__null = &V4L2_Buffer__Initial;

Unsigned V4L2_Buffer__mapped = V4L2_BUF_FLAG_MAPPED;
Unsigned V4L2_Buffer__queued = V4L2_BUF_FLAG_QUEUED;
Unsigned V4L2_Buffer__done = V4L2_BUF_FLAG_DONE;
Unsigned V4L2_Buffer__keyframe = V4L2_BUF_FLAG_KEYFRAME;
Unsigned V4L2_Buffer__pframe = V4L2_BUF_FLAG_PFRAME;
Unsigned V4L2_Buffer__bframe = V4L2_BUF_FLAG_BFRAME;
Unsigned V4L2_Buffer__timecode = V4L2_BUF_FLAG_TIMECODE;
Unsigned V4L2_Buffer__input = V4L2_BUF_FLAG_INPUT;

void
V4L2_Buffer__Initialize(void)
{
}

Unsigned
V4L2_Buffer__bytes_used_get(
  V4L2_Buffer buffer)
{
    return buffer->bytesused;
}

Integer
V4L2_Buffer__dequeue(
  V4L2_Buffer buffer,
  Integer file_descriptor)
{
    Integer result;

    do {
      result = ioctl(file_descriptor, VIDIOC_DQBUF, (void *)buffer);
      /* (void)fprintf(stderr, "dequeue:type=%d memory:%d index=%d\n",
	 buffer->type, buffer->memory, buffer->index);  */
    } while (result == -1 && errno == EINTR);
    return result;
}

Integer
V4L2_Buffer__enqueue(
  V4L2_Buffer buffer,
  Integer file_descriptor)
{
    Integer result;

    do {
      result = ioctl(file_descriptor, VIDIOC_QBUF, (void *)buffer);
      /* (void)fprintf(stderr, "enqueue:type=%d memory:%d index=%d\n",
	 buffer->type, buffer->memory, buffer->index);  */
    } while (result == -1 && errno == EINTR);
    return result;
}

void
V4L2_Buffer__erase(
  V4L2_Buffer buffer)
{
    Unsigned malloc_bytes = sizeof *((V4L2_Buffer)0);
    (void)memset((void *)buffer, 0, malloc_bytes);    
}

Unsigned
V4L2_Buffer__flags_get(
  V4L2_Buffer buffer)
{
    return buffer->flags;
}

Unsigned
V4L2_Buffer__index_get(
  V4L2_Buffer buffer)
{
    return buffer->index;
}

void
V4L2_Buffer__index_set(
  V4L2_Buffer buffer,
  Unsigned index)
{
    buffer->index = index;
}

Unsigned
V4L2_Buffer__length_get(
  V4L2_Buffer buffer)
{
    return buffer->length;
}

V4L2_Buffer
V4L2_Buffer__new(void)
{
    Unsigned malloc_bytes = sizeof *((V4L2_Buffer)0);
    /* (void)printf("V4L2_Buffer__new: malloc_bytes=%d\n", malloc_bytes); */

    V4L2_Buffer buffer = (V4L2_Buffer)malloc(malloc_bytes);
    V4L2_Buffer__erase(buffer);
    return buffer;
}

Unsigned
V4L2_Buffer__offset_get(
  V4L2_Buffer buffer)
{
    return buffer->m.offset;
}

Integer
V4L2_Buffer__query(
  V4L2_Buffer buffer,
  Integer file_descriptor)
{
    Integer result;
    /* (void)printf("=>V4L2_Buffer__query(%d)\n", file_descriptor); */

    do {
      result = ioctl(file_descriptor, VIDIOC_QUERYBUF, (void *)buffer);
      /* (void)printf("type=%d mem=%d index=%d\n",
	 buffer->type, buffer->memory, buffer->index); */
    } while (result == -1 && errno == EINTR);
    return result;
}

void
V4L2_Buffer__memory_set(
  V4L2_Buffer buffer,
  V4L2_Memory memory)
{
    buffer->memory = memory;
}

void
V4L2_Buffer__type_set(
  V4L2_Buffer buffer,
  V4L2_Buffer_Type type)
{
    buffer->type = type;
}



/* {V4L2_Buffer_Type} stuff: */

V4L2_Buffer_Type V4L2_Buffer_Type__video_capture = V4L2_BUF_TYPE_VIDEO_CAPTURE;
V4L2_Buffer_Type V4L2_Buffer_Type__video_output = V4L2_BUF_TYPE_VIDEO_OUTPUT;
V4L2_Buffer_Type V4L2_Buffer_Type__video_overlay = V4L2_BUF_TYPE_VIDEO_OVERLAY;
V4L2_Buffer_Type V4L2_Buffer_Type__vbi_capture = V4L2_BUF_TYPE_VBI_CAPTURE;
V4L2_Buffer_Type V4L2_Buffer_Type__vbi_output = V4L2_BUF_TYPE_VBI_OUTPUT;
V4L2_Buffer_Type V4L2_Buffer_Type__sliced_vbi_capture =
  V4L2_BUF_TYPE_SLICED_VBI_CAPTURE;
V4L2_Buffer_Type V4L2_Buffer_Type__sliced_vbi_output = V4L2_BUF_TYPE_SLICED_VBI_OUTPUT;
V4L2_Buffer_Type V4L2_Buffer_Type__video_output_overlay =
  V4L2_BUF_TYPE_VIDEO_OUTPUT_OVERLAY;
V4L2_Buffer_Type V4L2_Buffer_Type__PRIVATE = V4L2_BUF_TYPE_PRIVATE;

void
V4L2_Buffer_Type__Initialize(void)
{
}

/* {V4L2_Chunk} stuff: */

struct chunk V4L2_Chunk__Initial;
V4L2_Chunk V4L2_Chunk__null = &V4L2_Chunk__Initial;

void
V4L2_Chunk__Initialize(void)
{
}

V4L2_Chunk
V4L2_Chunk__create(
  V4L2_Buffer buffer,
  Integer file_descriptor)
{
    Unsigned malloc_bytes = sizeof *((V4L2_Chunk)0);
    /* (void)printf("V4L2_Chunk__create: malloc_bytes=%d\n", malloc_bytes); */
    V4L2_Chunk chunk = (V4L2_Chunk)malloc(malloc_bytes);
    if (chunk == (V4L2_Chunk)0) {
        chunk = V4L2_Chunk__null;
    } else {
	(void)memset((void *)chunk, 0, malloc_bytes);

	/* Perform the memory map: */
	/* (void)fprintf(stderr, "length=%d offset=%d\n",
	   buffer->length, buffer->m.offset); */
	unsigned char *data = mmap(0, buffer->length, PROT_READ | PROT_WRITE,
	  MAP_SHARED, file_descriptor, buffer->m.offset);
	if (data == MAP_FAILED) {
	     /* (void)printf("errno=%d EACCES=%d\n", errno, EACCES);
	     perror("mmap failed"); */
	    chunk = V4L2_Chunk__null;
	} else {
	    chunk->data = data;
	}
    }
    return chunk;
}

void
V4L2_Chunk__yuvu_to_gray(
  V4L2_Chunk chunk,
  CV_Image gray_image)
{
    Integer width = gray_image->width;
    Integer height = gray_image->height;
    unsigned char *yuvu = chunk->data;
    unsigned char *gray = gray_image->imageData;
    unsigned int yuv_row_span = yuv_row_span = width * 2;
    unsigned int gray_row_span = gray_row_span = width * 1;
    unsigned row;

    for (row = 0; row < height; row++) {
	unsigned char *yuvu_pointer;
	unsigned char *gray_pointer;
	unsigned column;

	yuvu_pointer = &yuvu[row * yuv_row_span];
	gray_pointer = &gray[row * gray_row_span];

	// Now process two pixels at a time: 
	for (column = 0; column < width; column += 2) {
	    // Grab Y0, U, Y1, and V values: 
	    unsigned char y0, y1;
	    y0 = *yuvu_pointer++;
	    yuvu_pointer++;	// u 
	    y1 = *yuvu_pointer++;
	    yuvu_pointer++;	// v 
	    *gray_pointer++ = y0;
	    *gray_pointer++ = y1;
	}
    }
}

/* {V4L2_Capability} stuff: */

struct v4l2_capability V4L2_Capability__Initial;

V4L2_Capability V4L2_Capability__null = &V4L2_Capability__Initial;

Unsigned V4L2_Capability__video_capture = V4L2_CAP_VIDEO_CAPTURE;
Unsigned V4L2_Capability__video_output = V4L2_CAP_VIDEO_OUTPUT;
Unsigned V4L2_Capability__video_overlay = V4L2_CAP_VIDEO_OVERLAY;
Unsigned V4L2_Capability__vbi_capture = V4L2_CAP_VBI_CAPTURE;
Unsigned V4L2_Capability__vbi_output = V4L2_CAP_VBI_OUTPUT;
Unsigned V4L2_Capability__sliced_vbi_capture = V4L2_CAP_SLICED_VBI_CAPTURE;
Unsigned V4L2_Capability__sliced_vbi_output = V4L2_CAP_SLICED_VBI_OUTPUT;
Unsigned V4L2_Capability__rds_capture = V4L2_CAP_RDS_CAPTURE;
Unsigned V4L2_Capability__video_output_overlay = V4L2_CAP_VIDEO_OUTPUT_OVERLAY;
/* Unsigned V4L2_Capability__hw_freq_seek = V4L2_CAP_HW_FREQ_SEEK; */
Unsigned V4L2_Capability__tuner = V4L2_CAP_TUNER;
Unsigned V4L2_Capability__audio = V4L2_CAP_AUDIO;
Unsigned V4L2_Capability__radio = V4L2_CAP_RADIO;
Unsigned V4L2_Capability__readwrite = V4L2_CAP_READWRITE;
Unsigned V4L2_Capability__asyncio = V4L2_CAP_ASYNCIO;
Unsigned V4L2_Capability__streaming = V4L2_CAP_STREAMING;

void
V4L2_Capability__Initialize(void)
{
}

Unsigned
V4L2_Capability__capabilities_get(
  V4L2_Capability capability)
{
    return capability->capabilities;
}

V4L2_Capability
V4L2_Capability__new(void)
{
    Unsigned malloc_bytes = sizeof *((V4L2_Capability)0);
    /* (void)printf("V4L2_Capabilty__new: malloc_bytes=%d\n", malloc_bytes); */

    V4L2_Capability capability = (V4L2_Capability)malloc(malloc_bytes);
    (void)memset((void *)capability, 0, malloc_bytes);
    return capability;
}

Integer
V4L2_Capability__query(
  V4L2_Capability capability,
  Integer file_descriptor)
{
    Integer result;

    do {
	result = ioctl(file_descriptor, VIDIOC_QUERYCAP, capability);
    } while (result == -1 && errno == EINTR);
    return result;
}

/* {V4L2_Crop} stuff:*/

struct v4l2_crop V4L2_Crop__Initial;

V4L2_Crop V4L2_Crop__null = &V4L2_Crop__Initial;

void
V4L2_Crop__Initialize(void)
{
}

V4L2_Rectangle
V4L2_Crop__crop_rectangle_get(
  V4L2_Crop crop)
{
    return &crop->c;
}

V4L2_Crop
V4L2_Crop__new(void)
{
    Unsigned malloc_bytes = sizeof *((V4L2_Crop)0);
    /* (void)printf("V4L2_Crop__new: malloc_bytes=%d\n", malloc_bytes); */

    V4L2_Crop crop = (V4L2_Crop)malloc(malloc_bytes);
    (void)memset((void *)crop, 0, malloc_bytes);
    return crop;
}

Integer
V4L2_Crop__set(
  V4L2_Crop crop,
  Integer file_descriptor)
{
    Integer result;

    do {
        result = ioctl(file_descriptor, VIDIOC_S_CROP, (void *)crop);
    } while (result == -1 && errno == EINTR);
    return result;
}

void
V4L2_Crop__type_set(
  V4L2_Crop crop,
  V4L2_Buffer_Type buffer_type)
{
    crop->type = buffer_type;
}


/* {V4L2_Crop_Capability} stuff:*/

struct v4l2_cropcap V4L2_Crop_Capability__Initial;

V4L2_Crop_Capability V4L2_Crop_Capability__null =
  &V4L2_Crop_Capability__Initial;

void
V4L2_Crop_Capability__Initialize(void)
{
}

V4L2_Rectangle
V4L2_Crop_Capability__bounds_get(
  V4L2_Crop_Capability crop_capability)
{
    return &crop_capability->bounds;
}

V4L2_Rectangle
V4L2_Crop_Capability__default_rectangle_get(
  V4L2_Crop_Capability crop_capability)
{
    return &crop_capability->defrect;
}

V4L2_Crop_Capability
V4L2_Crop_Capability__new(void)
{
    Unsigned malloc_bytes = sizeof *((V4L2_Crop_Capability)0);
    /* (void)printf("V4L2_Capabilty__new: malloc_bytes=%d\n", malloc_bytes); */

    V4L2_Crop_Capability crop_capability =
      (V4L2_Crop_Capability)malloc(malloc_bytes);
    (void)memset((void *)crop_capability, 0, malloc_bytes);
    return crop_capability;
}

Integer
V4L2_Crop_Capability__query(
  V4L2_Crop_Capability crop_capability,
  Integer file_descriptor)
{
    Integer result;

    do {
	result = ioctl(file_descriptor, VIDIOC_CROPCAP, crop_capability);
    } while (result == -1 && errno == EINTR);
    return result;
}

V4L2_Buffer_Type
V4L2_Crop_Capability__type_get(
  V4L2_Crop_Capability crop_capability)
{
    return crop_capability->type;
}

void
V4L2_Crop_Capability__type_set(
  V4L2_Crop_Capability crop_capability,
  V4L2_Buffer_Type buffer_type)
{
    crop_capability->type = buffer_type;
}

/* {V4L2_Field_Stuff} : */

V4L2_Field V4L2_Field__any = V4L2_FIELD_ANY;
V4L2_Field V4L2_Field__none = V4L2_FIELD_NONE;
V4L2_Field V4L2_Field__top = V4L2_FIELD_TOP;
V4L2_Field V4L2_Field__bottom = V4L2_FIELD_BOTTOM;
V4L2_Field V4L2_Field__interlaced = V4L2_FIELD_INTERLACED;
V4L2_Field V4L2_Field__seq_tb = V4L2_FIELD_SEQ_TB;
V4L2_Field V4L2_Field__seq_bt = V4L2_FIELD_SEQ_BT;
V4L2_Field V4L2_Field__alternate = V4L2_FIELD_ALTERNATE;
V4L2_Field V4L2_Field__interlaced_tb = V4L2_FIELD_INTERLACED_TB;
V4L2_Field V4L2_Field__interlaced_bt = V4L2_FIELD_INTERLACED_BT;

void
V4L2_Field__Initialize(void)
{
}

/* {V4L2_Format} stuff: */

struct v4l2_format V4L2_Format__Initial;

V4L2_Format V4L2_Format__null = &V4L2_Format__Initial;

void
V4L2_Format__Initialize(void)
{
}

V4L2_Format
V4L2_Format__new(void)
{
    Unsigned malloc_bytes = sizeof *((V4L2_Format)0);
    /* (void)printf("V4L2_Format__new: malloc_bytes=%d\n", malloc_bytes); */

    V4L2_Format format = (V4L2_Format)malloc(malloc_bytes);
    (void)memset((void *)format, 0, malloc_bytes);
    return format;
}

V4L2_Buffer_Type
V4L2_Format__type_get(
  V4L2_Format format)
{
    return format->type;
}

Integer
V4L2_Format__set(
  V4L2_Format format,
  Integer file_descriptor)
{
    Integer result;

    do {
	result = ioctl(file_descriptor, VIDIOC_S_FMT, (void *)format);
    } while (result == -1 && errno == EINTR);
    if (result == -1) {
	perror("V4L2_Pixel_Format__set()");
    }
    return result;
}

void
V4L2_Format__type_set(
  V4L2_Format format,
  V4L2_Buffer_Type type)
{
    format->type = type;
}

V4L2_Pixel_Format
V4L2_Format__pixel_format_get(
  V4L2_Format format)
{
    return &format->fmt.pix;
}

/* {V4L2_Memory} stuff: */

V4L2_Memory V4L2_Memory__mmap = V4L2_MEMORY_MMAP;
V4L2_Memory V4L2_Memory__user_pointer = V4L2_MEMORY_USERPTR;
V4L2_Memory V4L2_Memory__overlay = V4L2_MEMORY_OVERLAY;

void
V4L2_Memory__Initialize(void)
{
}


/* {V4L2_Pixel_Format} stuff */

Unsigned V4L2_Pixel_Format__rgb332 = V4L2_PIX_FMT_RGB332;
Unsigned V4L2_Pixel_Format__rgb444 = V4L2_PIX_FMT_RGB444;
Unsigned V4L2_Pixel_Format__rgb555 = V4L2_PIX_FMT_RGB555;
Unsigned V4L2_Pixel_Format__rgb565 = V4L2_PIX_FMT_RGB565;
Unsigned V4L2_Pixel_Format__rgb555x = V4L2_PIX_FMT_RGB555X;
Unsigned V4L2_Pixel_Format__rgb565x = V4L2_PIX_FMT_RGB565X;
Unsigned V4L2_Pixel_Format__bgr24 = V4L2_PIX_FMT_BGR24;
Unsigned V4L2_Pixel_Format__rgb24 = V4L2_PIX_FMT_RGB24;
Unsigned V4L2_Pixel_Format__bgr32 = V4L2_PIX_FMT_BGR32;
Unsigned V4L2_Pixel_Format__rgb32 = V4L2_PIX_FMT_RGB32;
Unsigned V4L2_Pixel_Format__grey = V4L2_PIX_FMT_GREY;
/* Unsigned V4L2_Pixel_Format__y16 = V4L2_PIX_FMT_Y16; */
Unsigned V4L2_Pixel_Format__pal8 = V4L2_PIX_FMT_PAL8;
Unsigned V4L2_Pixel_Format__yvu410 = V4L2_PIX_FMT_YVU410;
Unsigned V4L2_Pixel_Format__yvu420 = V4L2_PIX_FMT_YVU420;
Unsigned V4L2_Pixel_Format__yuyv = V4L2_PIX_FMT_YUYV;
Unsigned V4L2_Pixel_Format__uyvy = V4L2_PIX_FMT_UYVY;
/* Unsigned V4L2_Pixel_Format__vyuy = V4L2_PIX_FMT_VYUY; */
Unsigned V4L2_Pixel_Format__yuv422p = V4L2_PIX_FMT_YUV422P;
Unsigned V4L2_Pixel_Format__yuv411p = V4L2_PIX_FMT_YUV411P;
Unsigned V4L2_Pixel_Format__y41p = V4L2_PIX_FMT_Y41P;
Unsigned V4L2_Pixel_Format__yuv444 = V4L2_PIX_FMT_YUV444;
Unsigned V4L2_Pixel_Format__yuf555 = V4L2_PIX_FMT_YUV555;
Unsigned V4L2_Pixel_Format__yuv565 = V4L2_PIX_FMT_YUV565;
Unsigned V4L2_Pixel_Format__yuv32 = V4L2_PIX_FMT_YUV32;
Unsigned V4L2_Pixel_Format__nv12 = V4L2_PIX_FMT_NV12;
Unsigned V4L2_Pixel_Format__nv21 = V4L2_PIX_FMT_NV21;
/* Unsigned V4L2_Pixel_Format__nv16 = V4L2_PIX_FMT_NV16; */
/* Unsigned V4L2_Pixel_Format__nv61 = V4L2_PIX_FMT_NV61; */
Unsigned V4L2_Pixel_Format__yuv410 = V4L2_PIX_FMT_YUV410;
Unsigned V4L2_Pixel_Format__yuv420 = V4L2_PIX_FMT_YUV420;
Unsigned V4L2_Pixel_Format__yyuv = V4L2_PIX_FMT_YYUV;
Unsigned V4L2_Pixel_Format__hi240 = V4L2_PIX_FMT_HI240;
Unsigned V4L2_Pixel_Format__hm12 = V4L2_PIX_FMT_HM12;
Unsigned V4L2_Pixel_Format__sbggr8 = V4L2_PIX_FMT_SBGGR8;
/* Unsigned V4L2_Pixel_Format__sgbrg8 = V4L2_PIX_FMT_SGBRG8; */
/* Unsigned V4L2_Pixel_Format__sgrbg8 = V4L2_PIX_FMT_SGRBG8; */
/* Unsigned V4L2_Pixel_Format__sgrbg10 = V4L2_PIX_FMT_SGRBG10; */
/* Unsigned V4L2_Pixel_Format__sgrbg10dpcm8 = V4L2_PIX_FMT_SGRBG10DPCM8; */
/* Unsigned V4L2_Pixel_Format__sbggr16 = V4L2_PIX_FMT_SBGGR16; */
Unsigned V4L2_Pixel_Format__mjpeg = V4L2_PIX_FMT_MJPEG;
Unsigned V4L2_Pixel_Format__jpeg = V4L2_PIX_FMT_JPEG;
Unsigned V4L2_Pixel_Format__dv = V4L2_PIX_FMT_DV;
Unsigned V4L2_Pixel_Format__mpeg = V4L2_PIX_FMT_MPEG;
Unsigned V4L2_Pixel_Format__wnva = V4L2_PIX_FMT_WNVA;
Unsigned V4L2_Pixel_Format__sn9c10x = V4L2_PIX_FMT_SN9C10X;
/* Unsigned V4L2_Pixel_Format__sn9c20x_i420 = V4L2_PIX_FMT_SN9C20X_I420; */
Unsigned V4L2_Pixel_Format__pwc1 = V4L2_PIX_FMT_PWC1;
Unsigned V4L2_Pixel_Format__pwc2 = V4L2_PIX_FMT_PWC2;
Unsigned V4L2_Pixel_Format__et61x251 = V4L2_PIX_FMT_ET61X251;
/* Unsigned V4L2_Pixel_Format__spca501 = V4L2_PIX_FMT_SPCA501; */
/* Unsigned V4L2_Pixel_Format__spca505 = V4L2_PIX_FMT_SPCA505; */
/* Unsigned V4L2_Pixel_Format__spca508 = V4L2_PIX_FMT_SPCA508; */
/* Unsigned V4L2_Pixel_Format__spca561 = V4L2_PIX_FMT_SPCA561; */
/* Unsigned V4L2_Pixel_Format__pac207 = V4L2_PIX_FMT_PAC207; */
/* Unsigned V4L2_Pixel_Format__mr97310a = V4L2_PIX_FMT_MR97310A; */
/* Unsigned V4L2_Pixel_Format__sq905c = V4L2_PIX_FMT_SQ905C; */
/* Unsigned V4L2_Pixel_Format__pjpg = V4L2_PIX_FMT_PJPG; */
/* Unsigned V4L2_Pixel_Format__yvyu = V4L2_PIX_FMT_YVYU; */
/* Unsigned V4L2_Pixel_Format__ov511 = V4L2_PIX_FMT_OV511; */
/* Unsigned V4L2_Pixel_Format__ov518 = V4L2_PIX_FMT_OV518; */

struct v4l2_pix_format V4L2_Pixel_Format__Initial;

V4L2_Pixel_Format V4L2_Pixel_Format__null = & V4L2_Pixel_Format__Initial;

void
V4L2_Pixel_Format__Initialize(void)
{
}

Integer
V4L2_Pixel_Format__bytes_per_line_get(
  V4L2_Pixel_Format pixel_format)
{
    return pixel_format->bytesperline;
}

void
V4L2_Pixel_Format__bytes_per_line_set(
  V4L2_Pixel_Format pixel_format,
  Integer bytes_per_line)
{
    pixel_format->bytesperline = bytes_per_line;
}

Integer
V4L2_Pixel_Format__size_image_get(
  V4L2_Pixel_Format pixel_format)
{
    return pixel_format->sizeimage;
}

void
V4L2_Pixel_Format__size_image_set(
  V4L2_Pixel_Format pixel_format,
  Integer size_image)
{
    pixel_format->sizeimage = size_image;
}

void
V4L2_Pixel_Format__field_set(
  V4L2_Pixel_Format pixel_format,
  V4L2_Field field)
{
    pixel_format->field = field;
}

void
V4L2_Pixel_Format__format_set(
  V4L2_Pixel_Format pixel_format,
  Unsigned format)
{
    pixel_format->pixelformat = format;
}

Integer
V4L2_Pixel_Format__height_get(
  V4L2_Pixel_Format pixel_format)
{
    return pixel_format->height;
}

void
V4L2_Pixel_Format__height_set(
  V4L2_Pixel_Format pixel_format,
  Integer height)
{
    pixel_format->height = height;
}

Integer
V4L2_Pixel_Format__width_get(
  V4L2_Pixel_Format pixel_format)
{
    return pixel_format->width;
}

void
V4L2_Pixel_Format__width_set(
  V4L2_Pixel_Format pixel_format,
  Integer width)
{
    pixel_format->width = width;
}

/* {V4L2_Rectangle} stuff: */

struct v4l2_rect V4L2_Rectangle__Initial;

V4L2_Rectangle V4L2_Rectangle__null = &V4L2_Rectangle__Initial;

void
V4L2_Rectangle__Initialize(void)
{
}

Integer
V4L2_Rectangle__height_get(
  V4L2_Rectangle rectangle)
{
    return rectangle->height;
}

void
V4L2_Rectangle__height_set(
  V4L2_Rectangle rectangle,
  Integer height)
{
    rectangle->height = height;
}

Integer
V4L2_Rectangle__left_get(
  V4L2_Rectangle rectangle)
{
    return rectangle->left;
}

void
V4L2_Rectangle__left_set(
  V4L2_Rectangle rectangle,
  Integer left)
{
    rectangle->left = left;
}

Integer
V4L2_Rectangle__top_get(
  V4L2_Rectangle rectangle)
{
    return rectangle->top;
}

void
V4L2_Rectangle__top_set(
  V4L2_Rectangle rectangle,
  Integer top)
{
    rectangle->top = top;
}

Integer
V4L2_Rectangle__width_get(
  V4L2_Rectangle rectangle)
{
    return rectangle->width;
}

void
V4L2_Rectangle__width_set(
  V4L2_Rectangle rectangle,
  Integer width)
{
    rectangle->width = width;
}


/* {V4L2_Request_Buffers} stuff: */

struct v4l2_requestbuffers V4L2_Request_Buffers__Initial;
V4L2_Request_Buffers V4L2_Request_Buffers__null =
  &V4L2_Request_Buffers__Initial;

void
V4L2_Request_Buffers__Initialize(void)
{
}

V4L2_Request_Buffers
V4L2_Request_Buffers__create(
  Unsigned count,
  V4L2_Buffer_Type type,
  V4L2_Memory memory)
{
    Unsigned malloc_bytes = sizeof *((V4L2_Request_Buffers)0);
    /* (void)printf("V4L2_Request_Bytes__new: malloc_bytes=%d\n",
        malloc_bytes); */

    V4L2_Request_Buffers request_buffers =
      (V4L2_Request_Buffers)malloc(malloc_bytes);
    (void)memset((void *)request_buffers, 0, malloc_bytes);

    request_buffers->count = count;
    request_buffers->type = type;
    request_buffers->memory = memory;

    return request_buffers;
}

Integer
V4L2_Request_Buffers__count_get(
  V4L2_Request_Buffers request_buffers)
{
    return request_buffers->count;
}

Integer
V4L2_Request_Buffers__request(
  V4L2_Request_Buffers request_buffers,
  Integer file_descriptor)
{
    Integer result;

    do {
	result =
	  ioctl(file_descriptor, VIDIOC_REQBUFS, (void *)request_buffers);
    } while (result == -1 && errno == EINTR);
    return result;
}

