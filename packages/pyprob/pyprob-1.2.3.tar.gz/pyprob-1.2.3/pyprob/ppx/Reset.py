# automatically generated by the FlatBuffers compiler, do not modify

# namespace: ppx

import flatbuffers
from flatbuffers.compat import import_numpy
np = import_numpy()

class Reset(object):
    __slots__ = ['_tab']

    @classmethod
    def GetRootAsReset(cls, buf, offset):
        n = flatbuffers.encode.Get(flatbuffers.packer.uoffset, buf, offset)
        x = Reset()
        x.Init(buf, n + offset)
        return x

    @classmethod
    def ResetBufferHasIdentifier(cls, buf, offset, size_prefixed=False):
        return flatbuffers.util.BufferHasIdentifier(buf, offset, b"\x50\x50\x58\x46", size_prefixed=size_prefixed)

    # Reset
    def Init(self, buf, pos):
        self._tab = flatbuffers.table.Table(buf, pos)

def ResetStart(builder): builder.StartObject(0)
def ResetEnd(builder): return builder.EndObject()
