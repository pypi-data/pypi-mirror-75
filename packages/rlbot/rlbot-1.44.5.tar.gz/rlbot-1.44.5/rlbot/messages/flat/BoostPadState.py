# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers

class BoostPadState(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsBoostPadState(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = BoostPadState()
        x.Init(buf, n + offset)
        return x

    # BoostPadState
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

# /// True if the boost can be picked up
    # BoostPadState
    def IsActive(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.BoolFlags, o + self._tab.Pos)
        return 0

# /// The number of seconds since the boost has been picked up, or 0.0 if the boost is active.
    # BoostPadState
    def Timer(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Float32Flags, o + self._tab.Pos)
        return 0.0

def BoostPadStateStart(builder): builder.StartObject(2)
def BoostPadStateAddIsActive(builder, isActive): builder.PrependBoolSlot(0, isActive, 0)
def BoostPadStateAddTimer(builder, timer): builder.PrependFloat32Slot(1, timer, 0.0)
def BoostPadStateEnd(builder): return builder.EndObject()
