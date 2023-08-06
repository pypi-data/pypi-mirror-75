import sys
import numpy as np
import pandas as pd
import flatbuffers
from flatmake.idl.python.Dim import UByteArray
from flatmake.idl.python.Dim import Float32bArray
from flatmake.idl.python.Dim import UInt32bArray
from flatmake.idl.python.Dim import LabeledIndexSet
from flatmake.idl.python.Dim import LabeledIndexSuperSet
from flatmake.idl.python.Dim import Coordinates2D
from flatmake.idl.python.Dim import ColorArray1D
from flatmake.idl.python.Dim import RGBTripleArray


def add_ubyte_array(builder, np_arr):
    arr = builder.CreateNumpyVector(x=np_arr)
    UByteArray.UByteArrayStart(builder)
    UByteArray.UByteArrayAddData(builder=builder, data=arr)
    return UByteArray.UByteArrayEnd(builder)


def add_float32_array(builder, np_arr):
    arr = builder.CreateNumpyVector(x=np_arr.astype(np.float32))
    Float32bArray.Float32bArrayStart(builder)
    Float32bArray.Float32bArrayAddData(builder=builder, data=arr)
    return Float32bArray.Float32bArrayEnd(builder)


def add_uint32_array(builder, np_arr):
    arr = builder.CreateNumpyVector(x=np_arr.astype(np.uint32))
    UInt32bArray.UInt32bArrayStart(builder)
    UInt32bArray.UInt32bArrayAddData(builder=builder, data=arr)
    return UInt32bArray.UInt32bArrayEnd(builder)


def build_float32_array(np_arr):
    builder = flatbuffers.Builder(0)
    arr = builder.CreateNumpyVector(np_arr)
    Float32bArray.Float32bArrayStart(builder)
    Float32bArray.Float32bArrayAddData(builder=builder, data=arr)
    float32_array = Float32bArray.Float32bArrayEnd(builder)
    builder.Finish(float32_array)
    return builder


def serialize_float32_array(np_arr, verbose=False):
    try:
        builder = build_float32_array(
            np_arr=np_arr
        )
        buf = bytes(builder.Output())
    except Exception as e:
        raise Exception(e)

    if verbose is True:
        print(f"Size: {str(sys.getsizeof(buf))} bytes")

    return buf


def add_labeled_index_set(builder, name, np_arr):

    if not isinstance(name, int) and not isinstance(name, str):
        raise Exception(f"Serializing a LabeledIndexSet labeled with a {type(name)} is not supported.")
    fb_index_set_name = builder.CreateString(s=str(object=name))
    fb_uint32_arr = add_uint32_array(
        builder=builder,
        np_arr=np_arr
    )
    LabeledIndexSet.LabeledIndexSetStart(builder=builder)
    LabeledIndexSet.LabeledIndexSetAddName(builder=builder, name=fb_index_set_name)
    LabeledIndexSet.LabeledIndexSetAddIndices(builder=builder, indices=fb_uint32_arr)
    return LabeledIndexSet.LabeledIndexSetEnd(builder=builder)


def build_labeled_index_set(name, np_arr):
    builder = flatbuffers.Builder(0)
    fb_labeled_index_set = add_labeled_index_set(
        builder=builder,
        name=name,
        np_arr=np_arr
    )
    builder.Finish(fb_labeled_index_set)
    return builder


def serialize_labeled_index_set(name, np_arr, verbose=False):
    try:
        builder = build_labeled_index_set(
            name=name,
            np_arr=np_arr
        )
        buf = bytes(builder.Output())
    except Exception as e:
        raise Exception(e)

    if verbose is True:
        print(f"Size: {str(sys.getsizeof(buf))} bytes")

    return buf


def build_labeled_index_super_set(name, np_arr, verbose=False):
    # Source: https://google.github.io/flatbuffers/md__java_usage.html
    # Everything else (other tables, strings, vectors) MUST be created before the start of the table they are referenced in.
    builder = flatbuffers.Builder(0)
    fb_super_set_name = builder.CreateString(s=name)
    df = pd.DataFrame({"set": np_arr})
    groups = df.groupby("set")
    num_groups = len(groups)
    fb_labeled_index_sets = []
    for group_name, group in groups:
        fb_labeled_index_set = add_labeled_index_set(
            builder=builder,
            name=group_name,
            np_arr=group.index.values
        )
        fb_labeled_index_sets.append(fb_labeled_index_set)
    LabeledIndexSuperSet.LabeledIndexSuperSetStartSetsVector(builder=builder, numElems=num_groups)
    for i in range(num_groups):
        builder.PrependUOffsetTRelative(fb_labeled_index_sets[i])
    fb_sets = builder.EndVector(num_groups)
    LabeledIndexSuperSet.LabeledIndexSuperSetStart(builder=builder)
    LabeledIndexSuperSet.LabeledIndexSuperSetAddName(builder=builder, name=fb_super_set_name)
    LabeledIndexSuperSet.LabeledIndexSuperSetAddSets(builder=builder, sets=fb_sets)
    fb_labeled_index_super_set = LabeledIndexSuperSet.LabeledIndexSuperSetEnd(builder=builder)
    builder.Finish(fb_labeled_index_super_set)
    return builder


