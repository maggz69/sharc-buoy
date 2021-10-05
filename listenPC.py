import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
requests_recieved = 0


def setupListeningServer():
    # create a socket and specify the address and ports
    HOST = ("0.0.0.0", 9998)
    sock.bind(HOST)

    # set the socket to accept incoming req
    sock.listen(1)
    print("PC Server listening")


    while requests_recieved < 2:
        connection, client_address = sock.accept()
        retrieveConnectionData(connection, client_address)


# Parse the recieved data to read the csv fil sent such that it can be sent back
def retrieveConnectionData(connection, client_address):
    global requests_recieved
    print("Some data has been recieved")
    requests_recieved += 1

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
    print("Chunks have been recieved")
    connection.close()

    data = b" ".join(fragments)

    print("Recieved data from\t{}".format(client_address))
    print("\n Data Recieved \n")

    print(data)

setupListeningServer()