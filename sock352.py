import binascii
import socket as syssock
import struct
import sys
import numpy as np
import struct
# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

sender_port = 0
receiver_port = 0
destination = 0
client_isn = 25

PACKET_LIST = []
MAX_PACKET_SIZE = 64*1024
class Packet:
    
    def __init__(self, version = 0, flags = 0, header_len = 0, sequence_no = 0, ack_no = 0, payload_len = 0, data = 0):
        self.version = version
        self.flags = flags
        self.header_len = header_len
        self.sequence_no = sequence_no
        self.ack_no = ack_no
        self.payload_len = payload_len
        self.data = data
        self.SOCK352_SYN = 1
        self.SOCK352_FIN = 2
        self.SOCK352_ACK = 4
        self.SOCK352_RESET = 8
        self.SOCK352_HAS_OPT = 16
        self.packet_format = '!BBHQQLQ'


    def pack(self):
        bindata = struct.pack(self.packet_format, self.version, self.flags, self.header_len, self.sequence_no, self.ack_no, self.payload_len, self.data)
        return bindata
    def unpack(self, bytes ):
        packet_fields = struct.unpack(self.packet_format, bytes)
        self.version = packet_fields[0]
        self.flags = packet_fields[1]
        self.header_len = packet_fields[2]
        self.sequence_no = packet_fields[3]
        self.ack_no = packet_fields[4]
        self.payload_len = packet_fields[5]
        self.data = packet_fields[6]

def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
    global sender_port
    global receiver_port
    sender_port = UDPportTx
    receiver_port = UDPportRx
    pass 
    
class socket:

    def __init__(self):  # fill in your code here 

        self.sock = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
        #self.sock2 = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
        self.packet = Packet()
        return
    
    def bind(self,address):
        #Bind socket sock to the given address
        self.sock.bind(address)
        print('Bind: ' + str(address[1]))
        return 

    def connect(self,address):  # fill in your code here 
        global client_isn
        global PACKET_LIST
        global destination 
        destination = address
        #Make UDP Connection and bind receiving socket
        #self.sock.bind(1112)
        self.sock.connect(address)
        print('Connect: ' + str(address))
        #Create connection packet and initialize variables
        #self.packet.version = self.packet.SOCK352_SYN
        #self.packet.sequence_no = client_isn
        #Pack the function
        #packed_data = self.packet.pack()

        #Send packet
        #self.sock2.sendto(packed_data, address)
        #PACKET_LIST.append(Packet(self.packet.version, self.packet.flags, self.packet.header_len, self.packet.sequence_no, self.packet.ack_no, self.packet.payload_len, self.packet.data))


        #print(PACKET_LIST)

        return 
    
    def listen(self,backlog):
        #Don't have to do anything
        return

    def accept(self):
        global destination
        (clientsocket, address) = (self,destination) # change this to your code
        print('Accept: ' + str(self))
        return (clientsocket,address)
     
    def close(self):   # fill in your code here 
        self.sock.close()
        #self.sock2.close()
        return 

    def send(self,buffer):
        global PACKET_LIST
        global client_isn
        global destination
        print('sending...')
        self.packet.version = self.packet.SOCK352_SYN
        self.packet.sequence_no = client_isn
        packed_data = self.packet.pack()
        bytessent = 10     # fill in your code here
        #buff = self.packet.pack(buffer)
        #PACKET_LIST.append(buff)
        self.sock.send(packed_data)
        PACKET_LIST.append(Packet(self.packet.version, self.packet.flags, self.packet.header_len, self.packet.sequence_no, self.packet.ack_no, self.packet.payload_len, self.packet.data))
        return bytessent 

    def recv(self,nbytes):
        global MAX_PACKET_SIZE

        bytesreceived = self.sock.recv(nbytes)
        print('bytes received at server: ' + bytesreceived)
        return bytesreceived 


    

# import binascii
# import socket as syssock
# import struct
# import sys
# import random


# MAX_PACKET_SIZE = 32000
# sock352PktHdrData = '!BBBBHHLLQQLL' 
# DEFAULT = 5299
# packets = []


