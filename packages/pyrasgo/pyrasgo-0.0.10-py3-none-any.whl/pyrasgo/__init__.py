
# if somebody does "from somepackage import *", this is what they will
# be able to access:
__all__ = [
    'connect',
]


from pyrasgo.connection import RasgoConnection

def connect(api_key):
    conn = RasgoConnection(api_key)
    return conn

