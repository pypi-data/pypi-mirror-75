/*
 * Copyright (c) 2020 Qianqian Fang <q.fang at neu.edu>. All rights reserved.
 * Copyright (c) 2001-2016 Python Software Foundation; All Rights Reserved
 *
 * Licensed under PSF license, see: https://docs.python.org/3/license.html
 *
 * Herein are a selection of functions which are not part of Python's public
 * C-API, including some from floatobject.c
 */

#include <Python.h>

#include <ctype.h>
#include <float.h>

/******************************************************************************/

/* this is for the benefit of the pack/unpack routines below */

typedef enum {
    unknown_format, ieee_big_endian_format, ieee_little_endian_format
} float_format_type;

static float_format_type double_format, float_format;


/* MUST be called before using floating point related functions defined below */
void _pyfuncs_ubj_detect_formats(void) {
    float_format_type detected_double_format, detected_float_format;

/* We attempt to determine if this machine is using IEEE
   floating point formats by peering at the bits of some
   carefully chosen values.  If it looks like we are on an
   IEEE platform, the float packing/unpacking routines can
   just copy bits, if not they resort to arithmetic & shifts
   and masks.  The shifts & masks approach works on all finite
   values, but what happens to infinities, NaNs and signed
   zeroes on packing is an accident, and attempting to unpack
   a NaN or an infinity will raise an exception.
   Note that if we're on some whacked-out platform which uses
   IEEE formats but isn't strictly little-endian or big-
   endian, we will fall back to the portable shifts & masks
   method. */

#if SIZEOF_DOUBLE == 8
    {
        double x = 9006104071832581.0;
        if (memcmp(&x, "\x43\x3f\xff\x01\x02\x03\x04\x05", 8) == 0)
            detected_double_format = ieee_big_endian_format;
        else if (memcmp(&x, "\x05\x04\x03\x02\x01\xff\x3f\x43", 8) == 0)
            detected_double_format = ieee_little_endian_format;
        else
            detected_double_format = unknown_format;
    }
#else
    detected_double_format = unknown_format;
#endif

#if SIZEOF_FLOAT == 4
    {
        float y = 16711938.0;
        if (memcmp(&y, "\x4b\x7f\x01\x02", 4) == 0)
            detected_float_format = ieee_big_endian_format;
        else if (memcmp(&y, "\x02\x01\x7f\x4b", 4) == 0)
            detected_float_format = ieee_little_endian_format;
        else
            detected_float_format = unknown_format;
    }
#else
    detected_float_format = unknown_format;
#endif

    double_format = detected_double_format;
    float_format = detected_float_format;
}

/******************************************************************************/

int
_pyfuncs_ubj_PyFloat_Pack4(double x, unsigned char *p, int le)
{
    if (float_format == unknown_format) {
        unsigned char sign;
        int e;
        double f;
        unsigned int fbits;
        int incr = 1;

        if (le) {
            p += 3;
            incr = -1;
        }

        if (x < 0) {
            sign = 1;
            x = -x;
        }
        else
            sign = 0;

        f = frexp(x, &e);

        /* Normalize f to be in the range [1.0, 2.0) */
        if (0.5 <= f && f < 1.0) {
            f *= 2.0;
            e--;
        }
        else if (f == 0.0)
            e = 0;
        else {
            PyErr_SetString(PyExc_SystemError,
                            "frexp() result out of range");
            return -1;
        }

        if (e >= 128)
            goto Overflow;
        else if (e < -126) {
            /* Gradual underflow */
            f = ldexp(f, 126 + e);
            e = 0;
        }
        else if (!(e == 0 && f == 0.0)) {
            e += 127;
            f -= 1.0; /* Get rid of leading 1 */
        }

        f *= 8388608.0; /* 2**23 */
        fbits = (unsigned int)(f + 0.5); /* Round */
        assert(fbits <= 8388608);
        if (fbits >> 23) {
            /* The carry propagated out of a string of 23 1 bits. */
            fbits = 0;
            ++e;
            if (e >= 255)
                goto Overflow;
        }

        /* First byte */
        *p = (sign << 7) | (e >> 1);
        p += incr;

        /* Second byte */
        *p = (char) (((e & 1) << 7) | (fbits >> 16));
        p += incr;

        /* Third byte */
        *p = (fbits >> 8) & 0xFF;
        p += incr;

        /* Fourth byte */
        *p = fbits & 0xFF;

        /* Done */
        return 0;

    }
    else {
        float y = (float)x;
        const unsigned char *s = (unsigned char*)&y;
        int i, incr = 1;

        if (Py_IS_INFINITY(y) && !Py_IS_INFINITY(x))
            goto Overflow;

        if ((float_format == ieee_little_endian_format && !le)
            || (float_format == ieee_big_endian_format && le)) {
            p += 3;
            incr = -1;
        }

        for (i = 0; i < 4; i++) {
            *p = *s++;
            p += incr;
        }
        return 0;
    }
  Overflow:
    PyErr_SetString(PyExc_OverflowError,
                    "float too large to pack with f format");
    return -1;
}