# #creating a packet "struct"
# class packet:
#     def __init__(self,flags, header_len,sequence_no,ack_no,payload_len):     #initialize the packet
#         self.version = 0x1
#         self.flags = flags
#         self.opt_ptr = 0
#         self.checksum = 0 #TODO what is this
#         self.protocol = 0
#         self.header_len = header_len
#         self.source_port = 0
#         self.dest_port = 0
#         self.sequence_no = sequence_no
#         self.ack_no = ack_no
#         self.window = 0
#         self.payload_len = payload_len
#         return   
 
# # these functions are global to the class and
# # define the UDP ports all messages are sent
# # and received from

# SYN = 0x01 #Connection Initiation
# FIN = 0x02 #Connection End
# ACK = 0x04 #Connection Acknowledgement 
# RESET = 0x08 #Reset Connection
# HAS_OPT = 0xA0 # Option Field is valid



# def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
#     #global port nums
#     global portTx #transmit = client
#     global portRx #receiving = server

#     if int(UDPportTx) == 0:
#         portTx = DEFAULT
#     elif int(UDPportRx) == 0:
#         portRx = DEFAULT
#     else:
#         portTx = int(UDPportTx)
#         portRx = int(UDPportRx)
    
   
#     pass 
    
# class socket:
#     def __init__(self):  # fill in your code here 
#         #make a UDP socket as defined in the Python library
        
#         self.mySock = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
     
#         return
    
#     def bind(self,address):
#         return 
        
#     #establish the connection - 3 way handshake
#     def connect(self,address):  # fill in your code here 
       
#         destination = address[0] #client passes in (destination,port)
#         port = address[1]
#         #assign portTx to the port number that the client passed; portRx = destination
#         portTx = port
#         portRx = destination
#         print("initiating 3 way handshake!")
     
#         #STEP 1: send from client
#         #establish random sequence
        
       

#         #initialize the packet to be sent by client
#         clientPacketHeader = struct.Struct(sock352PktHdrData)
#         header_len = struct.calcsize(sock352PktHdrData)
#         cPacket = packet
#         cPacket.sequence_no = random.randint(1,10000)
#         cPacket.flags = {SYN}
#         cPacket.ack_no = 0
#         cPacket.payload_len = 0
#         cPacket.header_len = header_len 

#         #pack packet and send to addresss
        
#         clientHeader = clientPacketHeader.pack(cPacket)
        
#         #sendto is inbuilt python function
#         self.mySock.sendto(clientHeader,portRx)
        
#         #STEP 3: recv ACK from server, send final ACK
#         (cPacket, address) = self.recvACK()  
#         cPacket.flags = {SYN,ACK} #TODO check flags
#         cPacket.sequence_no = cPacket.ack_no
#         cPacket.ack_no = cPacket.sequence_no + 1

#         #pack packet and send to addresss = portTX??
       
#         clientHeader = clientPacketHeader.pack(cPacket)
#         self.mySock.sendto(clientHeader,portTx)

#         print("Connected! (Host)")
#         return 
    
#     def listen(self,backlog):
#         return

#     #accept the connection
#     def accept(self):
    
#         #STEP 2: server receives SYN and sends SYN-ACK in return
#         #TODO CHECK THE STATUS/FLAGS OF THE RECEVIED PACKET 
#         serverPacketHeader = struct.Struct(sock352PktHdrData)
#         header_len = struct.calcsize(sock352PktHdrData)
        
#         #unpack whatever data we just received
#         (sPacket, address) = self.recvACK()
            
#         sPacket.sequence_no = random.randint(1,10000)
#         sPacket.flags = {SYN,ACK}
#         sPacket.ack_no = sPacket.sequence_no + 1
#         sPacket.payload_len = 0 #TODO
#         sPacket.header_len = header_len
            
      
#         #pack packet and send to addresss portTX??
        
#         serverHeader = serverPacketHeader.pack(sPacket.flags, sPacket.sequence_no, sPacket.ack_no,cPacket.payload_len)
#         self.mySock.sendto(serverHeader,portTx)
        
