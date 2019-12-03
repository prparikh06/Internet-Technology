import binascii
import socket as syssock
import struct
import sys
import random
import math

port = -1
recv = -1
sock = (0, 0)
address = ''
curr = 0
sock352PktHdrData = '!BBBBHHLLQQLL'



version = 0x1
#flags
SOCK352_SYN = 0x01  
SOCK352_FIN = 0x02
SOCK352_ACK = 0x04
SOCK352_RESET = 0x08
SOCK352_HAS_OPT = 0xA0
SOCK352_FLAG = 0x05
opt_ptr = 0x0
protocol = 0x0
header_len = 40
checksum = 0x0
source_port = 0x0
dest_port = 0x0
sequence_no = 0x0
ack_no = 0x0
window = 0x0
data = ''


# this init function is global to the class and
# defines the UDP ports all messages are sent
# and received from.
def init(UDPportTx, UDPportRx):     # initialize your UDP socket here 
    global sock, port, recv
    print("Waiting for client connection")
    #create the socket
    sock = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
    recv = int(UDPportRx)
    #checks if empty
    if(UDPportTx == ''):
        port = recv
    else:
        #creates the port
        port = int(UDPportTx) 
    #binds the socket to the port
    sock.bind(('', recv))
    #sets the timeout
    sock.settimeout(.2)
    return


