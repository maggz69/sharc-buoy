import socket
import socketserver
import sys

file_name = "raw_data.csv"


def readData():
    file = open(file_name, "r")
    return file.read()


# send data to listening server
def sendDataToPi(data):
    HOST, PORT = "localhost", 9999
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(bytes(data + "\n", "utf-8"))

        sock.close()

    print("Finished sending data to the socket")


if __name__ == "__main__":
    sendDataToPi(readData())