# You can run this .tac file directly with:
#    twistd -ny -tcp-listener.tac

"""
This is a .tac file which starts a TCP listener and listens
for the noninstantaneous data suitable for archiving

The important part of this, the part that makes it a .tac file, is
the final root-level section, which sets up the object called 'application'
which twistd will look for
"""
import os
from twisted.application import service, internet
from twisted.web import static, server

from ceil.ceil_tcp_factory import ceilTCPFactory

def getceilTCPListenerService():
    """
    Return a service suitable for creating an application object.
    """
    tcp_port = 4002
    return internet.TCPServer(tcp_port, ceilTCPFactory())

# this is the core part of any tac file, the creation of the root-level
# application object
application = service.Application("Nevis TCP listener")

# attach the service to its parent application
service = getceilTCPListenerService()
service.setServiceParent(application)
