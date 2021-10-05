import csv
import socket
import sys
from scipy.fft import fft, fftfreq
import numpy as np
import matplotlib as plt


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
requests_recieved = 0

debug_graphs  = False


def setupListeningServer():
    # create a socket and specify the address and ports
    HOST = ("localhost", 9999)
    sock.bind(HOST)

    # set the socket to accept incoming req
    sock.listen(1)
    print("Server listening")


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
            chunk = connection.recv(409600)
            if not chunk:
                print("Chunk closed")
                break
            fragments.append(chunk)
            iterations +=1
        except:
            print("Exception occurred")
    print("Chunks hae been recieved")
    connection.close()

    data = b" ".join(fragments)

    print("Recieved data from\t{}".format(client_address))
    # print("\n Data Recieved \n")

    # print(data)

    output_fourier =  readData(data)

    file  = open('compressed_data.txt','w')
    for row in output_fourier:
        file.write(str(row))
        file.write("\n")
        
    file.close()


# read csv data into list of lists
def readData(data):
    # break the byte data into lines
    
    split_data = data.split(b"\n")
    line_data = split_data[1:-1]

    # The last line contains string "computer utc end etc"; remove to perform fft

    data = []
    dataTypes = None

    for i in range(len(line_data)-1):
        try:
            if i==0:
                dataTypes = [x.strip() for x in (str(line_data[i]).split(",")[1:])]
            else:
                # dateTime = str(line_data[i]).split()[0:1][0][2:]
                row = str(line_data[i]).split(" ")[1:-1]
                data.append(np.double(row))
        except:
            print(f":( {i}")

    # Removes unwanted string elements (whitespace, etc.) from data types
    for i in range(len(dataTypes)):
        dataTypes[i] = dataTypes[i][2:-1]

    times = []
    for i in range(len(data)):
        times.append(i)

    return compress(data, times, dataTypes) 

# Placing data into a buffer after reading as the data is read as list of lists
# Zlib library cannot work with lists (only uses byte-type data) hence textfile
# Can send this buffer file back to pi for compression/enryption
# *** Temporary solution ***
# def buffer(input):
#     file = open("buffer.txt", "w")
#     for ele in input:
#         for i in range(len(ele)):
#             if i == len(ele) - 1:
#                 file.write(ele[i] + "\n")
#             else:
#                 file.write(ele[i] + ", ")
#     file.close()

def compress(inputData, inputTimes, dataHeaders):
    N = len(inputTimes)
    T = 1/N

    inputDataf = [] # fft(inputData)

    for row in inputData:
        inputDataf.append(fft(row))

    
    
    outputDataf = lowpass(inputDataf)
    
    # Plot graphs if debugging graphs is switched on

    if debug_graphs:
        # For plotting FFT data graph
        # Before plotRaw() and compress()
        fig, axs = plt.subplots(3)
        fig.suptitle("IMU Data: Raw, FFT and Compressed FFT")

        for i in range(len(inputData[0])):
            axs[0].plot(inputTimes, [y[i] for y in inputData], label = "%s"%dataHeaders[i])

        xf = fftfreq(N, T)[:N//2]

        axs[1].plot(xf, 2/N * np.abs(inputDataf[0:N//2]))
        axs[1].grid()

        # For plotting compressed data graph
        xf = inputTimes[0:len(outputDataf)]
        axs[2].plot(xf, 2/N * np.abs(outputDataf[0:N//2]))
        axs[2].grid()

        # After plotRaw() and compress()
        fig.legend()
        plt.show()

    
    # Returns compressed fourier transform data
    return outputDataf

def lowpass(fftData):
    # Will further test butterworth low pass filter from scipy.signal library
    
    compressFFT = []
    coeffs = len(fftData)//3
    for i in range(coeffs):
        compressFFT.append(fftData[i])
    
    return compressFFT

if __name__ == "__main__":
    print("Setting up a server :)")
    setupListeningServer()
