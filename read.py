import time
import imu
import datetime

global sensor


def initialize():
    global sensor
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


if __name__ == "__main__":
    
    # Determine whether to log data
    logging_data = askToLogData()
    
    initialize()

    if(logging_data == True):
        log_file = open('imu_data.csv', 'w')
        log_file.write("Time,Gyrometer,Magnenometer,Accelerometer\n")

    for i in range(60):

        [gyro_data, acc_data, mag_data] = readData()

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
            writeRowToFile(file=log_file,time=formatted_time, gyro_data=gyro_data,
                           acc_data=acc_data, mag_data=mag_data)

        time.sleep(1)
