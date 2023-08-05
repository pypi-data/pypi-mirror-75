import socket as s

def jpysocket():
    jpysoc = s.socket()
    return jpysoc
def jpyencode(msg):
    msg = (chr(92) + "x00" + chr(92) + "x" + format(len(msg), '02x') + msg).encode().decode('unicode-escape').encode()
    return msg
def jpydecode(msg):
        msg=str(msg.decode()[2:])
        return msg
