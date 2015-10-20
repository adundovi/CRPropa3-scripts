import zmq

from crpropa import Module

class SendCandidateProperties( Module ):
    """ Sends candidate proporties given by the function
        ```extract_func( candidate )``` over the network
        to the server on ```ip_port```
    """
    def __init__( self, ip_port, extract_func ):
        Module.__init__( self )
        self.ip_port = "tcp://" + ip_port
        self.extract_func = extract_func

    def beginRun( self ):
        context = zmq.Context()
        self.socket = context.socket( zmq.REQ )
        self.socket.connect( self.ip_port )

    def process(self, c):
        self.socket.send_pyobj( self.extract_func( c ) )
        msg_in = self.socket.recv_pyobj()

    def endRun( self ):
        del self.socket


class RecvCandidateProperties:
    """ Server side: receive data from the client module
        while listening on ```ip_port```
        self.recv method should be in a non-blocking loop
    """
    def __init__( self, ip_port ):
        context = zmq.Context()
        self.socket = context.socket( zmq.REP )
        self.socket.bind( "tcp://" + ip_port )

    def recv( self ):
        msg = self.socket.recv_pyobj()
        self.socket.send_pyobj(msg)
        return msg

