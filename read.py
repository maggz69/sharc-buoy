import time
import imu
import threading
import encrypt
import compress
import numpy as np
import sys

global sensor


def initialize():
    global sensor, compressed_data, last_buffer_expunge_time

    last_buffer_expunge_time = None
    compressed_data = []

    sensor = imu.ICM20948()
    print("Retrieving Data From IMU Sensor :)")

    print("{:^20}|{:^29}|{:^29}|{:^27}|".format(
        "Time", "Gyro", "Mag", "Accelerometer"))
    print(" "*20, end="|")
    print("{:^9} {:^9} {:^9}|".format("x", "y", "z")*3)


def readData():
    global sensor
    # Define what readings you would like to get
    sensor.icm20948_Gyro_Accel_Read()
    sensor.icm20948MagRead()
    sensor.icm20948CalAvgValue()

    time.sleep(0.1)

    sensor.imuAHRSupdate(imu.MotionVal[0] * 0.0175, imu.MotionVal[1] * 0.0175, imu.MotionVal[2] * 0.0175,
                         imu.MotionVal[3], imu.MotionVal[4], imu.MotionVal[5],
                         imu.MotionVal[6], imu.MotionVal[7], imu.MotionVal[8])

    gyro = getGyroData()
    acc = getAccelerationData()
    mag = getMagnenometerData()

    return [gyro, acc, mag]


def printData(data):
    print("{:^9.2f} {:^9.2f} {:^9.2f}|".format(
        data[0], data[1], data[2]), end="")


def getGyroData():
    return imu.Gyro


def getAccelerationData():
    return imu.Accel


def getMagnenometerData():
    return imu.Mag


def askToLogData():
    log_data = input(
        "Do you want to enabling logging data to a csv file ?\n [Y]Yes [N]No\n")

    if log_data == 'Y':
        print("Logging data to imu_data.csv")
        return True
    if log_data == 'N':
        print("Skipping  Logging of data")
        return False
    if log_data != 'Y' and log_data != 'N':
        print("\n\nYou've entered an invalid option!\n")
        return askToLogData()


def writeRowToFile(file, time, gyro_data, mag_data, acc_data):

    file.write(
        time
    )

    file.write(",")

    file.write(
        " ".join(str(gyro) for gyro in gyro_data)
    )

    file.write(",")

    file.write(
        " ".join(str(mag) for mag in mag_data)
    )

    file.write(",")

    file.write(
        " ".join(str(acc) for acc in mag_data)
    )

    file.write("\n")


def writeEncryptedToFile(encrypted_data):
    file = open('encrypted_txt.txt', 'a+')
    file.write(str(encrypted_data))
    file.close()

    print("Encrypted data has been written")


def compressEncryptDataThread(compressed_data):
    fourier_data = []


    start_compress_time = time.perf_counter()
    fourier_data = compress.compressRow(compressed_data)
    # Generate Fourier Data
    # for row in compressed_data:
    # fourier_data.append(compress.compressRow(row))

    # Perform Low Pass
    fourier_lp = compress.lowPass(fourier_data)

    # Fourier Str
    compressed_str = np.array_str(np.array(fourier_lp))

    end_compress_time = time.perf_counter()
    encrypted_data = encrypt.encryptFourierData(compressed_str)
    writeEncryptedToFile(encrypted_data)
    end_encrypt_time = time.perf_counter()

    # write to file in the following order (uncompressed_data_size,compressed_data_size,compression_time,encryption_time)
    file = open('timing_data.csv','a+')
    file.write(str(sys.getsizeof(compressed_data)))
    file.write(',')
    file.write(str(sys.getsizeof(fourier_lp)))
    file.write(',')
    file.write(str(end_compress_time - start_compress_time))
    file.write(',')
    file.write(str(end_encrypt_time - end_compress_time))
    file.write('\n')
    file.close

    sys.exit()


def appendRowToBuffer(row):
    global compressed_data, last_buffer_expunge_time

    current_time = time.perf_counter()

    compressed_data.append(row)

    if (last_buffer_expunge_time == None) or ((current_time - last_buffer_expunge_time) > 10):
        compression_thread = threading.Thread(
            target=compressEncryptDataThread, args=([compressed_data]))
        compression_thread.start()
        compressed_data = []
        last_buffer_expunge_time = current_time


if __name__ == "__main__":

    # Determine whether to log data
    # logging_data = askToLogData()

    logging_data = False

    initialize()

    if(logging_data == True):
        log_file = open('imu_data.csv', 'w')
        log_file.write("Time,Gyrometer,Magnenometer,Accelerometer\n")

    while True:

        [gyro_data, acc_data, mag_data] = readData()

        # append data to buffer

        appendRowToBuffer([gyro_data[0], gyro_data[1], gyro_data[2], acc_data[0],
                          acc_data[1], acc_data[2], mag_data[0], mag_data[1], mag_data[2]])

        # print the current time in gmt
        ct = time.gmtime()

        formatted_time = "{:0^4}/{:0^2}/{:0^2} {:0^2}:{:0^2}:{:0^2} ".format(ct.tm_year,
                                                                             ct.tm_mon, ct.tm_mday, ct.tm_hour, ct.tm_min, ct.tm_sec)
        print(formatted_time, end="|")

        # print the xyz data for the remaining domains
        printData(gyro_data)
        printData(mag_data)
        printData(acc_data)
        print("")

        if(logging_data):
            writeRowToFile(file=log_file, time=formatted_time, gyro_data=gyro_data,
                           acc_data=acc_data, mag_data=mag_data)

        time.sleep(2)
