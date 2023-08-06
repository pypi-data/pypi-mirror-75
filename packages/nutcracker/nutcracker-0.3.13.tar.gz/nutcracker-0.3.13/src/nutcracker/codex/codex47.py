import io
import struct

from enum import Enum

from nutcracker.utils import funcutils
from . import bomb

glyph4_x = [
  0, 1, 2, 3, 3, 3, 3, 2, 1, 0, 0, 0, 1, 2, 2, 1,
]

glyph4_y = [
  0, 0, 0, 0, 1, 2, 3, 3, 3, 3, 2, 1, 1, 1, 2, 2,
]

glyph8_x = [
  0, 2, 5, 7, 7, 7, 7, 7, 7, 5, 2, 0, 0, 0, 0, 0,
]

glyph8_y = [
  0, 0, 0, 0, 1, 3, 4, 6, 7, 7, 7, 7, 6, 4, 3, 1,
]

motion_vectors = [
    (   0,   0 ), (  -1, -43 ), (   6, -43 ), (  -9, -42 ), (  13, -41 ),
    ( -16, -40 ), (  19, -39 ), ( -23, -36 ), (  26, -34 ), (  -2, -33 ),
    (   4, -33 ), ( -29, -32 ), (  -9, -32 ), (  11, -31 ), ( -16, -29 ),
    (  32, -29 ), (  18, -28 ), ( -34, -26 ), ( -22, -25 ), (  -1, -25 ),
    (   3, -25 ), (  -7, -24 ), (   8, -24 ), (  24, -23 ), (  36, -23 ),
    ( -12, -22 ), (  13, -21 ), ( -38, -20 ), (   0, -20 ), ( -27, -19 ),
    (  -4, -19 ), (   4, -19 ), ( -17, -18 ), (  -8, -17 ), (   8, -17 ),
    (  18, -17 ), (  28, -17 ), (  39, -17 ), ( -12, -15 ), (  12, -15 ),
    ( -21, -14 ), (  -1, -14 ), (   1, -14 ), ( -41, -13 ), (  -5, -13 ),
    (   5, -13 ), (  21, -13 ), ( -31, -12 ), ( -15, -11 ), (  -8, -11 ),
    (   8, -11 ), (  15, -11 ), (  -2, -10 ), (   1, -10 ), (  31, -10 ),
    ( -23,  -9 ), ( -11,  -9 ), (  -5,  -9 ), (   4,  -9 ), (  11,  -9 ),
    (  42,  -9 ), (   6,  -8 ), (  24,  -8 ), ( -18,  -7 ), (  -7,  -7 ),
    (  -3,  -7 ), (  -1,  -7 ), (   2,  -7 ), (  18,  -7 ), ( -43,  -6 ),
    ( -13,  -6 ), (  -4,  -6 ), (   4,  -6 ), (   8,  -6 ), ( -33,  -5 ),
    (  -9,  -5 ), (  -2,  -5 ), (   0,  -5 ), (   2,  -5 ), (   5,  -5 ),
    (  13,  -5 ), ( -25,  -4 ), (  -6,  -4 ), (  -3,  -4 ), (   3,  -4 ),
    (   9,  -4 ), ( -19,  -3 ), (  -7,  -3 ), (  -4,  -3 ), (  -2,  -3 ),
    (  -1,  -3 ), (   0,  -3 ), (   1,  -3 ), (   2,  -3 ), (   4,  -3 ),
    (   6,  -3 ), (  33,  -3 ), ( -14,  -2 ), ( -10,  -2 ), (  -5,  -2 ),
    (  -3,  -2 ), (  -2,  -2 ), (  -1,  -2 ), (   0,  -2 ), (   1,  -2 ),
    (   2,  -2 ), (   3,  -2 ), (   5,  -2 ), (   7,  -2 ), (  14,  -2 ),
    (  19,  -2 ), (  25,  -2 ), (  43,  -2 ), (  -7,  -1 ), (  -3,  -1 ),
    (  -2,  -1 ), (  -1,  -1 ), (   0,  -1 ), (   1,  -1 ), (   2,  -1 ),
    (   3,  -1 ), (  10,  -1 ), (  -5,   0 ), (  -3,   0 ), (  -2,   0 ),
    (  -1,   0 ), (   1,   0 ), (   2,   0 ), (   3,   0 ), (   5,   0 ),
    (   7,   0 ), ( -10,   1 ), (  -7,   1 ), (  -3,   1 ), (  -2,   1 ),
    (  -1,   1 ), (   0,   1 ), (   1,   1 ), (   2,   1 ), (   3,   1 ),
    ( -43,   2 ), ( -25,   2 ), ( -19,   2 ), ( -14,   2 ), (  -5,   2 ),
    (  -3,   2 ), (  -2,   2 ), (  -1,   2 ), (   0,   2 ), (   1,   2 ),
    (   2,   2 ), (   3,   2 ), (   5,   2 ), (   7,   2 ), (  10,   2 ),
    (  14,   2 ), ( -33,   3 ), (  -6,   3 ), (  -4,   3 ), (  -2,   3 ),
    (  -1,   3 ), (   0,   3 ), (   1,   3 ), (   2,   3 ), (   4,   3 ),
    (  19,   3 ), (  -9,   4 ), (  -3,   4 ), (   3,   4 ), (   7,   4 ),
    (  25,   4 ), ( -13,   5 ), (  -5,   5 ), (  -2,   5 ), (   0,   5 ),
    (   2,   5 ), (   5,   5 ), (   9,   5 ), (  33,   5 ), (  -8,   6 ),
    (  -4,   6 ), (   4,   6 ), (  13,   6 ), (  43,   6 ), ( -18,   7 ),
    (  -2,   7 ), (   0,   7 ), (   2,   7 ), (   7,   7 ), (  18,   7 ),
    ( -24,   8 ), (  -6,   8 ), ( -42,   9 ), ( -11,   9 ), (  -4,   9 ),
    (   5,   9 ), (  11,   9 ), (  23,   9 ), ( -31,  10 ), (  -1,  10 ),
    (   2,  10 ), ( -15,  11 ), (  -8,  11 ), (   8,  11 ), (  15,  11 ),
    (  31,  12 ), ( -21,  13 ), (  -5,  13 ), (   5,  13 ), (  41,  13 ),
    (  -1,  14 ), (   1,  14 ), (  21,  14 ), ( -12,  15 ), (  12,  15 ),
    ( -39,  17 ), ( -28,  17 ), ( -18,  17 ), (  -8,  17 ), (   8,  17 ),
    (  17,  18 ), (  -4,  19 ), (   0,  19 ), (   4,  19 ), (  27,  19 ),
    (  38,  20 ), ( -13,  21 ), (  12,  22 ), ( -36,  23 ), ( -24,  23 ),
    (  -8,  24 ), (   7,  24 ), (  -3,  25 ), (   1,  25 ), (  22,  25 ),
    (  34,  26 ), ( -18,  28 ), ( -32,  29 ), (  16,  29 ), ( -11,  31 ),
    (   9,  32 ), (  29,  32 ), (  -4,  33 ), (   2,  33 ), ( -26,  34 ),
    (  23,  36 ), ( -19,  39 ), (  16,  40 ), ( -13,  41 ), (   9,  42 ),
    (  -6,  43 ), (   1,  43 ), (   0,   0 ), (   0,   0 ), (   0,   0 ),
]

