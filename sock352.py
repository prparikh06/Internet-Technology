
import binascii
import socket as syssock
import struct
import sys
import random


MAX_PACKET_SIZE = 32000
sock352PktHdrData = '!BBBBHHLLQQLL' 
DEFAULT = 5299


#creating a packet "struct"
class packet:
    def __init__(self,version,flags,header_len,sequence_no,ack_no,window,payload_len):     #initialize te packet
        self.version = 0x1 #should always be 0x1
        self.flags = flags{}
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
 
# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

SYN = 0x01 #Connection Initiation
FIN = 0x02 #Connection End
ACK = 0x04 #Connection Acknowledgement 
RESET = 0x08 #Reset Connection
HAS_OPT = 0xA0 # Option Field is valid



def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
    #global port nums
    global portTx
    global portRx

    if int(UDPportTx) == 0:
        portTx = DEFAULT
    elif int(UDPportRx) == 0:
        portRx = DEFAULT
    else:
        portTx = int(UDPportTx)
        portRx = int(UDPportRx)
    
   
    pass 
    
class socket:
    #initialize the socket TODO did not know what else to add
    def __init__(self):  # fill in your code here 
        #need to create server and client socket
        global serversocket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM) #UDP socket
        global clientsocket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)

        self.serversocket = serversocket
        self.clientsocket = clientsocket

        return
    
    def bind(self,address):
        return 
        
    #establish the connection - 3 way handshake
    def connect(self,address):  # fill in your code here 
        
        global cPacket
        global sPacket
        
        destination = address[0] #client passes in (destination,port)
        port = address[1]

        print("initiating 3 way handshake!")
     
        #STEP 1: send from client
        #establish random sequence
        
        print("our randomly generated sequnce is: ",randSequence)
        #initialize the packet to be sent by client
        cPacket = self.packet
        cPacket.sequence_no = rand.rand()
        cPacket.flags = {SYN}
        cPacket.ack_no = 0

        #pack packet and send to addresss
        clientPakcetHeader = struct.Struct(sock352PktHdrData)
        clientHeader = clientPakcetHeader.pack(cPacket.version,cPacket.flags, cPacket.opt_ptr, 
                    cPacket.protocol, cPacket.checksum, cPacket.soure_port,cPacket.dest_port,
                    cPacket.sequence_no, cPacket.ack_no, cPacket.window,cPacket.payload_len)
        serversocket.send(clientHeader, (destination, UDPportTx))
        #TODO literally send this header to server

        

        #STEP 2: server receives SYN and sends SYN-ACK in return
        #TODO CHECK THE STATUS/FLAGS OF THE RECEVIED PACKET - 
        sPacket = self.recv()
        sPacket.sequence_no = rand.rand()
        sPacket.flags = {SYN, ACK}
        sPacket.ack_no = sPacket.sequence_no + 1
        #TODO send another header back to client

        #STEP 3: client sends back random ACK
        cPacket.sequence_no = sPacket.ack_no
        cPacket.ack_no = sPacket.sequence_no + 1
        cPacket.flags = {SYN,ACK}

        #TODO accept on server side again
        sPacket.sequence_no = 
        sPacket.ack_no = cPacket.ack_no + 1

        return 
    
    def listen(self,backlog):
        return

    #accept the connection
    def accept(self):

        #client socket is client socket used to send/receive; address = serversocket's addy
        
        
        (clientsocket, address) = (1,1)  # change this to your code 
        return (clientsocket,address)
    
    #close the connection - 2 double handshakes
    def close(self):   # fill in your code here 
        return 

    #send the packet?
    def send(self,buffer):  # fill in your code here 
        #buffer = file contents
        
        #bytessent should be size of what we can handle 
        
        bytesent = len(buffer)
        if bytesent == 0:
            return 0
        #buffer is the size of packet
        if bytesent <= MAX_PACKET_SIZE:    
            #TODO send to server socket
            self.serversocket.send(buffer)
        else:
            #need to split and send into smaller packets
            while  bytesent >= MAX_PACKET_SIZE:
                #TODO send 32000
                bytesent -= MAX_PACKET_SIZE
                # TODO how do we do thisself.serversocket.send(buffer(bytesent))

            #TODO send last packet which would be of less than 32K

            bytesent+=toSend
        
        return bytesent 

    #receive the packet?
    def recv(self,nbytes):
        bytesreceived = 0     # fill in your code here
        return bytesreceived 
    
    #method to receive ACK
    def recvACK(self):



        return
    
    #method to send ACK
    def sendACK(self):



        return

        

