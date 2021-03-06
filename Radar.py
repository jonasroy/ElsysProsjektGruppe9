
import uRAD	# import the uRAD libray
import firebase_admin #import firebase library 
from firebase_admin import credentials
from firebase_admin import firestore
import time #import the time library
import requests
from pprint import pprint
import csv
from datetime import datetime



#Parameter changes for the radar
mode = 1	# Waveform mode set to 1, continous wave (CW). 
f0 = 5		# Operation mode set from 24.005 to 24.245 GHz.
BW = 240	# Operation bandwidth in the other ramp modes. 
Ns = 200	# Number of samples. Range value 38 to 21 samples/sec [50 to 200].
Ntar = 5	# Maximum number of targets to detect from 1 to 5. 
Rmax = 60	# Maximum distance the targets will be searched from 0 to 75. 
MTI = 1		# Moving targets Indication, when activated alll static objects are ignored. 
Mth = 3	    # Defines the sensitivity of the radar. From 1(low) to 4(high).

# results output array
movement = [0]

# load the configuration
uRAD.loadConfiguration(mode, f0, BW, Ns, Ntar, Rmax, MTI, Mth)

# switch ON uRAD
uRAD.turnON()


birdCount = 0

#Retrieving data from the website openweather.org. 
def getWeatherData():
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Trondheim,no&appid=ab285d3403cbfd7b88c9cace599e592d'
    res = requests.get(url)
    data = res.json()
    temp = data['main']['temp']
    wind_speed = data['wind']['speed']
    latitude = data['coord']['lat']
    longitude = data['coord']['lon']
    description = data['weather'][0]['description']
    #Prints the weather on the screen. 
    print('Temperature : {} degree celcius'.format(temp))
    print('Wind Speed : {} m/s'.format(wind_speed))
    print('Latitude : {}'.format(latitude))
    print('Longitude : {}'.format(longitude))
    print('Description : {}'.format(description))
    #Return weather data in a matrix. 
    return [float('{}'.format(temp)),float('{}'.format(wind_speed)),float('{}'.format(latitude)),
    float('{}'.format(longitude)),'{}'.format(description)]
    
def getWeatherData(time):
    
#Transfer the timestamp when function is activated in UNIX time.    
def websiteData():

    #Konfigurasjon av linkt til nettsiden med json fil. 
    cred = credentials.Certificate("/home/pi/Library/FirestoreKey.json")
    app = firebase_admin.initialize_app(cred)

    store = firestore.client()

   
    # Connect the doc_ref to selected Node on the website.
    
    doc_ref = store.collection(u'Unit').document(u"Node1" ).collection(u"Activity")
    
    #Add bird detection coordinates and in real time. 
    doc_ref.add({u"Bird": 1, u"Cord": [10.39621,63.426905],u"TimeStamp": round(time)})
    


#The function write to the next line in a specified CSV file when the Raspberry Pi booted up.
def startTime(filename):
    f = open(filename, mode = "a") 
    sensor_write = csv.writer(f, delimiter = ",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    write_to_log = sensor_write.writerow(["\n", "Raspberry pi booted up: ", gettime_print(), gettime()])

#Skriver til CSVfilen. 
def writeToFile(filename):    
    #the a is for append
    f = open(filename, mode = "a") 
    sensor_write = csv.writer(f, delimiter = ",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    write_to_log = sensor_write.writerow(["Bird detected", "#", birdCount, " ", gettime_print(), gettime()])


#Return UNIX time in seconds. 
def gettime():
    return round(time.clock_gettime(0))


#Return date og time and write to screen in the pi.
#Returns date and time to show 
def gettime_print():
    return datetime.now()
    
#Stores the detection times if the Raspberry Pi loses connection to WiFi. 
def backup_data(float time):
    filename = "/home/pi/Library/FugleData_backup"
    f = open(filename, mode = "a") 
    sensor_write = csv.writer(f, delimiter = ",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    write_to_log = sensor_write.writerow([time])
    
#Reads the content from a file and returns every line in a matrix. 
def readFromFile(file):
    a = []
    with open(file) as f:
            for line in f.readlines():
                a.append(line)
    return a

#Erase the content from a file. 
def delFile(filename): 
        file = open(filename,"r+")
        file.truncate(0)
        file.close()


getTimePiStartedBoot("/home/pi/Library/FugleData")
getWeatherData()

# infinite detection loop
while True:
    # target detecton request
    uRAD.detection(0, 0, 0, 0, 0, movement)
    time_count = time.perf_counter()
    if(time_count > 60):
        getWeatherData()
        time_count = 0
        
    if (movement[0] == True):
        detection_time = gettime()
        print("Bird detected.","#", birdCount," ", gettime_print())
        birdCount += 1
        writeToFile("/home/pi/Library/FugleData")
        try: 
            websiteData(detection_time)
            backup_list = readFromFile("/home/pi/Library/FugleData_backup")
            #Sends the detection times when the Raspberry Pi lost connection to WiFi.
            if(len(backup_list) > 0): 
                for i in range(0,len(backup_list)-1):
                    websiteData(float(backuplist[i]))
                delFile("/home/pi/Library/FugleData_backup")
        except: 
            backup_data(detection_time)
            
        

