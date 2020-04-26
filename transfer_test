
import firebase_admin #import firebase library 
from firebase_admin import credentials
from firebase_admin import firestore
import time #import the time library


#Return UNIX time in seconds. 
def gettime():
    return round(time.clock_gettime(0))


#The function sends n number of simulated bird detection with specified node on the website and coordinates. 
#nr_node - Node number. 
#n - how many test detection in a row to the website. 
#lat - latitude in coordiantes. 
#lon - longitude in coordinates. 

def transfer_test(int nr_node, int n, float lat, float lon):
    node = "Node" + str(nr_node)
    cred = credentials.Certificate("/home/pi/Library/FirestoreKey.json")
    app = firebase_admin.initialize_app(cred)
    store = firestore.client()
    doc_ref = store.collection(u'Unit').document(u+node ).collection(u"Activity")
    
    for i in range(n):
        doc_ref.add({u"Bird": 1, u"Cord": [lon,lat],u"TimeStamp": round(gettime())})
 
 #Test with the coordinates of the Nidaros Cathedral.
 transfer_test( 2, 200, 63.426905, 10.39621)
 
 #Test with the coordiantes of Gløshaugen. 
 transfer_test( 3, 70, 63.417402, 10.404144)
