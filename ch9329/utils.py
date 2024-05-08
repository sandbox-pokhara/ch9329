from __future__ import annotations


def get_packet(
    head: bytes, addr: bytes, cmd: bytes, length: bytes, data: bytes
):
    head_hex_list = list(head)
    head_hex_sum = sum(head_hex_list)
    data_hex_list = list(data)
    data_hex_sum = sum(data_hex_list)

    checksum = (
        sum(
            [
                head_hex_sum,
                int.from_bytes(addr, byteorder="big"),
                int.from_bytes(cmd, byteorder="big"),
                int.from_bytes(length, byteorder="big"),
                data_hex_sum,
            ]
        )
        # we need to mask the last 8-bit
        # insted of doing modulo operation
        # you can run below demo to see how
        # %255 and &255 are different
        & 0xFF
    )
    packet = head + addr + cmd + length + data + bytes([checksum])
    return packet


# for demo purpose
if __name__ == "__main__":
    for i in range(1, 0xFFFF):
        if i % 255 != i & 0xFF:
            print(
                f"Original sum [{i}] | after mod [{i%255}] | after masking [{i&0xff}]"
            )
