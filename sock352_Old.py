import binascii
import socket as syssock
import struct
import sys
import random
import time
import thread

sock352PktHdrData = '!BBBBHHLLQQLL' 
DEFAULT = 5299
header_len = struct.calcsize(sock352PktHdrData)
MAX_PACKET_SIZE = 32000 + header_len



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
        self.closed = False
        self.packets = [] #list to keep track of data sent
        self.ack = 0 #keeps track of most recent ack
        self.seq = 0 #keeps track of most recent seq 
	#both have to be 0 since ther are of type Q in header file (unsigned)
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
            final_packet.flags = ACK
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
            self.seq = randSeq
            seq_no = randSeq
            flags = SYN | ACK
            syn_ack_packet = packet(flags,header_len,seq_no,ack_no,0)
            
            self.send_packet(syn_ack_packet,self.send_addr)
            
        else: #pack and send the packet reset
            initialPacket.flags = RESET
            self.send_packet(initialPacket,self.send_addr)
            #return
                 
        #STEP 3 CONTD
        final_packet, addr = self.recv_packet()
        flags = final_packet.flags
        if flags == ACK:
            self.connected = True
            print ("Accepted!")
            
            self.ack = final_packet.ack_no
        else:
		#reset
            final_packet.flags = RESET
            self.send_packet(final_packet, self.send_addr)
            #return	
        print("after connection:self.seq =",self.seq,"self.ack =", self.ack)
        return (self, self.send_addr) 


    #TCP Close = 2 double handshakes!
    #Step 1: client sends FIN flag to server. use most recent sequence number
    #Step 2: server receives; flag = ACK; ack_no = seq + 1 to client
    #Step 3: again, server sends. FIN flag is set, 
    #Step 4: client recvs and sends, ack = seq + 1; ACK flag
    
    def close(self):   # fill in your code here
        
        #Step 1 client sends FIN
        print("current self.seq: ", self.seq) 
        #initialize, pack, and send the fin packet 
        initialPacket = packet(FIN,header_len,self.seq,0,0)
        self.send_packet(initialPacket,self.send_addr)

   
        #Step 2 recv packet and update
        initialPacket, addr = self.recv_packet()
        flags = initialPacket.flags
        self.send_addr = (addr[0], int(portTx))
        print(flags)
        
        if flags == FIN: 
            ack_no = initialPacket.sequence_no + 1
            flags = ACK
            fin_packet = packet(flags,header_len,self.seq,ack_no,0)
            self.send_packet(fin_packet,self.send_addr)
        elif flags == ACK:
            self.closed = True    
        
        #Step 3
        fin_pack, addr = self.recv_packet()
        flags = fin_pack.flags
        #send final FIN
        if flags == FIN:
            #Step 4
            flags = ACK
            ack_no = fin_pack.sequence_no + 1
            fin_packet = packet(flags,header_len,self.seq,ack_no,0)
            self.send_packet(fin_packet, self.send_addr)

        #else: #take care of this    
        self.closed = True
        #STEP 2 & 3: server receives FIN and sends FIN-ACK back
      
        print("Connection closed!!!")
        
    #     self.socket.close()
        return  

    def send(self,buffer):  # fill in your code here 
        if not self.connected:
            print("client has not connected with socket:(")
            return
        elif self.closed:
            print("connection has already been closed")
            return

	#theory: in send, have a new thread for each packet we're going to send
        #buffer = file contents #bytessent should be size of what we can handle 
        print("sending has begun!!!")
        bufferIndex = 0 #tells where in the buffer we are
        bufferSize = len(buffer) 
        if bufferSize < 0: 
            print ("file size is invalid")
            return 
        else:
            print("buffer len:", bufferSize)
	#my_thread = Thread(
	
        bytesSent = 0
        bytesLeft = bufferSize 
	#create thread to make sure all acks are received 
        gbn_thread = theading.Thread(target=recv_ACK, args=(self.ack+bufferSize)) #target = which function,args = args to that function)        
	gbn_thread.start()
        while bytesSent < bufferSize: #while we still have bytes to send...
            bufferIndex = bytesSent + MAX_PACKET_SIZE
            #TODO
            print("currently sending ", currPacketSize," bytes")
            #use send_packet function again, but now we update payload
            payload_len = c
        
            #update bytessent
            bytesSent +=payload_len
      #     try:
                         
        #     except syssock.timeout:
        #         pass
        return bytesSent 
    

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
    
    def recv_ACK(self,ack_no):
    



    
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
 
