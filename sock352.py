
import binascii
import socket as syssock
import struct
import sys


MAX_PACKET_SIZE = 64000
 

#creating a packet "struct"
class packet:
    def __init__(self,version,flags,header_len,sequence_no,ack_no,window,payload_len):     #initialize te packet
        self.version = 0x1 #should always be 0x1
        self.flags = flags
        self.opt_ptr = 0
        self.protocol = 0
        self.header_len = header_len
        self.checksum = 0
        self.soure_port = 0
        self.dest_port = 0
        self.sequence_no = sequence_no
        self.ack_no = ack_no
        self.window = 0
        self.payload_len = payload_len
        return
    def pack(self): #method to pack
        return
    def unpack(self): #method to unpack
        return
    
    



# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
    #global port nums
    global portTx
    global portRx
    pass 
    
class socket:
    
    def __init__(self):  # fill in your code here 
        return
    
    def bind(self,address):
        return 

    def connect(self,address):  # fill in your code here 
        return 
    
    def listen(self,backlog):
        return

    def accept(self):
        (clientsocket, address) = (1,1)  # change this to your code 
        return (clientsocket,address)
    
    def close(self):   # fill in your code here 
        return 

    def send(self,buffer):
        bytessent = 0     # fill in your code here 
        return bytesent 

    def recv(self,nbytes):
        bytesreceived = 0     # fill in your code here
        return bytesreceived 


    

