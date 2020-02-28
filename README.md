# tcp-logger
This is a suit of Python scripts we use to log the output from Campbell Scientific CS135 lidar ceilometer.

The cceilometer communicates over RS232 (115200 n81) and a moxa NPORT (5150-T) converts this to communication over ethernet. The default IP of the moxa is 192:168:127:254.

The code run on a centos 6 laptop and "listens" to a given port and sves everything that comes in on it. It also adds a system timestamp to each line it reads in. 

1. Use "arp" to find the IP addresses of what the laptop is connected to. You will know the MAC address of the moxa so you can tack which is its IP address.
2. Find the IP address of assigened to the host.
3. Open up a web browser and enter the IP address for the moxa - this should take you to the NPORT interface.
4. Select Quick Setup
5. Note or give the name of the server.
6. On page 2 make sure the RealCOM radio button only is selected
7. On Page 2 under TCP - Destination IP enter the IP assigend to the host (not the one assigned to the NPORT). This is tel1ing the system where the data is going. Host should be on port 4002  
8. On Page 3 enter the baud, parity, number of bit, number of stop bits and the communications protocol being used.

In our usage we placed the sorce and compiled code in /opt/scripts

In this usage data is written to the directory /data/ncas-ceil-1. Edit line 15 in ceil_tcp_litener.py to chmge this. Files are .csv and created daily. The file naming is yyyymmdd_ceilometer.csv. Edit line 50 in ceil_tcp_litener.py to chnge this.

The code also automatically generates a log file.