class socket:

    def __init__(self):     # fill in your code here 
        #nothing needed here
        return

    def bind(self, address):
        #not used for part of project
        pass
        return

    def connect(self, address):     # fill in your code here 
        global sock, curr, sock352PktHdrData, header_len, version, opt_ptr, protocol, checksum, \
            source_port, dest_port, window

        #current sequence number set to a random int
        curr = random.randint(10, 100)

        #create the header
        header1 = struct.Struct(sock352PktHdrData)  

        flags = SOCK352_SYN
        sequence_no = curr
        ack_no = 0
        payload_len = 0

        #create packet header
        header = header1.pack(version, flags, opt_ptr, protocol,
                                    header_len, checksum, source_port, dest_port, sequence_no,
                                    ack_no, window, payload_len)

        ACKFlag = -1

        # create the packet 
        while(ACKFlag != curr):
            sock.sendto(header,(address[0], port))
            newHeader = self.packet()
            ACKFlag = newHeader[9]

        #connect 
        sock.connect((address[0], port))

        curr += 1
        print("Connection achieved")
        return

    def listen(self, backlog):
        pass
        return

    def accept(self):
        global sock, recv, curr
        flag = -1
        newHeader = ""

        while(flag != SOCK352_SYN):
            #call packet until we get a new connection
            newHeader = self.packet()
            flag = newHeader[1]
        curr = newHeader[8]

        ####################
        # create a new header
        header1 = struct.Struct(sock352PktHdrData)

        flags = SOCK352_ACK
        sequence_no = 0
        ack_no = curr
        payload_len = 13

        header = header1.pack(version, flags, opt_ptr, protocol,
                              header_len, checksum, source_port, dest_port, sequence_no,
                              ack_no, window, payload_len)
        ##################
        sock.sendto(header + " accepted", address)

        curr += 1
        print("Target acquired")
        clientsocket = socket()
       # (clientsocket, address) = (1,1)     # change this to your code
        return (clientsocket, address)      
    
    def close(self):    # fill in your code here 

        #create temporary sequence number
        temp = random.randint(10, 100)

        ###################
        # create a new header
        header1 = struct.Struct(sock352PktHdrData)

        flags = SOCK352_FIN
        sequence_no = temp
        ack_no = 0
        payload_len = 0

        header = header1.pack(version, flags, opt_ptr, protocol,
                              header_len, checksum, source_port, dest_port, sequence_no,
                              ack_no, window, payload_len)

        ####################
        # sets the timeout and waits to see if theres a FIN packet
        ACKFlag = -1
        while(ACKFlag != temp):
            try:
                sock.sendto(header, address)
            except TypeError:
                sock.send(header)
            newHeader = self.packet()
            ACKFlag = newHeader[9]
        sock.close()
        print("Connection closed")
        return

    def send(self, buffer):
        global sock, header_len, curr

        bytessent = 0       # fill in your code here 
        length = len(buffer)

        while(length > 0):
            message = buffer[:255]
            #Take the top 255 bytes of the message because
            #thats the max payload we represent with a "B"
            ######################
            # create a new header
            header1 = struct.Struct(sock352PktHdrData)

            flags = 0x05
            sequence_no = curr
            ack_no = 0
            payload_len = len(message)

            pHeader = header1.pack(version, flags, opt_ptr, protocol,
                                  header_len, checksum, source_port, dest_port, sequence_no,
                                  ack_no, window, payload_len)
            ######################
            temp = 0
            ACKFlag = -1
            while(ACKFlag != curr):
                temp = sock.send(
                    pHeader + message) - header_len

                newHeader = self.packet()
                ACKFlag = newHeader[9]

            length -= 255
            buffer = buffer[255:]
            bytessent += temp
            curr += 1
        print("Segment of %d bytes was sent" % bytessent)
        return bytessent

    def recv(self, nbytes):
        global sock, data, curr

        data = ""
        bytesreceived  = ""
        while(nbytes > 0):
            seq_no = -1
            #Keep checking the incoming packets until we get
            #one with the sequence number we specified eralier
            while(seq_no != curr):
                newHeader = self.packet()
                seq_no = newHeader[8]
            
                ###############
                # create new header
                header1 = struct.Struct(sock352PktHdrData)

                flags = SOCK352_ACK
                sequence_no = 0
                ack_no = seq_no
                payload_len = 0

                header = header1.pack(version, flags, opt_ptr, protocol,
                                      header_len, checksum, source_port, dest_port, sequence_no,
                                      ack_no, window, payload_len)
                ###############
                sock.sendto(header, address)
            bytesreceived  += data
            nbytes -= len(data)
            
            curr += 1
        print("Finished receiving the specified amount.")
        return bytesreceived 

    # Packet class
    def packet(self):
        global sock, sock352PktHdrData, address, data
        # attempts to recv packet if not will print error message
        try:
            (data, dest) = sock.recvfrom(4096)
        except syssock.timeout:
            print("No packets received, timeout window maxed")
            head = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            return head

        # unpacks the 
        (data, message) = (data[:40], data[40:])
        header = struct.unpack(sock352PktHdrData, data)
        flag = header[1]

        # checks serveral flag conditions as listed in the specs
        if(flag == SOCK352_SYN):
            address = dest
            return header
        elif(flag == SOCK352_FIN):
            ###############
            # create header
            header1 = struct.Struct(sock352PktHdrData)

            flags = SOCK352_ACK
            sequence_no = 0
            ack_no = header[8]
            payload_len = 0

            terminalHeader = header1.pack(version, flags, opt_ptr, protocol,
                                  header_len, checksum, source_port, dest_port, sequence_no,
                                  ack_no, window, payload_len)
            ###############
            sock.sendto(terminalHeader, dest)
            return header

        elif(flag == SOCK352_FLAG):
            data = message
            return header
        elif(flag == SOCK352_ACK):
            return header

        elif(flag == SOCK352_RESET):
            return header

        else:

            #####################
            # create header
            header1 = struct.Struct(sock352PktHdrData)

            flags = SOCK352_RESET
            sequence_no = header[8]
            ack_no = header[9]
            payload_len = 0

            header = header1.pack(version, flags, opt_ptr, protocol,
                                  header_len, checksum, source_port, dest_port, sequence_no,
                                  ack_no, window, payload_len)
            #####################
            if(sock.sendto(header, dest) > 0):
                print("Reset packet sent")
            else:
                print("Reset packet failed to send")
            return header
# import binascii
# import socket as syssock
# import struct
# import sys
# import random
# import time


# MAX_PACKET_SIZE = 32000
# sock352PktHdrData = '!BBBBHHLLQQLL' 
# DEFAULT = 5299
# header_len = struct.calcsize(sock352PktHdrData)



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

#     print("portTx = sending port: ", portTx, "portRx = receiving port: ", portRx)   
#     pass 
    
# class socket:
#     def __init__(self):  # fill in your code here 
#         #make a UDP socket as defined in the Python library
#         self.socket = syssock.socket(syssock.AF_INET, syssock.SOCK_DGRAM)
#         #self.socket.settimeout(0.2) #set the timeout 
#         self.connected = False #boolean to keep track of open connection
#         self.packets = [] #list to keep track of data sent
        
