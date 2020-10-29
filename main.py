import csv
import time
import serial
import RPi.GPIO as GPIO
import sqlite3

#def button_callback(channel=18):
#print("Button was pushed!")

conn=sqlite3.connect('Halo.db')

conn.execute('''CREATE TABLE Health
                (Name TEXT NOT NULL,
                Heartrate int NOT NULL,
                Temperature int NOT NULL,
                Status TEXT NOT NULL
                ); ''')
conn.execute('''CREATE TABLE History
                (Name TEXT NOT NULL,
                Heartrate int ,
                Temperature int ,
                Status TEXT 
                ); ''')

print("Database created successfully!")

patients=dict()

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

def Emergency(callback):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("\n\nPatient ",P_name," is experiencing complications! Sending sms!\n\n")
    msg="Patient {} is experiencing problems!! Asking for medical SUPPORT!".format(P_name)
    port.write(b'AT+CMGS="8688914045"\r')
    time.sleep(2)
    port.reset_output_buffer()
    time.sleep(2)
    port.write(str.encode(msg+chr(26)))
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    time.sleep(3)

GPIO.setmode(GPIO.BCM)
port = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=1)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
input_state=GPIO.input(18)
GPIO.add_event_detect(18, GPIO.RISING, callback=Emergency)


start =0
first=0

port.write(b"AT\r")
rcv = port.read(10)
port.write(b"AT+CMGF=1\r")


with open("/home/pi/Desktop/scan-data/Data.csv" , mode='r') as file:
    csvFile = csv.reader(file)
        
    for line in csvFile:
        global P_name
        P_name = line[0]
        if(start==0):
            print("Starting the program:\n")
            print("*********************")
            start=start+1
            continue
        
        if (line[0]=='Name') or (line[0]=='Break'):
            time.sleep(3)
            print("Checking in again:")
            print("******************\n")
            conn.execute("""INSERT INTO History (Name, Heartrate, Temperature, Status) \
                VALUES (?,?,?,?);""",[('Next Room'),(''),(''),('')])
            continue

        print("Patient name: "+line[0]+"\n")
        patients[line[0]]=patients.get(line[0],0)
        heart_rate=int(line[1])
        
        if(int(heart_rate<=100 and heart_rate>=60)):            
            if(first<=16):
                conn.execute("""INSERT INTO Health (Name, Heartrate, Temperature, Status) \
                VALUES (?,?,?,?);""",[(line[0]),(line[1]),(line[2]),('Normal')])
                conn.commit()
            else:
                conn.execute("""UPDATE Health SET  Heartrate=?, Temperature=?, Status=? \
                WHERE Name=?;""",[(line[1]),(line[2]),('Normal'),( line[0])])
                conn.commit()
            conn.execute("""INSERT INTO History (Name, Heartrate, Temperature, Status) \
                VALUES (?,?,?,?);""",[(line[0]),(line[1]),(line[2]),('Normal')])
            cache=patients[line[0]]
            print("The patient is fine")
        
        elif(heart_rate>100):
            print("The patient is experiencing high heart rate. Seeking medical attention.\n")
            name=line[0]
            heart=line[1]
            temp=line[2]
            if(first<16):
                conn.execute("""INSERT INTO Health (Name, Heartrate, Temperature, Status) \
                VALUES (?,?,?,?);""",[( line[0]),(line[1]),(line[2]),('High heart rate')])
                conn.commit()
            else:
                conn.execute("""UPDATE Health SET  Heartrate=?, Temperature=?, Status=? \
                WHERE Name=?;""",[(line[1]),(line[2]),('High heart rate'),( line[0])])
                conn.commit()
            callDoc(line[0],line[1],line[2])
            conn.execute("""INSERT INTO History (Name, Heartrate, Temperature, Status) \
                VALUES (?,?,?,?);""",[(line[0]),(line[1]),(line[2]),('High Heart Rate')])
        else:
            print("The patient is experiencing low heart rate. Seeking medical attention")
            if(first<16):
                conn.execute("""INSERT INTO Health (Name, Heartrate, Temperature, Status) \
                VALUES (?,?,?,?);""",[( line[0]),(line[1]),(line[2]),('Low heart Rate')])
                conn.commit()
            else:
                conn.execute("""UPDATE Health SET  Heartrate=?, Temperature=?, Status=? \
                WHERE Name=?;""",[(line[1]),(line[2]),('Low heart rate'),( line[0])])
                conn.commit()
            callDoc(line[0],line[1],line[2])
            conn.execute("""INSERT INTO History (Name, Heartrate, Temperature, Status) \
                VALUES (?,?,?,?);""",[(line[0]),(line[1]),(line[2]),('Low heart rate')])

        print("________________________________________")
        print("")
        time.sleep(2)
        first=first+1
        
        
    print("Final status!\n")
    cursor=conn.execute("""SELECT Name, Heartrate, Temperature, Status from Health""")
    for row in cursor:
        print("Name = ", row[0])
        print ("Heartrate = ", row[1])
        print ("Temperature = ", row[2])
        print ("Status = ", row[3], "\n")
    
    file.close()
    
print("Done")
GPIO.cleanup()