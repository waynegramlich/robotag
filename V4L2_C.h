/*
 * Header for OpenCV.
 *
 * Copyright (c) 2010 by Wayne C. Gramlich
 * All rights reserved.
 */

#ifndef V4L2_C_H_INCLUDED
#define V4L2_C_H_INCLUDED 1

#include "linux/videodev2.h"

struct chunk {
  unsigned char *data;
};

typedef struct v4l2_buffer	*V4L2_Buffer;
typedef enum   v4l2_buf_type	 V4L2_Buffer_Type;
typedef struct v4l2_capability	*V4L2_Capability;
typedef struct chunk		*V4L2_Chunk;
typedef struct v4l2_crop	*V4L2_Crop;
typedef struct v4l2_cropcap	*V4L2_Crop_Capability;
typedef enum   v4l2_field	 V4L2_Field;
typedef struct v4l2_format	*V4L2_Format;
typedef enum   v4l2_memory	 V4L2_Memory;
typedef struct v4l2_pix_format	*V4L2_Pixel_Format;
typedef struct v4l2_rect	*V4L2_Rectangle;
typedef struct v4l2_requestbuffers *V4L2_Request_Buffers;

extern struct v4l2_buffer	V4L2_Buffer__Initial;
extern struct v4l2_capability	V4L2_Capability__Initial;
extern struct chunk		V4L2_Chunk__Initial;
extern struct v4l2_cropcap	V4L2_Crop_Capability__Initial;
extern struct v4l2_crop		V4L2_Crop__Initial;
extern struct v4l2_format	V4L2_Format__Initial;
extern struct v4l2_pix_format	V4L2_Pixel_Format__Initial;
extern struct v4l2_rect		V4L2_Rectangle__Initial;
extern struct v4l2_requestbuffers V4L2_Request_Buffers__Initial;

#endif /* V4L2_C_H_INCLUDED */
