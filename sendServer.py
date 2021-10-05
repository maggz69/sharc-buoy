import socket
import socketserver
import sys

file_name = "raw_data.csv"


def readData():
    file = open(file_name, "r")

    lines = 40
    data = ''.join(file.readlines()[0:lines])

    return data


# send data to listening server
def sendDataToPi(data):
    HOST, PORT = "192.168.0.154", 9999
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))

        # recv = sock.recv(1024)
        sock.close()

    print("Finished sending data to the socket \n\n",data)


if __name__ == "__main__":
    sendDataToPi(readData())