import os
import csv
import time
import serial
import RPi.GPIO as GPIO
from selenium import webdriver
import sqlite3

conn=sqlite3.connect('test.db')

conn.execute('''CREATE TABLE Company
                (Name TEXT NOT NULL,
                Heartrate int NOT NULL,
                Temperature int NOT NULL,
                Status TEXT NOT NULL
                ); ''')


print("Database created successfully!")


def callDoc(Name, Heart_Rate, Temperature):
    msg="Patient {} conditions:\nHeart Rate:{}\nTemperature:{}".format(Name,Heart_Rate,Temperature)
    print(msg)
    port.write(b'AT+CMGS="8688914045"\r')
    time.sleep(3)
    port.reset_output_buffer()
    time.sleep(1)
    port.write(str.encode(msg+chr(26)))
    time.sleep(3)
    print("message sent…")

GPIO.setmode(GPIO.BOARD)
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)

start =0
first=0

port.write(b"AT\r")
rcv = port.read(10)
port.write(b"AT+CMGF=1\r")


with open("/home/pi/Desktop/scan-data/Data.csv" , mode='r') as file:
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
            print("******************\n")
            continue

        print("Patient name: "+line[0]+"\n")
        
        heart_rate=int(line[1])
        
        if(int(heart_rate<=110 and heart_rate>=60)):
            {
            print("The patient is fine")
            
            if(first<=20):
                conn.execute("""INSERT INTO Company (Name, Heartrate, Temperature, Status) \
                VALUES (?,?,?,?);""",[(line[0],line[1],line[2],'Normal')])
                conn.commit()
        }
        elif(heart_rate>110):
            print("The patient is experiencing high heart rate. Seeking medical attention.\n")
            callDoc(line[0],line[1],line[2])
        else:
            print("The patient is experiencing low heart rate. Seeking medical attention")
            callDoc(line[0],line[1],line[2])

        print("________________________________________")
        print("")
        time.sleep(2)
        first=first+1


    file.close()