#         #STEP 3 contd: recv the final packet the client sent
#         (sPacket, address) = self.recvACK() #TODO check flag 

#         print ("Done connecting...")
#         #need to return (s2,address)
#         return (self.mySock, address) 

    
#     def close(self):   # fill in your code here

#        #Step 1 client sends FIN
#         cPacket = packet()
#         cPacket.sequence_no = rand.rand()
#         cPacket.flags = {FIN}
#         cPacket.ack_no = 0 #TODO
#         cPacket.payload_len = 0 #TODO

#         clientPacketHeader = struct.Struct(sock352PktHdrData)
#         clientHeader = clientPacketHeader.pack(cPacket.version,cPacket.flags, cPacket.sequence_no, cPacket.ack_no, cPacket.payload_len)
        
#         self.mySock.sendto(clientHeader,portRx)

#       #STEP 2 & 3: server receives FIN and sends FIN-ACK back
#         (sPacket, address) = self.recvfrom()
#         sPacket.sequence_no = rand.rand()
#         sPacket.flags = {FIN, ACK}
#         sPacket.ack_no = sPacket.sequence_no + 1
#         sPacket.payload_len = 0 #TODO

#         serverHeader = sock352PktHdrData.pack(sPacket.flags, sPacket.sequence_no, sPacket.ack_no,cPacket.payload_len)
#         self.mySock.sendto(serverHeader,portTx)


#         #Step 4: client sends back an ACK
#         cPacket.sequence_no = sPacket.ack_no
#         cPacket.ack_no = sPacket.sequence_no + 1
#         cPacket.flags = {ACK}

#         (sPacket, address) = self.recvACK()
#         sPacket.sequence_no = rand.rand()
#         sPacket.ack_no = cPacket.ack_no + 1


#         #need to return (s2,address)
#         print("Closing the connection")
        
#         self.mySock.close()
#         return  

#     def send(self,buffer):  # fill in your code here 
#         #buffer = file contents
#         #bytessent should be size of what we can handle 
#         bufferIndex = len(buffer)
#         bytessent = 0
#         packetIndex = 0
#         while bytessent < bufferIndex:
#         #buffer is larger than max
#             try:
                
#                 #TODO send the info using sendto? --make packet that will actually get sent
#                 if (packetIndex == 0): #first packet getting sent
#                     self.mySock.sendto(buffer[bytessent: MAX_PACKET_SIZE],portRx)
#                     bufferIndex -= MAX_PACKET_SIZE
#                     bytessent += MAX_PACKET_SIZE
#                     continue

#                 if (packetIndex > 0): #not the first packet
#                     #check for GBN
#                     if (packets[packetIndex-1] == None): #TODO #if there was no packet recvd before it/aka not been sent properly
#                         #do go back n ? send everything again? recursively redo
#                         packets.clear()
#                         socket.send(self,buffer)
                            
#                     else: 
#                         self.mySock.sendto(buffer[bytessent: MAX_PACKET_SIZE],portRx)
#                         bufferIndex -= MAX_PACKET_SIZE
#                         bytessent += MAX_PACKET_SIZE
#                     continue
                          
#             except syssock.timeout:
#                 pass
#         return bytessent 
    

#     def recv(self,nbytes):
#         bytesreceived = 0     # fill in your code here
               
#         while bytesreceived < nbytes:
#             try:
#                 currPacket = self.mySock.recv(min(nbytes - bytesreceived, MAX_PACKET_SIZE))
#                 packets.append(currPacket)
#                 bytesreceived = bytesreceived + len(packet)
            
            
#             except syssock.timeout:
#                 pass
#         return bytesreceived
#     def recvACK(self):
#         recvSize = struct.calcsize(sock352PktHdrData)
#         (data, address) = self.mySock.recvfrom(recvSize)
#         #unpack whatever data we just received
#         recvPacket = sock352PktHdrData.unpack(data)

#         #check the flags of recvPacket here TODO

#         #return the received packet
#         return (recvPacket , address)
