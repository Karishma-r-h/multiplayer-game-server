import struct

# Header: 4-byte sequence number (unsigned int)
SEQ_FORMAT = "!I"
SEQ_SIZE = struct.calcsize(SEQ_FORMAT)

# Position payload: two 4-byte floats (x, y)
POS_FORMAT = "!ff"
POS_SIZE = struct.calcsize(POS_FORMAT)

def pack_packet(seq_num: int, payload: bytes) -> bytes:
    """Prepend a sequence number to a payload."""
    return struct.pack(SEQ_FORMAT, seq_num) + payload

def unpack_packet(data: bytes) -> tuple[int, bytes]:
    """Split raw bytes back into (sequence_number, payload)."""
    seq_num = struct.unpack(SEQ_FORMAT, data[:SEQ_SIZE])[0]
    payload = data[SEQ_SIZE:]
    return seq_num, payload

def pack_position(x: float, y: float) -> bytes:
    """Pack an (x, y) position into bytes."""
    return struct.pack(POS_FORMAT, x, y)

def unpack_position(payload: bytes) -> tuple[float, float]:
    """Unpack bytes back into an (x, y) position."""
    return struct.unpack(POS_FORMAT, payload)