import json
from flask import Flask
app = Flask(__name__)

def getSampleClass():
    sampleClass = dict()
    sampleClass['courseTitle'] = 'Tibetan Buddhism'
    sampleClass['meetingDay'] = 'TuTh' #flattened from inside of 'sectionMeetings'
    sampleClass['startTime'] = '1230'
    sampleClass['building'] = 'Dwinelle Hall'
    sampleClass['room'] = '215'
    return sampleClass

@app.route("/getRandomClass")
def getRandomClass():
    ret_class = getSampleClass() #TODO: replace with randomized database lookup
    ret_class = json.dumps(ret_class)
    return ret_class

if __name__ == "__main__":
    #print getRandomClass()
    app.run()
    # * Running on http://localhost:5000/
    #usage: wget http://127.0.0.1:5000/getRandomClass 
    # -> outputs {"courseTitle": "Tibetan Buddhism", etc} in a file "getRandomClass"
