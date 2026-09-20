import struct

# 4-byte unsigned integer for the sequence number, big-endian
SEQ_FORMAT = "!I"
SEQ_SIZE = struct.calcsize(SEQ_FORMAT)

def pack_packet(seq_num: int, payload: bytes) -> bytes:
    """Prepend a sequence number to a payload."""
    return struct.pack(SEQ_FORMAT, seq_num) + payload

def unpack_packet(data: bytes) -> tuple[int, bytes]:
    """Split raw bytes back into (sequence_number, payload)."""
    seq_num = struct.unpack(SEQ_FORMAT, data[:SEQ_SIZE])[0]
    payload = data[SEQ_SIZE:]
    return seq_num, payload