#         return
    
#     def bind(self,address):
#         global portRx
#         self.recv_addr = (address[0], int(portRx))
#         self.socket.bind(self.recv_addr)
        
        
#     #establish the connection - 3 way handshake
#     #TCP: step 1: connect - random number for sequence_no, flag = SYN, send packet to server
#     #step 2: accept - receive the packet - sequence_no = new random, flag = SYN | ACK, ack_no = old sequence_no + 1, send to client
#     #step 3: connect & accept- receive the packet - ack_no = seq_no + 1
#     #NOTE: address is of type in form {destination IP, port} that client passes in

#     def connect(self,address):  # fill in your code here 
#         global portRx, portTx
#         print("header len: ", header_len)
#         if self.connected: #return error
#             print ("Client has already connected to server")
        
#         destination = address[0] 
        
#         print ("get hostname:",syssock.gethostname()) 
                
#         self.recv_addr = (syssock.gethostname(), int(portRx)) #receiving = client
#         self.send_addr = (destination, portTx) # sending = server
        
#         self.socket.bind(self.recv_addr)
#         print("initiating 3 way handshake!")

#         #STEP 1: send from client
#         randSeq = random.randint(1,100) #establish random sequence
#         print ("random int: ", randSeq)
#         #initialize, pack, and send the syn packet 
#         initialPacket = packet(SYN,header_len,randSeq,0,0)
#         self.send_packet(initialPacket,self.send_addr)

#         #STEP 3: recv ACK from server, send final ACK
#         syn_ack_packet, addr = self.recv_packet()
#         print("recvd syn_ack")
#         flags = syn_ack_packet.flags
#         print(flags)
#         #check flags
#         if flags == SYN | ACK:
#             print("step 3")
#             final_packet = syn_ack_packet
#             final_packet.ack_no = final_packet.sequence_no + 1
#             self.send_packet(final_packet, self.send_addr)
#             print("should be done!!")
            
        
#         elif flags == RESET:
#             print ("something went wrong so connection has been reset")
#             return
        
#         print("connecting...!")
#         return 
    
#     def listen(self,backlog):
#         return

#     #accept the connection
#     def accept(self):
#         global portTx

#         print("ready to accept")
#         #STEP 2: server receives SYN and sends SYN-ACK in return    
#         initialPacket, addr = self.recv_packet()
#         flags = initialPacket.flags
#         self.send_addr = (addr[0], int(portTx))
#         print(flags)
        
#         if flags == SYN: 
#             ack_no = initialPacket.sequence_no + 1
#             randSeq = random.randint(1,100)
#             seq_no = randSeq
#             flags = SYN | ACK
#             syn_ack_packet = packet(flags,header_len,seq_no,ack_no,0)
            
#             self.send_packet(syn_ack_packet,self.send_addr)
            
#         else: #pack and send the packet reset
#             initialPacket.flags = RESET
#             self.send_packet(initialPacket,self.send_addr)
#             return
                 
#         #STEP 3 CONTD
#         final_packet, addr = self.recv_packet()
        
#         self.connected = True

#         print ("Accepted!")
       
#         return (self, self.send_addr) 

#     def close(self):   # fill in your code here
        
#     #    #Step 1 client sends FIN
#     #     cPacket = packet()
#     #     cPacket.sequence_no = rand.rand()
#     #     cPacket.flags = {FIN}
#     #     cPacket.ack_no = 0 #TODO
#     #     cPacket.payload_len = 0 #TODO

#     #     clientPacketHeader = struct.Struct(sock352PktHdrData)
#     #     clientHeader = clientPacketHeader.pack(cPacket.version,cPacket.flags, cPacket.sequence_no, cPacket.ack_no, cPacket.payload_len)
        
#     #     self.mySock.sendto(clientHeader,portRx)

#     #   #STEP 2 & 3: server receives FIN and sends FIN-ACK back
#     #     (sPacket, address) = self.recvfrom()
#     #     sPacket.sequence_no = rand.rand()
#     #     sPacket.flags = {FIN, ACK}
#     #     sPacket.ack_no = sPacket.sequence_no + 1
#     #     sPacket.payload_len = 0 #TODO

