import os
import csv
import time
start =0

with open("Data\Data.csv" , mode='r') as file:
    csvFile = csv.reader(file)

    for line in csvFile:
        if(start==0):
            print("Starting the program:\n")
            print("*********************")
            start=start+1
            continue
        
        if (line[0]=='Name') or (line[0]=='Break'):
            time.sleep(3)
            print("Checking in again:")
            continue

        print("Patient name: "+line[0]+"\n")
        heart_rate=int(line[1])
        if(int(heart_rate<=110 and heart_rate>=60)):
            {
            print("The patient is fine")
        }
        elif(heart_rate>110):
            print("The patient is experiencing high heart rate. Seeking medical attentio.\n")
            print("Patient conditions:\nHeart Rate:{}\nTemperature:{}".format(line[1],line[2]))
        else:
            print("The patient is experiencing low heart rate. Seeking medical attention")

        print("________________________________________")
        print("")
        time.sleep(2)


    file.close()
