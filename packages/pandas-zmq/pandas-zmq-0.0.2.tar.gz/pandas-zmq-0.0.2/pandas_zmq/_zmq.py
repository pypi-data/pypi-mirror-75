
import zlib
import pickle
import hashlib
from zmq import *


def send_dataframe(socket, obj, secret='', flags=0, alg='sha256'):
    """send pandas dataframe***"""

    p = pickle.dumps(obj, -1)
    a = hashlib.new(alg)
    a.update(secret.encode() + p)
    h = a.hexdigest().upper()
    z = zlib.compress(h.encode() + b'\n' + p)
    return socket.send(z, flags=flags)


def recv_dataframe(socket, secret='', flags=0, alg='sha256'):
    """receive pandas dataframe***"""
    z = socket.recv(flags)
    s = zlib.decompress(z)
    h = s[:s.find(b'\n')]
    p = s[(s.find(b'\n')+1):]
    a = hashlib.new(alg)
    a.update(secret.encode() + p)

    if a.hexdigest().upper() != h.decode():
        raise Exception("Signature mismatch")

    return pickle.loads(p)