def read_le_uint16(f):
    bts = bytes(x % 256 for x in f[:2])
    return struct.unpack('<H', bts)[0]

def read_le_uint32(f):
    bts = bytes(x % 256 for x in f[:4])
    return struct.unpack('<I', bts)[0]

_width = None
_height = None

_frameSize = None
_deltaSize = None
_deltaBuf = None
_prev1 = None
_prev2 = None
_curBuf = None

_prev_seq = None

def cast_int16(x):
    x = x % (2 ** 16)
    return x - (x >> 15) * (2 ** 16)

def cast_int8(x):
    x = x % (2 ** 8)
    return x - (x >> 7) * (2 ** 8)

_p4x4glyphs = None
_p8x8glyphs = None

class GlyphEdge(Enum):
    LEFT_EDGE = 0
    TOP_EDGE = 1
    RIGHT_EDGE = 2
    BOTTOM_EDGE = 3
    NO_EDGE = 4

class GlyphDir(Enum):
    DIR_LEFT = 0
    DIR_UP = 1
    DIR_RIGHT = 2
    DIR_DOWN = 3
    NO_DIR = 4

def which_edge(x, y, edge_size):
    edge_max = edge_size - 1
    if not y:
        return GlyphEdge.BOTTOM_EDGE
    elif y == edge_max:
        return GlyphEdge.TOP_EDGE
    elif not x:
        return GlyphEdge.LEFT_EDGE
    elif x == edge_max:
        return GlyphEdge.RIGHT_EDGE
    else:
        return GlyphEdge.NO_EDGE

