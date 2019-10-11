
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
        global clientsocket = syssock.socket()

        self.packet = packet()
        self.serversocket = serversocket
        self.clientsocket = clientsocket

        return
    
    def bind(self,address):
        return 
        
    #establish the connection - 3 way handshake
    def connect(self,address):  # fill in your code here 
        
        global clientPacket
        global serverPacket
        
        destination = address[0] #client passes in (destination,port)
        port = address[1]

        print("initiating 3 way handshake!")
     

        #STEP 1: send from client
        #establish random sequence
        randSequence = random.random()
        print("our randomly generated sequnce is: ",randSequence)
        #initialize the packet to be sent by client
        clientPacket = self.packet
        clientPacket.sequence_no = randSequence
        clientPacket.flags = {SYN}
        clientPacket.ack_no = 0

        #pack packet and send to addresss
        clientPakcetHeader = struct.Struct(sock352PktHdrData)
        clientHeader = clientPakcetHeader.pack(clientPacket.version,clientPacket.flags, clientPacket.opt_ptr, 
                    clientPacket.protocol, clientPacket.checksum, clientPacket.soure_port,clientPacket.dest_port,
                    clientPacket.sequence_no, clientPacket.ack_no, clientPacket.window,clientPacket.payload_len)
        serversocket.send(clientHeader, (destination, UDPportTx))
        
        #STEP 2: server receives SYN and sends SYN-ACK in return
        #TODO CHECK THE STATUS/FLAGS OF THE RECEVIED PACKET - 
        serverPacket = self.recv()
        #serverHeader = serversocket.unpack(sock352PktHdrData,)
        serverPacket.sequence_no = clientPacket.sequence_no
        serverPacket.flags = {SYN, ACK}
        serverPacket.ack_no = serverPacket.sequence_no + 1



        #STEP 3: client sends back ACK
        

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
        #bytessent should be size of what we can handle 
        bytessent = 0 
        toSend = len(buffer)
        if toSend == 0:
            return 0
        

        #buffer is the size of packet
        if toSend <= MAX_PACKET_SIZE:    
            bytesent = toSend
            #TODO send 
        else:
            #need to split and send into smaller packets
            
            while  toSend >= MAX_PACKET_SIZE:
                #TODO send 32000
                toSend -= 32000
                bytesent+=toSend
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

    def pack(self): #method to pack into sendable binary data or less
        
        return
    def unpack(self): #method to unpack into readable data
        
        return
        

