## Running the code
1. Start the `listenPI.py` server
2. Start the `listenPC.py` server
3. Run the `sendServer.py` code

The `sendServer.py` will read the data from the CSV and send it to the PI through TCP Sockets. 

This will then be read into the PI, compressed, encrypted and returned back to the PC that will be listening in on a defined port and the original IP address that was used to send the data from.