def which_direction(edge0, edge1):
    if any((
        (edge0 == GlyphEdge.LEFT_EDGE and edge1 == GlyphEdge.RIGHT_EDGE),
        (edge1 == GlyphEdge.LEFT_EDGE and edge0 == GlyphEdge.RIGHT_EDGE),
        (edge0 == GlyphEdge.BOTTOM_EDGE and edge1 != GlyphEdge.TOP_EDGE),
        (edge1 == GlyphEdge.BOTTOM_EDGE and edge0 != GlyphEdge.TOP_EDGE)
    )):
        return GlyphDir.DIR_UP
    elif any((
        (edge0 == GlyphEdge.TOP_EDGE and edge1 != GlyphEdge.BOTTOM_EDGE),
        (edge1 == GlyphEdge.TOP_EDGE and edge0 != GlyphEdge.BOTTOM_EDGE)
    )):
        return GlyphDir.DIR_DOWN
    elif any((
        (edge0 == GlyphEdge.LEFT_EDGE and edge1 != GlyphEdge.RIGHT_EDGE),
        (edge1 == GlyphEdge.LEFT_EDGE and edge0 != GlyphEdge.RIGHT_EDGE)
    )):
        return GlyphDir.DIR_LEFT
    elif any((
        (edge0 == GlyphEdge.TOP_EDGE and edge1 == GlyphEdge.BOTTOM_EDGE),
        (edge1 == GlyphEdge.TOP_EDGE and edge0 == GlyphEdge.BOTTOM_EDGE),
        (edge0 == GlyphEdge.RIGHT_EDGE and edge1 != GlyphEdge.LEFT_EDGE),
        (edge1 == GlyphEdge.RIGHT_EDGE and edge0 != GlyphEdge.LEFT_EDGE)
    )):
        return GlyphDir.DIR_RIGHT

    return GlyphDir.NO_DIR

def interp_point(x0, y0, x1, y1, pos, npoints):
    if not npoints:
        return x0, y0
    return (
        (x0 * pos + x1 * (npoints - pos) + (npoints >> 1)) // npoints,
        (y0 * pos + y1 * (npoints - pos) + (npoints >> 1)) // npoints
    )

def make_glyphs(xvec, yvec, side_length):
    glyph_size = side_length * side_length

    for x0, y0 in zip(xvec, yvec):
        edge0 = which_edge(x0, y0, side_length)

        for x1, y1 in zip(xvec, yvec):
            pglyph = [0 for _ in range(glyph_size)]
            edge1 = which_edge(x1, y1, side_length)
            dirr = which_direction(edge0, edge1)
            npoints = max(abs(x1 - x0), abs(y1 - y0))

            for ipoint in range(npoints + 1):
                point = interp_point(x0, y0, x1, y1, ipoint, npoints)
                if dirr == GlyphDir.DIR_UP:
                    for irow in range(point[1] + 1):
                        pglyph[point[0] + irow * side_length] = 1
                elif dirr == GlyphDir.DIR_DOWN:
                    for irow in range(point[1], side_length):
                        pglyph[point[0] + irow * side_length] = 1
                elif dirr == GlyphDir.DIR_LEFT:
                    for icol in range(point[0] + 1):
                        pglyph[icol + point[1] * side_length] = 1
                elif dirr == GlyphDir.DIR_RIGHT:
                    for icol in range(point[0], side_length):
                        pglyph[icol + point[1] * side_length] = 1

            yield pglyph

def init_codec47(width, height):
    global _width
    global _height

    global _frameSize
    global _deltaSize
    global _deltaBuf
    global _prev1
    global _prev2
    global _curBuf

    global _p4x4glyphs
    global _p8x8glyphs

    _width = width
    _height = height

    _p4x4glyphs = list(make_glyphs(glyph4_x, glyph4_y, 4))
    _p8x8glyphs = list(make_glyphs(glyph8_x, glyph8_y, 8))

    assert len(_p4x4glyphs) == len(_p8x8glyphs) == 256

    _frameSize = _width * _height
    _deltaSize = _frameSize * 3
    _deltaBuf = [0 for _ in range(_deltaSize)]
    _prev1, _prev2 = 0, _frameSize
    _curBuf = _frameSize * 2

