
import binascii
import socket as syssock
import struct
import sys
import random
import time
from threading import Thread, Lock
from math import ceil


#creating a packet "struct"
class packet:
# these functions are global to the class and
# define the UDP ports all messages are sent
# and received from

SYN = 0x01 #Connection Initiation
FIN = 0x02 #Connection End
ACK = 0x04 #Connection Acknowledgement 
RESET = 0x08 #Reset Connection
HAS_OPT = 0xA0 # Option Field is valid
MAX_PAYLOAD_SIZE = 32000
header_len = 40
packet_size = MAX_PAYLOAD_SIZE
DEFAULT = 5299


def init(UDPportTx,UDPportRx):   # initialize your UDP socket here 
    #global port nums
    global send_port #transmit = UDPportTx
    global recv_port #receiving = UDPportRx

    if int(UDPportTx) == 0:
        portTx = DEFAULT
    elif int(UDPportRx) == 0:
        portRx = DEFAULT
    else:
        send_port = int(UDPportTx)
        recv_port = int(UDPportRx)
    pass 
    
class socket:
    def __init__(self):  # fill in your code here 
        #make a UDP socket as defined in the Python library
        global mySock
        global packet
        
        
        sock352PktHdrData = '!BBBBHHLLQQLL'
        self.struct = struct.Struct(sock352PktHdrData)
        self.mySock = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
        self.rn = 0
        self.my_rn = 0
        self.done = false
        self.lock = Lock()
        self.timeout = False  
 
        return
    
    def bind(self,address):
        global recv_port
        self.recv_address = (address[0], int(recv_port))
        self.socket.bind(self.recv_address
        return 
        
    #establish the connection - 3 way handshake
    def connect(self,address):  # fill in your code here  
        global send_port, recv_port
        self.recv_address = (syssock.gethostname(), int(recv_port))
        self.socket.bind(self.recv_address[0]), int(send_port))
        self.socket.settimeout(0.2)
        done = False
        self.rn = randint(1,1000)
        while not done:
            self.send_packet(seq_no = self.rn, flags=SYN)
            syn_ack = self.get_packet()
            if syn_ack['flags'] == SYN | ACK:
                done = True
                self.my_rn = syn_ack['seq_no'] + 1
                self.rn = syn_ack['ack_no']
                self.send_packet(ack_no=self.my_rn, flags=ACK)
         return
            
        
        #DONE UP UNTIL HERE!!!!**************************
    
    def listen(self,backlog):
        return

    #accept the connection
    def accept(self):
    
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
        
        
        #need to return (s2,address)
        return 

    
    
    
    def close(self):   # fill in your code here 
        self.socket.settimeout(.2)
        fin_sent = False
        while not self.done or not fin.sent:
            self.send_packet(seq_no=self.my_rn, flags=SOCK352_FIN)
            fin_pack = self.get_packet()
            if fin_pack['flags'] == SOCK352_FIN:
                self.send_packet(ack_no = fin_pack['seq_no']+1, flags=SOCK352_ACK)
                self.done = True
                elif fin_pack['flags'] == SOCK352_ACK and fin_pack['ack_no'] == self.my_rn + 1:
                    fin_sent = True
                self.socket.settimeout(1)
                timeout = 0
                while True:
                    fin_pack = self.get_packet()
                    timeout = fin_pack['payload_len']
                    if timeout == -1:
                        return
                    else:
                        if fin_pack['flags'] == SOCK352_FIN:
                            self.send_packet(ack_no = fin_pack['seq_no'] + 1, flags=SOCK352_ACK)
                     
                     

    def send(self,buffer):  # fill in your code here 
        self.socket.settimeout(0.2)
        goal = self.rn + len(buffer)
        ack_thread = Thread(target=self.recv_acks, args=(goal,))
        num_left = len(buffer)
        start_rn = self.rn
        imagined_rn = self.rn
        ack_therad.start()
        while ack_thread.isAlive():
            with self.lock:
                if self.timeout:
                    imagined_rn = self.rn
                    self.timeout = False
            if imagined_rn >= goal:
                imagined_rn = max(imagined_rn - MAX_PAYLOAD_SIZE, start_rn)
            start_index = imagined_rn - start_rn
            num left = goal - imagined_rn
            end_index = start_index + min(num_left, MAX_PAYLOAD_SIZE)
            payload = buffer[start_index : end_index]
            self.send_packet(seq_no = imagined_rn, payload=payload)
            imagined_rn += len(payload)
            return len(buffer)
        
    

    def recv(self,nbytes):
        good_packet_list = []
        self.socket.settimeout(None)
        goal_length = int(ceil(float(nbytes) / MAX_PAYLOAD_SIZE)
        while len(good_packet_list) < goal_length:
              if len(good_packet_list) == goal_length - 1:
                 num_to_get = header_len + nbytes - ((goal_length - 1) * MAX_PAYLOAD_SIZE)
              else:
                  num_to_get = header_len + MAX_PAYLOAD_SIZE
              data_pack = self.get_packet(size=num_to_get)
              if data_pack['flags'] != 0:
                 print('Probably getting extra from ahndshake', data_pack['flags'])
              elif data_pack['seq_no'] == self.my_rn:
                   self.my_rn += data_pack['payload'])
              self.send_packet(ack_no = self.my_rn, flags=ACK)
              final_string = b''.join(good_packet_list)
              return final_string;
    def register_timeout(self):
        with self.lock:
            self.timeout = True
    def recv_acks(self, goal_rn):
        timer = time.time()
        while self.rn < goal_rn:
            ack_pack = self.get_packet(timeout_func=self.register_timeout)
            if ack_pack['flags'] == SOCK352_ACK:
                if ack_pack['ack_no'] > self.rn:
                    with self.lock:
                        self.rn = ack_pack['ack_no']
                        timer = time.time()
            elif ack_pack['flags'] == SOCK352_RESET:
                self.send_packet(ack_no=self.my_rn, flags=SOCK352_ACK)
            elif ack_pack['flags'] == SOCK352_FIN:
                self.done = True
                self.send_packet(ack_no=ack_pack['seq_no'] + 1, flags=SOCK352_ACK)
                return
            if time.time() - timer > .2:
                
                
        
                        
                          #FINISH recv acks? accept and close**************************************************************
        



