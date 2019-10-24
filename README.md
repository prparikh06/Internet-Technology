# Internet-Technology
Projects implemented in CS352 at Rutgers University

For Project 1, we completed connect, accept, and close to take care of opening and closing connections between the client and the server. 
We used a helper recvACK method which uses the Python socket recvfrom function. As for send, we sent packets of size 32K or less. In recv, for every packets recevied, we added the packet to an array.
Back in send, if the previous index of the newest packet is None, then we know a packet has been missed. If so, resend all the packets (since the window size is infinite) by recursively calling send() again.
It was impossible to know if this works because during testing, we kept getting invalid syntax errors regarding the data received from the Python recvfrom() method.
Please have mercy on us :(

