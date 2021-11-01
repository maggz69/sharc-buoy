import numpy
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES,DES,PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
import time
import sys
import json
import matplotlib.pyplot as plt
import pandas

rows_to_gen = 3600
key = b'0123456789012345'
iv = key

def compareAllAlgo():
    rsa_data = pandas.read_csv('rsa_cbc_time_comparison.csv')
    aes_data = pandas.read_csv('aes_cbc_time_comparison.csv')
    des_data = pandas.read_csv('des_cbc_time_comparison.csv')

    

    chart_plot_1 = aes_data.plot.scatter(x='rows',y='encryption_elapsed_time',c='Blue',marker='+')

    rsa_data.plot.scatter(ax=chart_plot_1,x='rows',y='encryption_elapsed_time',c='Orange',marker='+')
    
    des_data.plot.scatter(ax=chart_plot_1,x='rows',y='encryption_elapsed_time',c='Yellow',marker='+')

    plt.title("Comparing all the different algorithms")
    plt.legend(['AES','RSA','DES'])
    plt.savefig('all_encryption_comparison.png')

def runAES():
    timing_results = []

    for i in range(rows_to_gen):

        case = numpy.random.rand(i+1, 9)

        case_str = numpy.array_str(case)

        start_time = time.perf_counter()

        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(bytes(case_str, encoding="utf-8"), 16))

        end_time = time.perf_counter()

        timing_results.append({
            'rows': i+1,
            'input_data_size': sys.getsizeof(case_str),
            'output_data_size': sys.getsizeof(str(ciphertext)),
            'encryption_elapsed_time': (end_time - start_time)})


    data = pandas.DataFrame.from_dict(timing_results)
    chart_plot = data.plot(x='rows',y='encryption_elapsed_time')

    plt.ylabel('Time in s')
    plt.xlabel('Rows of Sensor Data')
    plt.savefig('aes_cbc_time_comparison.png')

    data  = data.sort_values(by=['encryption_elapsed_time','rows'])
    data.to_csv('aes_cbc_time_comparison.csv',mode='w+')

def runRSA():
    timing_results = []

    key = RSA.generate(2048)

    # Create the public key that will be used in encryption , 
    f = open('rsakey.pem','wb')
    f.write(key.export_key('PEM'))
    f.close()

    recipient_key = RSA.import_key(open("rsakey.pem").read())
    key = get_random_bytes(16)

    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(key)

    for i in range(rows_to_gen):

        case = numpy.random.rand(i+1, 9)

        case_str = numpy.array_str(case)

        start_time = time.perf_counter()

        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(bytes(case_str, encoding="utf-8"), 16))

        end_time = time.perf_counter()

        timing_results.append({
            'rows': i+1,
            'input_data_size': sys.getsizeof(case_str),
            'output_data_size': sys.getsizeof(str(ciphertext)),
            'encryption_elapsed_time': (end_time - start_time)})

    data = pandas.DataFrame.from_dict(timing_results)
    chart_plot = data.plot(x='rows',y='encryption_elapsed_time')

    plt.ylabel('Time in s')
    plt.xlabel('Rows of Sensor Data')
    plt.savefig('rsa_cbc_time_comparison.png')

    data  = data.sort_values(by=['encryption_elapsed_time','rows'])
    data.to_csv('rsa_cbc_time_comparison.csv',mode='w+')

def runDes():
    timing_results = []

    for i in range(rows_to_gen):

        case = numpy.random.rand(i+1, 9)

        case_str = numpy.array_str(case)

        start_time = time.perf_counter()

        cipher = DES.new(b'12345678', DES.MODE_CBC, b'12345678')
        ciphertext = cipher.encrypt(pad(bytes(case_str, encoding="utf-8"), 16))

        end_time = time.perf_counter()

        timing_results.append({
            'rows': i+1,
            'input_data_size': sys.getsizeof(case_str),
            'output_data_size': sys.getsizeof(str(ciphertext)),
            'encryption_elapsed_time': (end_time - start_time)})


    data = pandas.DataFrame.from_dict(timing_results)
    chart_plot = data.plot(x='rows',y='encryption_elapsed_time')

    plt.ylabel('Time in s')
    plt.xlabel('Rows of Sensor Data')
    plt.savefig('des_cbc_time_comparison.png')

    data  = data.sort_values(by=['encryption_elapsed_time','rows'])
    data.to_csv('des_cbc_time_comparison.csv',mode='w+')

if __name__ == "__main__":
    #runDes()
    #runAES()
    #runRSA()
    
    compareAllAlgo()


