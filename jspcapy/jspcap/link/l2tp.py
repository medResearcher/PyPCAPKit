#!/usr/bin/python3
# -*- coding: utf-8 -*-


# Layer Two Tunneling Protocol
# Analyser for L2TP header


from .link import Link
from ..protocols import Info


class L2TP(Link):

    __all__ = ['name', 'info', 'length', 'src', 'dst', 'layer', 'protocol']

    ##########################################################################
    # Properties.
    ##########################################################################

    @property
    def name(self):
        return 'Layer 2 Tunneling Protocol'

    @property
    def info(self):
        return self._info

    @property
    def length(self):
        return self._info.len

    @property
    def src(self):
        return (self._info.sha, self._info.spa)

    @property
    def dst(self):
        return (self._info.tha, self._info.tpa)

    @property
    def layer(self):
        return self.__layer__

    @property
    def protocol(self):
        return (self._info.htype, self._info.ptype)

    ##########################################################################
    # Data models.
    ##########################################################################

    def __init__(self, _file):
        self._file = _file
        self._info = Info(self.read_l2tp())

    def __len__(self):
        return self._info.len

    def __length_hint__(self):
        return 16

    ##########################################################################
    # Utilities.
    ##########################################################################

    def read_l2tp(self):
        """Read Layer Two Tunneling Protocol.

        Structure of L2TP header [RFC 2661]:

            0                   1                   2                   3
            0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |T|L|x|x|S|x|O|P|x|x|x|x|  Ver  |          Length (opt)         |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |           Tunnel ID           |           Session ID          |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |             Ns (opt)          |             Nr (opt)          |
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
           |      Offset Size (opt)        |    Offset pad... (opt)
           +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

            Octets          Bits          Name                Discription
              0              0          l2tp.flags        Flags and Version Info
              0              0          l2tp.flags.type   Type (0/1)
              0              1          l2tp.flags.len    Length
              0              2          l2tp.flags.res    Reserved (must be zero)
              0              4          l2tp.flags.seq    Sequence
              0              5          l2tp.flags.x      Reserved (must be zero)
              0              6          l2tp.flags.offset Offset
              0              7          l2tp.flags.prio   Priority
              1              8          l2tp.resv         Reserved (must be zero)
              1              12         l2tp.ver          Version (2)
              2              16         l2tp.length       Length (optional by len)
              4              32         l2tp.tunnelid     Tunnel ID
              6              48         l2tp.sessionid    Session ID
              8              64         l2tp.ns           Sequence Number (optional by seq)
              10             80         l2tp.nr           Next Sequence Number (optional by seq)
              12             96         l2tp.offset       Offset Size (optional by offset)

        """
        _flag = self._read_binary(1)
        _vers = self._read_fileng(1).hex()[1]
        _hlen = self._read_unpack(2) if int(_flag[1]) else None
        _tnnl = self._read_unpack(2)
        _sssn = self._read_unpack(2)
        _nseq = self._read_unpack(2) if int(_flag[4]) else None
        _nrec = self._read_unpack(2) if int(_flag[4]) else None
        _size = self._read_unpack(2) if int(_flag[6]) else None

        l2tp = dict(
            flags = dict(
                type = 'control' if int(_flag[0]) else 'data',
                len = True if int(_flag[1]) else False,
                res = b'\x00\x00',
                seq = True if int(_flag[4]) else False,
                x = b'\x00',
                offset = True if int(_flag[6]) else False,
                prio = True if int(_flag[7]) else False,
            ),
            resv = b'\x00' * 4,
            ver = int(_vers, base=16),
            length = _hlen,
            tunnelid = _tnnl,
            sessionid = _sssn,
            ns = _nseq,
            nr = _nrec,
            offset = _size * 8,
        )

        l2tp['len'] = _hlen or (6 + 2*(int(_flag[1]) + 2*int(_flag[4]) + int(_flag[6])))
        if _size:
            l2tp['padding'] = self._read_fileng(_size * 8)
            l2tp['len'] += _size * 8

        return l2tp