def decode47(src, width, height):
    global _table
    global _prev_seq
    global _curBuf
    global _prev1
    global _prev2

    if not (_width, _height) == (width, height):
        print(f'init {width, height}')
        init_codec47(width, height)

    seq_nb = read_le_uint16(src)
    compression = src[2]
    rotation = src[3]
    skip = src[4]

    assert set(src[5:8]) == {0}, src[5:8]

    params = src[8:]
    bg1, bg2 = src[12:14]

    decoded_size = read_le_uint32(src[14:])
    assert decoded_size == _frameSize

    assert set(src[18:26]) == {0}, src[18:26]

    gfx_data = src[26:]
    if skip & 1:
        gfx_data = gfx_data[0x8080:]

    if seq_nb == 0:
        _deltaBuf[_prev1:_prev1 + _frameSize] = [bg1 for i in range(_frameSize)]
        _deltaBuf[_prev2:_prev2 + _frameSize] = [bg2 for i in range(_frameSize)]
        _prev_seq = -1

    out = _deltaBuf[_curBuf:_curBuf + _frameSize]

    print(f'COMPRESSION: {compression}')
    if compression == 0:
        out = gfx_data[:_frameSize]
        _deltaBuf[_curBuf:_curBuf + _frameSize] = out
    elif compression == 1:
        dst = 0
        d_src = 0
        for _ in range(0, height, 2):
            for i in range(0, width, 2):
                out[dst + i:dst + i + 2] = gfx_data[d_src:d_src + 2]
                out[dst + i + width:dst + i + width + 2] = gfx_data[d_src + 2:d_src + 4]
            dst += width * 2
        _deltaBuf[_curBuf:_curBuf + _frameSize] = out
    elif compression == 2:
        if seq_nb == _prev_seq + 1:
            out = decode2(out, gfx_data, width, height, params)
        _deltaBuf[_curBuf:_curBuf + _frameSize] = out
    elif compression == 3:
        out = _deltaBuf[_prev2:_prev2 + _frameSize]
        _deltaBuf[_curBuf:_curBuf + _frameSize] = out
    elif compression == 4:
        out = _deltaBuf[_prev1:_prev1 + _frameSize]
        _deltaBuf[_curBuf:_curBuf + _frameSize] = out
    elif compression == 5:
        out = bomb.decode_line(gfx_data, decoded_size)
        assert len(out) == _frameSize
        _deltaBuf[_curBuf:_curBuf + _frameSize] = out
    else:
        raise ValueError(f'Unknow compression: {compression}')

    if seq_nb == _prev_seq + 1 and rotation != 0:
        if rotation == 2:
            _prev1, _prev2 = _prev2, _prev1
        _curBuf, _prev2 = _prev2, _curBuf

    _prev_seq = seq_nb

    return [x for x in out]

def decode2(out, src, width, height, params):
    prev1 = _prev1
    prev2 = _prev2

    dst = 0

    with io.BytesIO(src) as stream:
        for _ in range(0, height, 8):
            for i in range(0, width, 8):
                process_block(out, stream, dst + i, prev1 + i, prev2 + i, width, params, 8)
            dst += width * 8
            prev1 += width * 8
            prev2 += width * 8

    return out[:_frameSize]

def process_block(out, stream, dst, prev1, prev2, stride, params, size):
    code = ord(stream.read(1))

    assert prev1 - _prev1 == prev2 - _prev2

    if code < 0xf8:
        mx, my = motion_vectors[code]
        for k in range(size):
            tmp = prev2 + mx + (my + k) * stride
            out[dst:dst + size] = _deltaBuf[tmp:tmp + size]
            dst += stride
    elif code == 0xff:
        if size == 2:
            out[dst:dst + 2] = [x for x in stream.read(2)]
            out[dst + stride:dst + stride + 2] = [x for x in stream.read(2)]
        else:
            size >>= 1
            process_block(out, stream, dst, prev1, prev2, stride, params, size)
            process_block(out, stream, dst + size, prev1 + size, prev2 + size, stride, params, size)
            dst += size * stride
            prev1 += size * stride
            prev2 += size * stride
            process_block(out, stream, dst, prev1, prev2, stride, params, size)
            process_block(out, stream, dst + size, prev1 + size, prev2 + size, stride, params, size)
    elif code == 0xfe:
        t = ord(stream.read(1))
        for _ in range(size):
            out[dst:dst + size] = [t] * size
            dst += stride
    elif code == 0xfd:
        assert size > 2
        code = ord(stream.read(1))
        pglyph = _p8x8glyphs[code] if size == 8 else _p4x4glyphs[code]
        colors = [x for x in stream.read(2)]
        glines = funcutils.grouper(pglyph, size)
        for k, gline in zip(range(size), glines):
            assert not (set(gline) - {0, 1})
            out[dst:dst + size] = [colors[1 - x] for x in gline]
            dst += stride
    elif code == 0xfc:
        off = prev1
        for _ in range(size):
            out[dst:dst + size] = _deltaBuf[off:off + size]
            dst += stride
            off += stride
    else:
        t = params[code & 7]
        for _ in range(size):
            out[dst:dst + size] = [t] * size
            dst += stride


def fake_encode47(out, bg1=b'\0', bg2=b'\0'):
    # from . import codex47_np as cdx

    width = len(out[0])
    height = len(out)
    print(width, height)

    seq_nb = b'\0\0'
    compression = b'\0'
    rotation = b'\0'
    skip = b'\0'
    _dummy = b'\0\0\0'
    params = b'\0\0\0\0'
    bg1 = bg1
    bg2 = bg2

    decoded_size = struct.pack('<I', width * height)

    _dummy2 = b'\0' * 8

    return seq_nb + compression + rotation + skip + _dummy + params + bg1 + bg2 + decoded_size + _dummy2 + b''.join(out)