int
_pyfuncs_ubj_PyFloat_Pack8(double x, unsigned char *p, int le)
{
    if (double_format == unknown_format) {
        unsigned char sign;
        int e;
        double f;
        unsigned int fhi, flo;
        int incr = 1;

        if (le) {
            p += 7;
            incr = -1;
        }

        if (x < 0) {
            sign = 1;
            x = -x;
        }
        else
            sign = 0;

        f = frexp(x, &e);

        /* Normalize f to be in the range [1.0, 2.0) */
        if (0.5 <= f && f < 1.0) {
            f *= 2.0;
            e--;
        }
        else if (f == 0.0)
            e = 0;
        else {
            PyErr_SetString(PyExc_SystemError,
                            "frexp() result out of range");
            return -1;
        }

        if (e >= 1024)
            goto Overflow;
        else if (e < -1022) {
            /* Gradual underflow */
            f = ldexp(f, 1022 + e);
            e = 0;
        }
        else if (!(e == 0 && f == 0.0)) {
            e += 1023;
            f -= 1.0; /* Get rid of leading 1 */
        }

        /* fhi receives the high 28 bits; flo the low 24 bits (== 52 bits) */
        f *= 268435456.0; /* 2**28 */
        fhi = (unsigned int)f; /* Truncate */
        assert(fhi < 268435456);

        f -= (double)fhi;
        f *= 16777216.0; /* 2**24 */
        flo = (unsigned int)(f + 0.5); /* Round */
        assert(flo <= 16777216);
        if (flo >> 24) {
            /* The carry propagated out of a string of 24 1 bits. */
            flo = 0;
            ++fhi;
            if (fhi >> 28) {
                /* And it also progagated out of the next 28 bits. */
                fhi = 0;
                ++e;
                if (e >= 2047)
                    goto Overflow;
            }
        }

        /* First byte */
        *p = (sign << 7) | (e >> 4);
        p += incr;

        /* Second byte */
        *p = (unsigned char) (((e & 0xF) << 4) | (fhi >> 24));
        p += incr;

        /* Third byte */
        *p = (fhi >> 16) & 0xFF;
        p += incr;

        /* Fourth byte */
        *p = (fhi >> 8) & 0xFF;
        p += incr;

        /* Fifth byte */
        *p = fhi & 0xFF;
        p += incr;

        /* Sixth byte */
        *p = (flo >> 16) & 0xFF;
        p += incr;

        /* Seventh byte */
        *p = (flo >> 8) & 0xFF;
        p += incr;

        /* Eighth byte */
        *p = flo & 0xFF;
        /* p += incr; */

        /* Done */
        return 0;

      Overflow:
        PyErr_SetString(PyExc_OverflowError,
                        "float too large to pack with d format");
        return -1;
    }
    else {
        const unsigned char *s = (unsigned char*)&x;
        int i, incr = 1;

        if ((double_format == ieee_little_endian_format && !le)
            || (double_format == ieee_big_endian_format && le)) {
            p += 7;
            incr = -1;
        }

        for (i = 0; i < 8; i++) {
            *p = *s++;
            p += incr;
        }
        return 0;
    }
}

