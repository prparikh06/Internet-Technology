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
        self.lock = Lock() 
	#both have to be 0 since ther are of type Q in header file (unsigned)
        self.timeout_occurred = False
        return
    
    def bind(self,address):
        global portRx
        self.recv_addr = (address[0], int(portRx))
        self.socket.bind(self.recv_addr)

    def connect(self,address):  # fill in your code here  
        global portRx, portTx
        self.recv_addr = (syssock.gethostname(), int(portRx))
        self.socket.bind(self.recv_addr)
        self.send_addr= (str(address[0]), int(portTx))
        self.socket.settimeout(0.2)
        done = False
        self.ack = random.randint(1,1000)
        while not done:
            self.send_packet2(seq_no = self.ack, flags=SYN)
            syn_ack = self.recv_packet2()
            if syn_ack['flags'] == SYN | ACK:
                done = True
                self.seq = syn_ack['seq_no'] + 1
                self.ack = syn_ack['ack_no']
                self.send_packet2(ack_no=self.seq, flags=ACK)
        self.connected = True 
        return
                
    def listen(self,backlog):
        return

    #accept the connection
    def accept(self):
        global portTx
        done= False
        while not done:
            first_packet = self.recv_packet2()
            if first_packet['flags'] == SYN:
                done = True
                self.seq = first_packet['seq_no'] + 1
            else:
                self.send_packet2(dest=first_packet['address'], ack_no= self.seq, flags=RESET)
            self.socket.settimeout(0.2)
            self.send_addr = (first_packet['address'][0], int(portTx))
            done = False
            self.ack = random.randint(1,1000)
            while not done:
                self.send_packet2(seq_no = self.ack, ack_no=self.seq, flags=SYN | ACK)
                second_packet = self.recv_packet2()
                if second_packet['flags'] == ACK and second_packet['ack_no'] == self.ack + 1:
                    self.ack = second_packet['ack_no']
                    done = True
                else:
                    self.send_packet2(ack_no=self.ack, flags=RESET)
        return (self,self.send_addr)  

 
    def close(self):   # fill in your code here
        self.socket.settimeout(0.2)
        fin_sent = False
        while not self.closed or not fin_sent:
            self.send_packet2(seq_no=self.seq, flags=FIN)
            fin_pack = self.recv_packet2()
            flag = fin_pack['flags']
            if flag == FIN:
                self.send_packet2(ack_no=fin_pack['seq_no']+1, flags=ACK)
                self.closed = True
            elif flag == ACK and fin_pack['ack_no'] == self.seq + 1:
                fin_sent = True

        self.socket.settimeout(1)
        timeout = 0
        while True:
            fin_pack = self.recv_packet2()
            timeout = fin_pack['payload_len']
            if timeout == -1:
                return
            else:
                if fin_pack['flags'] == FIN:
                    self.send_packet2(ack_no=fin_pack['seq_no']+1, flags=ACK)



    def send(self,buffer):  # fill in your code here 
        if not self.connected:
            print("client has not connected with socket :(")
            return -1
        elif self.closed:
            print("connection has already been closed")
            return -1
        print("how much we need to send: ", len(buffer))
        final_ack = len(buffer) + self.ack   #what our final ack should be
        bytesLeft = len(buffer) #bytes left to send
        self.socket.settimeout(0.2)
        #we want to have a thread to keep track of all the acks recvd, which is different function
        ack_thread = Thread(target=self.recv_ack, args = (final_ack,))
