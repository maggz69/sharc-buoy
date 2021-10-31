import numpy as np
from scipy.fftpack import fft, fftfreq
import sys

# Author: Mathew January, Pius Gumo
# Compression algorithm v2


def compressRow(dataRow):
    ''' Return the fourier transform of 
        the row passed to the function

        dataRow list item containing the data elements to be parsed
    '''

    # Loop through the data list passed and fourier transform the data
    # This is ideally similar to  gyro x,y,z : acc x,y,z

    print(f"Data row \n", dataRow)
    sys.stdout.flush()

    compressed_row_array = np.array(dataRow)
    compressed_row = fft(compressed_row_array)

    return compressed_row


def lowPass(fourier_data):
    ''' Perform low pass filtering on the fourier transformed
        data to obtain at least 25% 
    '''

    filtered_data = []
    co_efficients = len(fourier_data)//3

    for i in range(co_efficients):
        filtered_data.append(fourier_data[i])
    return filtered_data


def performCompressionOnImuDataSet(imu_rows_data, imu_row_header):
    ''' Perform compression on a set of data retrieved from
        the IMU '''

    fourier_data = []

    # perform fourier transform first
    for i in range(len(imu_rows_data)):
        fourier_data[i] = compressRow(imu_rows_data[i])

    # perform lowpass on the fourier transforms
    filtered_data = lowPass(fourier_data)

    return filtered_data
