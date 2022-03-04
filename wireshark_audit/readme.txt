Using this script, all network data, packet count and traffic per protocol can be digested into InfluxDB. Packets using protocols such as ARP, TCP, UDP, DNS can be easily captured and processsed.


Dependencies needed to be installed - 

1. InfluxDB
2. Tshark
3. Wireshark
4. Python


Instructions to run network_data.py:

1. Run the following command on the terminal after installing TShark - "tshark -D". This will list all the interfaces on which we can capture. 

2. Run the following command on the terminal to start the script - "stdbuf -i0 -oL -e0 tshark -i [name of interface] -q -T fields -e frame.time_relative -e _ws.col.Protocol -e frame.len -e eth.src -e eth.dst -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport | python /home/sensorweb/NetworkData.py"

3. If the python script is in a different directory, please make sure you enter the full path to the script, as in the above example.

4. To stop the script, press ctrl+c.

Parameters - 
 
stdbuf -i0 -oL -e0 = To disable buffering of output
-i _______ = name of interface on which you want to capture
-q -T fields = Fields we want to display
-e frame.time_relative = Time at which packet was captured
-e _ws.col.Protocol = Name of protocol
-e eth.src = Source MAC address
-e eth.dst = Destination MAC address
-e frame.len = Length of packet
-e ip.src = Source IP address
-e ip.dst = Destination IP address
-e tcp.srcport = Source TCP port
-e tcp.dstport = Destination TCP port
-e udp.srcport = Source UDP port
-e udp.dstport = Destination UDP port

