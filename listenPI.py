import csv
import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def setupListeningServer():
    # create a socket and specify the address and ports
    HOST = ("localhost", 9999)
    sock.bind(HOST)

    # set the socket to accept incoming req
    sock.listen(1)
    print("Server listening")

    while True:
        connection, client_address = sock.accept()
        retrieveConnectionData(connection, client_address)


# Parse the recieved data to read the csv fil sent such that it can be sent back
def retrieveConnectionData(connection, client_address):
    print("Some data has been recieved")
    fragments = []
    iterations = 1
    while True:
        try:
            chunk = connection.recv(4096)
            if not chunk:
                print("Chunk closed")
                break
            fragments.append(chunk)
            iterations +=1
        except:
            print("Exception occurred")
    print("Chunks hae been recieved")
    connection.close()

    print("Recieved data from\t{}".format(client_address))
    print("\n Data Recieved \n")
    print(b" ".join(fragments))


# read csv data into list of lists
def readData():
    # Reads each row of CSV file; skips headers
    file = open("raw_data.csv")  # Set this name to the name of the file received
    csvreader = csv.reader(file)
    csvData = []
    for line in csvreader:
        csvData.append(line)

    file.close()

    # Rows are read from CSV file as lists; this converts them to string and splits them to get list of lists
    data = []
    for i in range(len(csvData)):
        if i > 1:
            data.append(str(csvData[i]).split()[1:-1])

    # The last line contains string "computer utc end etc"; remove to perform fft
    data.remove(data[-1])
    # return data


# Placing data into a buffer after reading as the data is read as list of lists
# Zlib library cannot work with lists (only uses byte-type data) hence textfile
# Can send this buffer file back to pi for compression/enryption
# *** Temporary solution ***
def buffer(input):
    file = open("buffer.txt", "w")
    for ele in input:
        for i in range(len(ele)):
            if i == len(ele) - 1:
                file.write(ele[i] + "\n")
            else:
                file.write(ele[i] + ", ")
    file.close()


if __name__ == "__main__":
    print("Setting up a server :)")
    setupListeningServer()