def serialize_labeled_index_super_set(name, np_arr, verbose=False):
    try:
        builder = build_labeled_index_super_set(
            name=name,
            np_arr=np_arr
        )
        buf = bytes(builder.Output())
    except Exception as e:
        print(e)

    if verbose is True:
        print(f"Size: {str(sys.getsizeof(buf))} bytes")

    return buf


def build_coordinates_2d(np_x, np_y):
    builder = flatbuffers.Builder(0)
    fb_x = add_float32_array(
        builder=builder,
        np_arr=np_x
    )
    fb_y = add_float32_array(
        builder=builder,
        np_arr=np_y
    )
    Coordinates2D.Coordinates2DStart(builder)
    Coordinates2D.Coordinates2DAddX(builder=builder, x=fb_x)
    Coordinates2D.Coordinates2DAddY(builder=builder, y=fb_y)
    coordinates_2d = Coordinates2D.Coordinates2DEnd(builder)
    builder.Finish(coordinates_2d)
    return builder


def serialize_coordinates_2d(np_x, np_y, verbose=False):
    try:
        builder = build_coordinates_2d(
            np_x=np_x,
            np_y=np_y
        )
        buf = bytes(builder.Output())
    except Exception as e:
        print(e)

    if verbose is True:
        print(f"Size: {str(sys.getsizeof(buf))} bytes")

    return buf


def normalize_to_rgb(np_arr):
    return np.interp(
        np_arr,
        (np_arr.min(), np_arr.max()),
        (0, 255)
    ).astype(np.uint8)


def build_rgb_triple_array(np_r, np_g, np_b):
    try:
        builder = flatbuffers.Builder(0)
        fb_r = add_ubyte_array(
            builder=builder,
            np_arr=normalize_to_rgb(
                np_arr=np_r
            )
        )
        fb_g = add_ubyte_array(
            builder=builder,
            np_arr=normalize_to_rgb(
                np_arr=np_r
            )
        )
        fb_b = add_ubyte_array(
            builder=builder,
            np_arr=normalize_to_rgb(
                np_arr=np_r
            )
        )
        RGBTripleArray.RGBTripleArrayStart(builder)
        RGBTripleArray.RGBTripleArrayAddR(builder=builder, r=fb_r)
        RGBTripleArray.RGBTripleArrayAddG(builder=builder, g=fb_g)
        RGBTripleArray.RGBTripleArrayAddB(builder=builder, b=fb_b)
        rgb_triple_array = RGBTripleArray.RGBTripleArrayEnd(builder)
        builder.Finish(rgb_triple_array)
        return builder
    except Exception as e:
        raise Exception(e)


def serialize_rgb_triple_array(np_red, np_green, np_blue, verbose=False):
    try:
        builder = build_rgb_triple_array(
            np_r=np_red,
            np_g=np_green,
            np_b=np_blue
        )
        buf = bytes(builder.Output())
    except Exception as e:
        raise Exception(e)

    if verbose is True:
        print(f"Size: {str(sys.getsizeof(buf))} bytes")

    return buf


def build_color_array(np_arr):
    try:
        builder = flatbuffers.Builder(0)
        fb_arr = add_ubyte_array(
            builder=builder,
            np_arr=normalize_to_rgb(
                np_arr=np_arr
            )
        )
        ColorArray1D.ColorArray1DStart(builder)
        ColorArray1D.ColorArray1DAddColor(builder=builder, color=fb_arr)
        color_array_1d = ColorArray1D.ColorArray1DEnd(builder)
        builder.Finish(color_array_1d)
        return builder
    except Exception as e:
        raise Exception(e)


def serialize_color_array(np_arr, verbose=False):
    try:
        builder = build_color_array(
            np_arr=np_arr
        )
        buf = bytes(builder.Output())
    except Exception as e:
        raise Exception(e)

    if verbose is True:
        print(f"Size: {str(sys.getsizeof(buf))} bytes")

    return buf
