# Author: Mathew January, Pius Gumo
# Compression algorithm v2

def compressRow(dataRows):
    ''' Return the fourier transform of 
        the row(s) passed to the function
    '''
    compressed_row = []

    for row in dataRows:
        compressed_data.append(row)
    
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

def performCompressionOnImuDataSet(imu_rows_data,imu_row_header):
    ''' Perform compression on a set of data retrieved from
        the IMU '''
    
    fourier_data = []

    # perform fourier transform first
    for i in range(len(imu_rows_data)):
        fourier_data[i] = compressRow(row)
    
    # perform lowpass on the fourier transforms
    filtered_data = lowPass(fourier_data)

    return filtered_data

