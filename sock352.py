import binascii
import socket as syssock
import struct
import sys
import random
import math
import time
from threading import Thread, Lock

sock352PktHdrData = '!BBBBHHLLQQLL' 
DEFAULT = 5299
header_len = struct.calcsize(sock352PktHdrData)
MAX_PACKET_SIZE = 32000



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
        self.timeout_occurred = False
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
        self.socket.settimeout(0.2)
        self.socket.bind(self.recv_addr)
        print("initiating 3 way handshake!")

        #STEP 1: send from client
        randSeq = random.randint(1,100) #establish random sequence
        print ("random int: ", randSeq)
        #initialize, pack, and send the syn packet 
        print("header for payload", len(b''))
        initialPacket = packet(SYN,header_len,randSeq,0,payload=b'')
        self.send_packet(initialPacket,self.send_addr)

        #STEP 3: recv ACK from server, send final ACK
        syn_ack_packet, addr = self.recv_packet(header_len)
        print("recvd syn_ack")
        flags = syn_ack_packet.flags
        print(flags)

        #check flags
        if flags == SYN | ACK:
            print("step 3")
            syn_ack_packet.payload = b''
            syn_ack_packet.ack_no = syn_ack_packet.sequence_no + 1
            syn_ack_packet.flags = ACK
            self.send_packet(syn_ack_packet, self.send_addr)
            print("should be done!!")
            
        
        elif flags == RESET:
            print ("something went wrong so connection has been reset")
            return
        
        print("connecting...!")
        self.connected = True
        return 
    
    def listen(self,backlog):
        return

    #accept the connection
    def accept(self):
        global portTx

        print("ready to accept")
        #STEP 2: server receives SYN and sends SYN-ACK in return    
        initialPacket, addr = self.recv_packet(header_len)
        flags = initialPacket.flags
        self.send_addr = (addr[0], int(portTx))
        print(flags)
        
        if flags == SYN: 
            ack_no = initialPacket.sequence_no + 1
            randSeq = random.randint(1,100)
            self.seq = randSeq
            seq_no = randSeq
            flags = SYN | ACK
            syn_ack_packet = packet(flags,header_len,seq_no,ack_no,b'')
             
            self.send_packet(syn_ack_packet,self.send_addr)
            
        else: #pack and send the packet reset
            initialPacket.flags = RESET
            self.send_packet(initialPacket,self.send_addr)
            #return
                 
        #STEP 3 CONTD
        self.socket.settimeout(0.2)
        final_packet, addr = self.recv_packet(header_len)
        flags = final_packet.flags
        if flags == ACK:
            self.connected = True
            print ("Accepted!")
            self.connected = True 
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
        initialPacket = packet(FIN,header_len,self.seq,0,b' ')
        self.send_packet(initialPacket,self.send_addr)

        self.socket.settimeout(0.2)
        #Step 2 recv packet and update
        initialPacket, addr = self.recv_packet(header_len)
        flags = initialPacket.flags
        self.send_addr = (addr[0], int(portTx))
        print(flags)
        
        if flags == FIN: 
            ack_no = initialPacket.sequence_no + 1
            flags = ACK
            fin_packet = packet(flags,header_len,self.seq,ack_no,b' ')
            self.send_packet(fin_packet,self.send_addr)
            self.closed = True
        elif flags == ACK and initialPacket.ack_no == self.seq + 1:
            #TODO do something? 
            print("this should theoretically break the loop") 
      

        self.socket.settimeout(0.2)
        #Step 3
        fin_pack, addr = self.recv_packet(header_len)
        #flags = fin_pack.flags
        payload = fin_pack.payload_len
        if payload < 0:
            return
        elif fin_pack.flags == FIN: 
      	    #send final ACK
            flags = ACK
            ack_no = fin_pack.sequence_no + 1
            fin_packet = packet(flags,header_len,self.seq,ack_no,b' ')
            self.send_packet(fin_packet, self.send_addr)

        #else: #take care of this    
        self.closed = True
        #STEP 2 & 3: server receives FIN and sends FIN-ACK back
      
        print("Connection closed!!!")
        
    #     self.socket.close()
        return  

    def send(self,buffer):  # fill in your code here 
        if not self.connected:
            print("client has not connected with socket :(")
            return -1
        elif self.closed:
            print("connection has already been closed")
            return -1
        final_ack = len(buffer) + self.ack   #what our final ack should be
        bytesLeft = len(buffer) #bytes left to send
        self.socket.settimeout(0.2)
        #we want to have a thread to keep track of all the acks recvd, which is different function
        ack_thread = Thread(target=self.recv_ack, args = (final_ack))
        curr_ack = len(buffer)
        ack_thread.start()
        while ack_thread.isAlive():
            with Lock():
                if self.timeout_occurred: #if timeout occurred, GBN
                     curr_ack = self.ack #reset ack 
                     self.timout_occurred = False
            if curr_ack >= final_ack: 
                curr_ack = max(curr_ack-MAX_PACKET_SIZE, self.ack)
            startIndex = curr_ack - self.ack
            bytesLeft = final_ack - curr_ack
            endIndex = startIndex + min(bytesLeft, MAX_PACKET_SIZE)
            payload = buffer[startIndex : endIndex]
            payload_len =  endIndex - startIndex
            #send payload packet
            curr_packet = packet(0, header_len,curr_ack, 0, payload)
            print(0,header_len,curr_ack,0,payload_len)
            self.send_packet(curr_packet, self.send_addr)
            curr_ack += payload_len #update the current ack by adding however many bytes we sent
            
        return len(buffer) 
    

    def recv(self,nbytes):
        packets_recvd = 0     # fill in your code here
        self.socket.settimeout(None)
        packets_to_send = int(math.ceil(float(nbytes/MAX_PACKET_SIZE)))
        packet_size = 0
        while packets_recvd < packets_to_send:
            if packets_recvd  == packets_to_send - 1:
                packet_size = header_len + nbytes - (packets_recvd * MAX_PACKET_SIZE)
            else: 
                packet_size = header_len + MAX_PACKET_SIZE

            curr_packet,addr = self.recv_packet(packet_size)
            payload = curr_packet.payload
            print("curr packs payload type: ", type(payload))
            
            if curr_packet.flags != 0:

                print("flag was not 0, nbd")

            elif curr_packet.sequence_no == self.seq:
                self.packets.append(curr_packet.payload) 
                packets_recvd += 1
            curr_packet.ack_no = self.seq
            curr_packet.flags = ACK
            curr_packet.payload = payload
            self.send_packet(curr_packet,self.send_addr)
            return b''.join(self.packets) 
                
    
    def recv_ack(self,ack_no):
        
        print(ack_no)
        timer = time.time()
        while self.ack < ack_no:
            curr_packet,addr = self.recv_packet(header_len)
            flag = curr_packet.flags
            if flag == ACK:
                if curr_packet.ack_no > self.ack:
                    with Lock():
                        self.ack = curr_packet.ack_no
                        timer = time.time()
            elif flag == RESET:
                curr_packet.flags = ACK
                curr_packet.ack_no = self.seq
                self.send_packet(curr_packet,self.send_addr)
            elif flag == FIN: #done sending
                self.closed = True
                curr_packet.ack_no = curr_packet.sequence_no + 1
                curr_packet.flags = ACK
                self.send_packet(curr_packet,self.send_addr)
            if time.time() - timer > 0.2:
               self.register_timeout() 



    def register_timeout(self):
        with Lock():
            self.timeout = True
  
    def recv_packet(self,size):
        my_struct = struct.Struct(sock352PktHdrData)
        syn_ack_packet_data,addr = self.socket.recvfrom(size)
        header = syn_ack_packet_data[:header_len]
        this_packet = my_struct.unpack(header)
        
        if len(this_packet) > header_len:
            payload = this_packet[header_len:]
        else:
            payload = b''

        newPacket = packet(this_packet[1], this_packet[5], this_packet[8], this_packet[9], payload)
        #because the 11th element in the tuple from send_packet is payload_len, this_packet[11] = payload_len
         
           
        return (newPacket, addr)
    
    
    def send_packet(self,packetToSend, address):
        my_struct = struct.Struct(sock352PktHdrData)
        print("type of payload", type(packetToSend.payload))
        packetToSendData = my_struct.pack(packetToSend.version, packetToSend.flags, packetToSend.opt_ptr, packetToSend.protocol, packetToSend.checksum, packetToSend.header_len, packetToSend.source_port, packetToSend.dest_port, packetToSend.sequence_no, packetToSend.ack_no, packetToSend.window, packetToSend.payload_len)
        
        self.socket.sendto(packetToSendData+packetToSend.payload, address)
        return



#creating a packet "struct"
class packet:
    def __init__(self,flags, header_len,sequence_no,ack_no,payload):     #initialize the packet
        self.version = 1 #0
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
        self.payload = payload #11
        self.payload_len = len(payload) # 12
        return    
 