#        curr_ack = len(buffer)
        start_ack = self.ack
        curr_ack = self.ack
        ack_thread.start()
        while ack_thread.isAlive():
            with self.lock:
                if self.timeout_occurred: #if timeout occurred, GBN
                     curr_ack = self.ack #reset ack 
                     self.timout_occurred = False
            if curr_ack >= final_ack: 
                curr_ack = max(curr_ack-MAX_PACKET_SIZE, start_ack)
            startIndex = curr_ack - start_ack
            bytesLeft = final_ack - curr_ack
            endIndex = startIndex + min(bytesLeft, MAX_PACKET_SIZE)
            payload = buffer[startIndex : endIndex]
            payload_len =  len(payload)
            #send payload packet
            self.send_packet2(seq_no=curr_ack, payload=payload)         
            curr_ack += payload_len #update the current ack by adding however many bytes we sent
            
        return len(buffer) 
    

    def recv(self,nbytes):
        packets_recvd = 0     # fill in your code here
        packets = []
        self.socket.settimeout(None)
        packets_to_send = int(math.ceil(float(nbytes)/MAX_PACKET_SIZE))
        print("we need to send ", packets_to_send, "packets to send all ", nbytes, "nbytes")
        packet_size = 0
        while packets_recvd < packets_to_send:
            if packets_recvd  == packets_to_send - 1:
                packet_size = header_len + nbytes - ((packets_to_send-1) * MAX_PACKET_SIZE)
            else: 
                packet_size = header_len + MAX_PACKET_SIZE

            curr_packet = self.recv_packet2(size=packet_size)
            payload = curr_packet['payload']
            #print("recvd packet,payload size =  ",len(payload),". should match packet size?????:",packet_size)
            if curr_packet['flags'] != 0:

                print("flag was not 0, nbd")

            elif curr_packet['seq_no'] == self.seq:
                self.seq += payload
                packets.append(payload) 
                packets_recvd += 1
                
                print("packet", packets_recvd, "of ", packets_to_send,"recvd")
                
            self.send_packet2(ack_no=self.seq, flags=ACK)
        
        final_str = b''.join(packets)
        print("finsl string = ",final_str)
        print("packets", packets)
        print(len(final_str))
        return final_str
                
    
    def recv_ack(self,ack_no):
        
        print("ack = ",ack_no)
        timer = time.time()
        while self.ack < ack_no:
            curr_packet = self.recv_packet2(timeout_func=self.register_timeout)
            flag = curr_packet['flags']
            if flag == ACK:
                if curr_packet['ack_no'] > self.ack:
                    with self.lock:
                        self.ack = curr_packet['ack_no'] 
                    timer = time.time()
            elif flag == RESET:
                self.send_packet2(ack_no=self.seq,flags=ACK)
            elif flag == FIN: #done sending
                self.closed = True
                self.send_packet2(ack_no=curr_packet['seq_no'] + 1, flags=ACK)
                return
            if time.time() - timer > 0.2:
               self.register_timeout() 



    def register_timeout(self):
        with Lock():
            self.timeout = True

    
    def doNothing():
        pass
    
    def recv_packet2(self, size=header_len, timeout_func = doNothing):
        try:
            packet, addr = self.socket.recvfrom(size)
        except syssock.timeout:
            timeout_func()
            return dict(zip(('version', 'flags', 'opt_ptr', 'protocol', 'checksum', 'header_len', 'source_port', 'dest_port', 'seq_no', 'ack_no', 'window', 'payload_len', 'payload', 'address'), (-1 for i in range(14))))
        
        header = packet[:header_len]
        header_values = struct.unpack(sock352PktHdrData,header)
        if len(packet) > header_len:
            payload = packet[header_len:]
    	
        else:
    	    payload = 0
        
        return_values = header_values + (payload, addr)
    	
        return_dict = dict(zip(('version', 'flags', 'opt_ptr', 'protocol', 'checksum', 'header_len','source_port', 'dest_port', 'seq_no', 'ack_no', 'window', 'payload_len', 'payload', 'address'), return_values))
    	
        return return_dict
    
    def send_packet2(self, dest=None, seq_no=0, ack_no=0, payload = b'', flags=0):
        if dest == None:
            dest = self.send_addr
        version = 1
        opt_ptr = 0
        protocol = 0
        checksum = 0
        source_port = 0
        dest_port = 0
        window = 0
        payload_len = len(payload)
        HEADER_LEN = header_len
        header = struct.pack(sock352PktHdrData,version, flags, opt_ptr, protocol, checksum, HEADER_LEN, source_port, dest_port, seq_no, ack_no, window, payload_len)
        packet = header + payload
        self.socket.sendto(packet, self.send_addr)


