# automatically generated by the FlatBuffers compiler, do not modify

# namespace: ppx

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Message(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsMessage(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Message()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def MessageBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x50\x50\x58\x46", size_prefixed=size_prefixed)

    # Message
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

    # Message
    def BodyType(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(4))
        if o != 0:
            return self._tab.Get(flatbuffers.number_types.Uint8Flags, o + self._tab.Pos)
        return 0

    # Message
    def Body(self):
        o = flatbuffers.number_types.UOffsetTFlags.py_type(self._tab.Offset(6))
        if o != 0:
            from flatbuffers.table import Table
            obj = Table(bytearray(), 0)
            self._tab.Union(obj, o)
            return obj
        return None

def MessageStart(builder): builder.StartObject(2)
def MessageAddBodyType(builder, bodyType): builder.PrependUint8Slot(0, bodyType, 0)
def MessageAddBody(builder, body): builder.PrependUOffsetTRelativeSlot(1, flatbuffers.number_types.UOffsetTFlags.py_type(body), 0)
def MessageEnd(builder): return builder.EndObject()
