
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
    def __init__(self):  # fill in your code here 
        #TODO: not sure if this is right
   #     global serversocket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM) #UDP socket
   #     global clientsocket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
    
    global serversocket
    global clientsocket
        if socket is None:
            self.serversocket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
            self.clientsocket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
        else:
        self.serversocket = serversocket
        self.clientsocket = clientsocket 

        return
    
    def bind(self,address):
        return 
        
    #establish the connection - 3 way handshake
    def connect(self,address):  # fill in your code here 
        self.serversocket.connect(host, port) #TODO not sure what else this needs

        return 
    
    def listen(self,backlog):
        return

    #accept the connection
    def accept(self):
        #client socket is client socket used to send/receive; address = serversocket's addy
        (clientsocket, address) = (1,1)  # change this to your code  
        
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
        clientPacketHeader = struct.Struct(sock352PktHdrData)
        clientHeader = clientPacketHeader.pack(cPacket.version,cPacket.flags, cPacket.opt_ptr, 
                    cPacket.protocol, cPacket.checksum, cPacket.soure_port,cPacket.dest_port,
                    cPacket.sequence_no, cPacket.ack_no, cPacket.window,cPacket.payload_len)
        serversocket.send(clientHeader, (destination, UDPportTx))
        #TODO literally send this header to server   
        return (clientsocket,address)
    
    
    
    def close(self):   # fill in your code here 
        
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


    def send(self,buffer):  # fill in your code here 
        #buffer = file contents
        #bytessent should be size of what we can handle 
        
        bytesent == 0
        while bytesent < len(buffer)
        #buffer is larger than max
            if  len(buffer) >= MAX_PACKET_SIZE:
                self.clientsocket.send(buffer[bytesent: MAX_PACKET_SIZE])
                len(buffer) -= MAX_PACKET_SIZE
                bytesent += MAX_PACKET_SIZE
            else: 
                len(buffer) <= MAX_PACKET_SIZE:    
                self.clientsocket.send(buffer)
                bytesent += len(buffer)       
            return bytesent 
         if bytesent == 0
            raise RuntimeError("Connection broken")
    

    def recv(self,nbytes):
        bytesreceived = 0     # fill in your code here
        packets = []
        
        while bytesreceived < nbytes:
            packet = self.clientsocket.recv(min(nbytes - bytesreceived, MAX_PACKET_SIZE))
            if packet == '':
                raise RuntimeError("Connection broken")
            packets.append(packet)
            bytesreceived = bytesreceived + len(packet)
        return bytesreceived
        



