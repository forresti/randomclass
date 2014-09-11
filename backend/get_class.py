import json
from flask import Flask
app = Flask(__name__)
from crossdomain import crossdomain
import random

def getSampleClass():
    toyClassID = random.choice([0,1])
    if toyClassID == 0:
        sampleClass = dict()
        sampleClass['courseTitle'] = 'Tibetan Buddhism'
        sampleClass['meetingDay'] = 'TuTh' #flattened from inside of 'sectionMeetings'
        sampleClass['startTime'] = '1230'
        sampleClass['building'] = 'Dwinelle Hall'
        sampleClass['room'] = '215'

    else:
        sampleClass = dict()
        sampleClass['courseTitle'] = 'Special Topics in African History'
        sampleClass['meetingDay'] = 'TuTh' #flattened from inside of 'sectionMeetings'
        sampleClass['startTime'] = '1400' #clarify time of day stuff?
        sampleClass['building'] = 'Dwinelle Hall'
        sampleClass['room'] = '210'
    return sampleClass

@app.route("/getRandomClass")
@crossdomain(origin='*') #avoid 'Access-Control-Allow-Origin' error in browser
def getRandomClass():
    ret_class = getSampleClass() #TODO: replace with randomized database lookup
    ret_class = json.dumps(ret_class)
    return ret_class

if __name__ == "__main__":
    #print getRandomClass()

    #app.run()
    # * Running on http://localhost:5000/
    #usage: wget http://127.0.0.1:5000/getRandomClass 
    # -> outputs {"courseTitle": "Tibetan Buddhism", etc} in a file "getRandomClass"


    #exposes API to the public: http://r8.cs.berkeley.edu:5000/getRandomClass
    app.run(host='0.0.0.0')

    #exposes API to the public: http://r8.cs.berkeley.edu:8080/getRandomClass
    #app.run(host='0.0.0.0', port=8080)
