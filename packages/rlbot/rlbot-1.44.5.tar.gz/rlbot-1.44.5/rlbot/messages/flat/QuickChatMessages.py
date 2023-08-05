# automatically generated by the FlatBuffers compiler, do not modify

# namespace: flat

import flatbuffers

class QuickChatMessages(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsQuickChatMessages(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = QuickChatMessages()
        x.Init(buf, n + offset)
        return x

    # QuickChatMessages
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # QuickChatMessages
    def Messages(self, j):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            x = self._tab.Vector(o)
            x += flatbuffers.number_types.UOffsetTFlags.py_type(j) * 4
            x = self._tab.Indirect(x)
            from .QuickChat import QuickChat
            obj = QuickChat()
            obj.Init(self._tab.Bytes, x)
            return obj
        return None

    # QuickChatMessages
    def MessagesLength(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.VectorLen(o)
        return 0

def QuickChatMessagesStart(builder): builder.StartObject(1)
def QuickChatMessagesAddMessages(builder, messages): builder.PrependUOffsetTRelativeSlot(0, flatbuffers.number_types.UOffsetTFlags.py_type(messages), 0)
def QuickChatMessagesStartMessagesVector(builder, numElems): return builder.StartVector(4, numElems, 4)
def QuickChatMessagesEnd(builder): return builder.EndObject()