#     #     serverHeader = sock352PktHdrData.pack(sPacket.flags, sPacket.sequence_no, sPacket.ack_no,cPacket.payload_len)
#     #     self.mySock.sendto(serverHeader,portTx)


#     #     #Step 4: client sends back an ACK
#     #     cPacket.sequence_no = sPacket.ack_no
#     #     cPacket.ack_no = sPacket.sequence_no + 1
#     #     cPacket.flags = {ACK}

#     #     (sPacket, address) = self.recvACK()
#     #     sPacket.sequence_no = rand.rand()
#     #     sPacket.ack_no = cPacket.ack_no + 1


#     #     #need to return (s2,address)
#     #     print("Closing the connection")
        
#     #     self.mySock.close()
#         return  

#     def send(self,buffer):  # fill in your code here 
#         #buffer = file contents
#         #bytessent should be size of what we can handle 
#         bufferIndex = len(buffer)
#         bytessent = 0
#         # packetIndex = 0
#         # while bytessent < bufferIndex:
#         # #buffer is larger than max
#         #     try:
                
#         #         #TODO send the info using sendto? --make packet that will actually get sent
#         #         if (packetIndex == 0): #first packet getting sent
#         #             self.mySock.sendto(buffer[bytessent: MAX_PACKET_SIZE],portRx)
#         #             bufferIndex -= MAX_PACKET_SIZE
#         #             bytessent += MAX_PACKET_SIZE
#         #             continue

#         #         if (packetIndex > 0): #not the first packet
#         #             #check for GBN
#         #             if (packets[packetIndex-1] == None): #TODO #if there was no packet recvd before it/aka not been sent properly
#         #                 #do go back n ? send everything again? recursively redo
#         #                 packets.clear()
#         #                 socket.send(self,buffer)
                            
#         #             else: 
#         #                 self.mySock.sendto(buffer[bytessent: MAX_PACKET_SIZE],portRx)
#         #                 bufferIndex -= MAX_PACKET_SIZE
#         #                 bytessent += MAX_PACKET_SIZE
#         #             continue
                          
#         #     except syssock.timeout:
#         #         pass
#         return bytessent 
    

#     def recv(self,nbytes):
#         bytesreceived = 0     # fill in your code here
               
#         # while bytesreceived < nbytes:
#         #     try:
#         #         currPacket = self.mySock.recv(min(nbytes - bytesreceived, MAX_PACKET_SIZE))
#         #         packets.append(currPacket)
#         #         bytesreceived = bytesreceived + len(packet)
            
            
#         #     except syssock.timeout:
#         #         pass
#         return bytesreceived
    
    
#     def recv_packet(self):
#         syn_ack_packet_data,addr = self.socket.recvfrom(header_len)
#         syn_ack_packet = struct.unpack(sock352PktHdrData, syn_ack_packet_data)
        
#         newPacket = packet(syn_ack_packet[1], syn_ack_packet[5], syn_ack_packet[8], syn_ack_packet[9], syn_ack_packet[11])
#         return (newPacket, addr)
    
    
#     def send_packet(self,packetToSend, address):
#         packetToSendData = struct.pack(sock352PktHdrData,packetToSend.version, packetToSend.flags, packetToSend.opt_ptr, packetToSend.protocol, packetToSend.header_len, packetToSend.checksum, packetToSend.source_port, packetToSend.dest_port, packetToSend.sequence_no, packetToSend.ack_no, packetToSend.window, packetToSend.payload_len)
#         self.socket.sendto(packetToSendData, address)
#         return



# #creating a packet "struct"
# class packet:
#     def __init__(self,flags, header_len,sequence_no,ack_no,payload_len):     #initialize the packet
#         self.version = 0x1 #0
#         self.flags = flags #1
#         self.opt_ptr = 0 #2
#         self.checksum = 0 #3 TODO what is this
#         self.protocol = 0 #4
#         self.header_len = header_len #5
#         self.source_port = 0 #6
#         self.dest_port = 0 #7
#         self.sequence_no = sequence_no #8
#         self.ack_no = ack_no #9
#         self.window = 0 #10
#         self.payload_len = payload_len #11
#         return    
 
