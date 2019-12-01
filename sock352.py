import binascii
import socket as syssock
import struct
import sys
import random


MAX_PACKET_SIZE = 32000
sock352PktHdrData = '!BBBBHHLLQQLL' 
DEFAULT = 5299
header_len = struct.calcsize(sock352PktHdrData)



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
    global portTx #transmit = client
    global portRx #receiving = server

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
        #make a UDP socket as defined in the Python library
        self.socket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
        self.socket.settimeout(0.2) #set the timeout 
        self.connected = False #boolean to keep track of open connection
        self.packets = [] #list to keep track of data sent
        
        return
    
    def bind(self,address):
        return 
        
    #establish the connection - 3 way handshake
    #NOTE: address is of type in form {destination IP, port} that client passes in

    def connect(self,address):  # fill in your code here 
        if self.connected: #return error
            print ("Client has already connected to server")
        
        destination = address[0] 
        port = address[1]
        
        #TODO cast ? str or int        
        self.recv_addr = (destination, portRx)
        self.send_addr = (destination, portTx)
        
        self.socket.bind(self.recv_addr)

        print("initiating 3 way handshake!")
        self.socket.settimeout(0.2)
        #STEP 1: send from client

        connectionComplete = False
        randSeq = random.randint(1,10000) #establish random sequence
        #send packet from client 
        
        #initialize, pack, and send the syn packet 
        initialPacket = packet(flags=SYN,header_len=header_len,sequence_no=randSeq,ack_no=0,payload_len=0)
        initialPacketData = struct.pack(sock352PktHdrData, initialPacket.version, initialPacket.flags, initialPacket.opt_ptr, initialPacket.protocol, initialPacket.header_len, initialPacket.checksum, initialPacket.source_port, initialPacket.dest_port, initialPacket.sequence_no, initialPacket.ack_no, initialPacket.window, initialPacket.payload_len)
        self.socket.sendto(initialPacketData, self.send_addr)

        while not connectionComplete:
        
            #STEP 3: recv ACK from server, send final ACK
            (syn_ack_packet, address) = self.recvPacket()  
            
            flags = syn_ack_packet['flags']
            
            #check flags
            if flags == SYN | ACK:
                connectionComplete = True 
                newSeq = syn_ack_packet['ack_no']
                newAck = syn_ack_packet['sequence_no'] + 1
                syn_ack_packet['sequence_no'] = newSeq
                syn_ack_packet['ack_no'] = newAck

                #pack and send packet to sender addresss

                syn_ack_packet_data = struct.pack(sock352PktHdrData,syn_ack_packet.version, syn_ack_packet.flags, syn_ack_packet.opt_ptr, syn_ack_packet.protocol, syn_ack_packet.header_len, syn_ack_packet.checksum, syn_ack_packet.source_port, syn_ack_packet.dest_port, syn_ack_packet.sequence_no, syn_ack_packet.ack_no, syn_ack_packet.window, syn_ack_packet.payload_len)

                self.socket.sendto(syn_ack_packet_data, self.send_addr)
            elif flags == RESET:
                print ("something went wrong so connection has been reset")
                return

        
        print("connecting...!")
        return 
    
    def listen(self,backlog):
        return

    #accept the connection
    def accept(self):
        accepted = False
        #STEP 2: server receives SYN and sends SYN-ACK in return
        while not accepted:
            initialPacket = self.recvPacket()
            #initialPacket = struct.unpack(sock352PktHdrData,initialPacketData)
            flags = initialPacket['flags']
            if flags == SYN:
                accepted = True
                initialPacket['ack_no'] = initialPacket['sequence_no'] + 1
            else: #pack and send the packet reset
                initialPacket['flags'] = RESET
                initialPacketData = struct.pack(sock352PktHdrData,initialPacket.version, initialPacket.flags, initialPacket.opt_ptr, initialPacket.protocol, initialPacket.header_len, initialPacket.checksum, initialPacket.source_port, initialPacket.dest_port, initialPacket.sequence_no, initialPacket.ack_no, initialPacket.window, initialPacket.payload_len)
                self.socket.sendto(initialPacketData, self.send_addr)
        
        self.connected = True

        print ("Accepted!")
        #need to return (s2,address)
        return (self, self.send_addr) 

    
    def close(self):   # fill in your code here
        
    #    #Step 1 client sends FIN
    #     cPacket = packet()
    #     cPacket.sequence_no = rand.rand()
    #     cPacket.flags = {FIN}
    #     cPacket.ack_no = 0 #TODO
    #     cPacket.payload_len = 0 #TODO

    #     clientPacketHeader = struct.Struct(sock352PktHdrData)
    #     clientHeader = clientPacketHeader.pack(cPacket.version,cPacket.flags, cPacket.sequence_no, cPacket.ack_no, cPacket.payload_len)
        
    #     self.mySock.sendto(clientHeader,portRx)

    #   #STEP 2 & 3: server receives FIN and sends FIN-ACK back
    #     (sPacket, address) = self.recvfrom()
    #     sPacket.sequence_no = rand.rand()
    #     sPacket.flags = {FIN, ACK}
    #     sPacket.ack_no = sPacket.sequence_no + 1
    #     sPacket.payload_len = 0 #TODO

    #     serverHeader = sock352PktHdrData.pack(sPacket.flags, sPacket.sequence_no, sPacket.ack_no,cPacket.payload_len)
    #     self.mySock.sendto(serverHeader,portTx)


    #     #Step 4: client sends back an ACK
    #     cPacket.sequence_no = sPacket.ack_no
    #     cPacket.ack_no = sPacket.sequence_no + 1
    #     cPacket.flags = {ACK}

    #     (sPacket, address) = self.recvACK()
    #     sPacket.sequence_no = rand.rand()
    #     sPacket.ack_no = cPacket.ack_no + 1


    #     #need to return (s2,address)
    #     print("Closing the connection")
        
    #     self.mySock.close()
        return  

    def send(self,buffer):  # fill in your code here 
        #buffer = file contents
        #bytessent should be size of what we can handle 
        bufferIndex = len(buffer)
        bytessent = 0
        # packetIndex = 0
        # while bytessent < bufferIndex:
        # #buffer is larger than max
        #     try:
                
        #         #TODO send the info using sendto? --make packet that will actually get sent
        #         if (packetIndex == 0): #first packet getting sent
        #             self.mySock.sendto(buffer[bytessent: MAX_PACKET_SIZE],portRx)
        #             bufferIndex -= MAX_PACKET_SIZE
        #             bytessent += MAX_PACKET_SIZE
        #             continue

        #         if (packetIndex > 0): #not the first packet
        #             #check for GBN
        #             if (packets[packetIndex-1] == None): #TODO #if there was no packet recvd before it/aka not been sent properly
        #                 #do go back n ? send everything again? recursively redo
        #                 packets.clear()
        #                 socket.send(self,buffer)
                            
        #             else: 
        #                 self.mySock.sendto(buffer[bytessent: MAX_PACKET_SIZE],portRx)
        #                 bufferIndex -= MAX_PACKET_SIZE
        #                 bytessent += MAX_PACKET_SIZE
        #             continue
                          
        #     except syssock.timeout:
        #         pass
        return bytessent 
    

    def recv(self,nbytes):
        bytesreceived = 0     # fill in your code here
               
        # while bytesreceived < nbytes:
        #     try:
        #         currPacket = self.mySock.recv(min(nbytes - bytesreceived, MAX_PACKET_SIZE))
        #         packets.append(currPacket)
        #         bytesreceived = bytesreceived + len(packet)
            
            
        #     except syssock.timeout:
        #         pass
        return bytesreceived
    
    
    def recvPacket(self):
        
        (data, address) = self.socket.recvfrom(header_len)
        #unpack whatever data we just received
        recvPacket = struct.unpack(sock352PktHdrData, data)
        
        #return the received packet
        return recvPacket


#creating a packet "struct"
class packet:
    def __init__(self,flags, header_len,sequence_no,ack_no,payload_len):     #initialize the packet
        self.version = 0x1
        self.flags = flags
        self.opt_ptr = 0
        self.checksum = 0 #TODO what is this
        self.protocol = 0
        self.header_len = header_len
        self.source_port = 0 
        self.dest_port = 0
        self.sequence_no = sequence_no
        self.ack_no = ack_no
        self.window = 0
        self.payload_len = payload_len
        return    
 
