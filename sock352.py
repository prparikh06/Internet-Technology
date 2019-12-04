import binascii
import socket as syssock
import struct
import sys
import random
import time


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

    print("portTx = sending port: ", portTx, "portRx = receiving port: ", portRx)   
    #syssock.socket.bind(('', portRx))

    pass 
    
class socket:
    def __init__(self):  # fill in your code here 
        #make a UDP socket as defined in the Python library
        self.socket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
        #self.socket.settimeout(0.2) #set the timeout 
        self.connected = False #boolean to keep track of open connection
        self.packets = [] #list to keep track of data sent
        
        return
    
    def bind(self,address):
        global portRx
        self.recv_addr = (address[0], int(portRx))
        self.socket.bind(self.recv_addr)
        
        
    #establish the connection - 3 way handshake
    #TCP: step 1: connect - random number for sequence_no, flag = SYN, send packet to server
    #step 2: accept - receive the packet - sequence_no = new random, flag = SYN | ACK, ack_no = old sequence_no + 1, send to client
    #step 3: connect & accept- receive the packet - ack_no = seq_no + 1
    #NOTE: address is of type in form {destination IP, port} that client passes in

    def connect(self,address):  # fill in your code here 
        global portRx, portTx
        print("header len: ", header_len)
        if self.connected: #return error
            print ("Client has already connected to server")
        
        destination = address[0] 
        
        print ("get hostname:",syssock.gethostname()) 
                
        self.recv_addr = (syssock.gethostname(), int(portRx)) #receiving = client
        self.send_addr = (destination, portTx) # sending = server
        
        self.socket.bind(self.recv_addr)
        print("initiating 3 way handshake!")

        #STEP 1: send from client
        randSeq = random.randint(1,100) #establish random sequence
        print ("random int: ", randSeq)
        #initialize, pack, and send the syn packet 
        initialPacket = packet(SYN,header_len,randSeq,0,0)
        self.send_packet(initialPacket,self.send_addr)

        #STEP 3: recv ACK from server, send final ACK
        syn_ack_packet, addr = self.recv_packet()
        print("recvd syn_ack")
        flags = syn_ack_packet.flags
        print(flags)
        #check flags
        if flags == SYN | ACK:
            print("step 3")
            final_packet = syn_ack_packet
            final_packet.ack_no = final_packet.sequence_no + 1
            self.send_packet(final_packet, self.send_addr)
            print("should be done!!")
            
        
        elif flags == RESET:
            print ("something went wrong so connection has been reset")
            return
        
        print("connecting...!")
        return 
    
    def listen(self,backlog):
        return

    #accept the connection
    def accept(self):
        global portTx

        print("ready to accept")
        #STEP 2: server receives SYN and sends SYN-ACK in return    
        initialPacket, addr = self.recv_packet()
        flags = initialPacket.flags
        self.send_addr = (addr[0], int(portTx))
        print(flags)
        
        if flags == SYN: 
            ack_no = initialPacket.sequence_no + 1
            randSeq = random.randint(1,100)
            seq_no = randSeq
            flags = SYN | ACK
            syn_ack_packet = packet(flags,header_len,seq_no,ack_no,0)
            
            self.send_packet(syn_ack_packet,self.send_addr)
            
        else: #pack and send the packet reset
            initialPacket.flags = RESET
            self.send_packet(initialPacket,self.send_addr)
            return
                 
        #STEP 3 CONTD
        final_packet, addr = self.recv_packet()
        
        self.connected = True

        print ("Accepted!")
       
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
    
    
    def recv_packet(self):
        syn_ack_packet_data,addr = self.socket.recvfrom(header_len)
        syn_ack_packet = struct.unpack(sock352PktHdrData, syn_ack_packet_data)
        
        newPacket = packet(syn_ack_packet[1], syn_ack_packet[5], syn_ack_packet[8], syn_ack_packet[9], syn_ack_packet[11])
        return (newPacket, addr)
    
    
    def send_packet(self,packetToSend, address):
        packetToSendData = struct.pack(sock352PktHdrData,packetToSend.version, packetToSend.flags, packetToSend.opt_ptr, packetToSend.protocol, packetToSend.header_len, packetToSend.checksum, packetToSend.source_port, packetToSend.dest_port, packetToSend.sequence_no, packetToSend.ack_no, packetToSend.window, packetToSend.payload_len)
        self.socket.sendto(packetToSendData, address)
        return



#creating a packet "struct"
class packet:
    def __init__(self,flags, header_len,sequence_no,ack_no,payload_len):     #initialize the packet
        self.version = 0x1 #0
        self.flags = flags #1
        self.opt_ptr = 0 #2
        self.checksum = 0 #3 TODO what is this
        self.protocol = 0 #4
        self.header_len = header_len #5
        self.source_port = 0 #6
        self.dest_port = 0 #7
        self.sequence_no = sequence_no #8
        self.ack_no = ack_no #9
        self.window = 0 #10
        self.payload_len = payload_len #11
        return    
 