/******************************************************************************/

double
_pyfuncs_ubj_PyFloat_Unpack4(const unsigned char *p, int le)
{
    if (float_format == unknown_format) {
        unsigned char sign;
        int e;
        unsigned int f;
        double x;
        int incr = 1;

        if (le) {
            p += 3;
            incr = -1;
        }

        /* First byte */
        sign = (*p >> 7) & 1;
        e = (*p & 0x7F) << 1;
        p += incr;

        /* Second byte */
        e |= (*p >> 7) & 1;
        f = (*p & 0x7F) << 16;
        p += incr;

        if (e == 255) {
            PyErr_SetString(
                PyExc_ValueError,
                "can't unpack IEEE 754 special value "
                "on non-IEEE platform");
            return -1;
        }

        /* Third byte */
        f |= *p << 8;
        p += incr;

        /* Fourth byte */
        f |= *p;

        x = (double)f / 8388608.0;

        /* XXX This sadly ignores Inf/NaN issues */
        if (e == 0)
            e = -126;
        else {
            x += 1.0;
            e -= 127;
        }
        x = ldexp(x, e);

        if (sign)
            x = -x;

        return x;
    }
    else {
        float x;

        if ((float_format == ieee_little_endian_format && !le)
            || (float_format == ieee_big_endian_format && le)) {
            char buf[4];
            char *d = &buf[3];
            int i;

            for (i = 0; i < 4; i++) {
                *d-- = *p++;
            }
            memcpy(&x, buf, 4);
        }
        else {
            memcpy(&x, p, 4);
        }

        return x;
    }
}

double
_pyfuncs_ubj_PyFloat_Unpack8(const unsigned char *p, int le)
{
    if (double_format == unknown_format) {
        unsigned char sign;
        int e;
        unsigned int fhi, flo;
        double x;
        int incr = 1;

        if (le) {
            p += 7;
            incr = -1;
        }

        /* First byte */
        sign = (*p >> 7) & 1;
        e = (*p & 0x7F) << 4;

        p += incr;

        /* Second byte */
        e |= (*p >> 4) & 0xF;
        fhi = (*p & 0xF) << 24;
        p += incr;

        if (e == 2047) {
            PyErr_SetString(
                PyExc_ValueError,
                "can't unpack IEEE 754 special value "
                "on non-IEEE platform");
            return -1.0;
        }

        /* Third byte */
        fhi |= *p << 16;
        p += incr;

        /* Fourth byte */
        fhi |= *p  << 8;
        p += incr;

        /* Fifth byte */
        fhi |= *p;
        p += incr;

        /* Sixth byte */
        flo = *p << 16;
        p += incr;

        /* Seventh byte */
        flo |= *p << 8;
        p += incr;

        /* Eighth byte */
        flo |= *p;

        x = (double)fhi + (double)flo / 16777216.0; /* 2**24 */
        x /= 268435456.0; /* 2**28 */

        if (e == 0)
            e = -1022;
        else {
            x += 1.0;
            e -= 1023;
        }
        x = ldexp(x, e);

        if (sign)
            x = -x;

        return x;
    }
    else {
        double x;

        if ((double_format == ieee_little_endian_format && !le)
            || (double_format == ieee_big_endian_format && le)) {
            char buf[8];
            char *d = &buf[7];
            int i;

            for (i = 0; i < 8; i++) {
                *d-- = *p++;
            }
            memcpy(&x, buf, 8);
        }
        else {
            memcpy(&x, p, 8);
        }

        return x;
    }
}
