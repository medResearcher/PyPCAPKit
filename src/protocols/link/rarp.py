# -*- coding: utf-8 -*-
"""(dynamic) reverse address resolution protocol

``jspcap.protocols.link.rarp`` contains ``RARP`` only,
which implements extractor for (Dynamic) Reverse Address
Resolution Protocol (RARP/DRARP), whose structure is
described as below.

    Octets          Bits          Name                Discription
      0              0          rarp.htype        Hardware Type
      2              16         rarp.ptype        Protocol Type
      4              32         rarp.hlen         Hardware Address Length
      5              40         rarp.plen         Protocol Address Length
      6              48         rarp.oper         Operation
      8              64         rarp.sha          Sender Hardware Address
      14             112        rarp.spa          Sender Protocol Address
      18             144        rarp.tha          Target Hardware Address
      24             192        rarp.tpa          Target Protocol Address

"""
# Reverse Address Resolution Protocol
# Analyser for RARP/DRARP header


from jspcap.protocols.link.arp import ARP


__all__ = ['RARP']


class RARP(ARP):
    """This class implements Reverse Address Resolution Protocol.

    Properties:
        * name -- str, name of corresponding procotol
        * info -- Info, info dict of current instance
        * layer -- str, `Link`
        * length -- int, header length of corresponding protocol
        * protochain -- ProtoChain, protocol chain of current instance
        * src -- tuple(str, str), sender hardware & protocol address
        * dst -- tuple(str, str), target hardware & protocol address
        * type -- tuple(str, str), hardware & protocol type

   Methods:
       * read_arp -- read Address Resolution Protocol

    Attributes:
        * _file -- BytesIO, bytes to be extracted
        * _info -- Info, info dict of current instance
        * _protos -- ProtoChain, protocol chain of current instance

    Utilities:
        * _read_protos -- read next layer protocol type
        * _read_fileng -- read file buffer
        * _read_unpack -- read bytes and unpack to integers
        * _read_binary -- read bytes and convert into binaries
        * _decode_next_layer -- decode next layer protocol type
        * _import_next_layer -- import next layer protocol extractor
        * _read_addr_resolve -- resolve MAC address according to protocol
        * _read_proto_resolve -- solve IP address according to protocol

    """
    _name = 'Reverse Address Resolution Protocol'
