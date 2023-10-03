import struct


def recv_int(sock) -> int:
    pack = sock.recv(4)
    pack_decoded = struct.unpack('!i', pack)[0]
    return pack_decoded


def send_int(sock, integer):
    len_pack = struct.pack('!i', integer)
    sock.send(len_pack)


def send_long(sock, long):
    len_pack = struct.pack('!Q', long)
    sock.send(len_pack)


def recv_str(sock) -> str:
    str_len = recv_int(sock)
    encoded_str = sock.recv(str_len)
    decoded_str = encoded_str.decode('utf-8')
    return decoded_str


def send_str(sock, string):
    send_int(sock, len(string))
    sock.send(string.encode('utf-8'))
