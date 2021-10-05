file  = open('compressed_data.txt','r')

count = 0
max = 5
for line in file:
    if count < max:
        print(line)
    count += 1