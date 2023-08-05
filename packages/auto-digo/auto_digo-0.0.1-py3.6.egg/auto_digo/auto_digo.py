import os
import subprocess
import sys
import json
import random

def auto_run(path, setting):
    print("Welcom, Run Code \"{0}\", Setting is \"{1}\"".format(path, setting))

    fileDirectory = os.path.dirname(os.path.abspath(path))
    
    if os.path.exists(path) is False:
        raise Exception("Not Found File : Check Path {}".format(path))

    if os.path.exists(fileDirectory + os.path.sep + setting) is False:
        raise Exception("Not Found File : Check Setting File {}".format(fileDirectory + os.path.sep + setting))


    with open(fileDirectory + os.path.sep + setting) as ml_option_raw:
        ml_option = json.loads(ml_option_raw.read())

    print(ml_option)

    for i in range(ml_option["iterator"]):
        parameters = ['python', '-u', path]

        for p in ml_option["parameter"]:
            if p["random"] == None or p["random"] == False :
                parameters.append(p["name"])
                parameters.append(str(p["data"]))

            else :
                parameters.append(p["name"])
                if p["type"] == "float":
                    parameters.append(str(random.uniform(p["data"][0], p["data"][1])))
                elif p["type"] == "int":
                    parameters.append(str(random.randint(p["data"][0], p["data"][1])))
        
        print (parameters)
        proc = subprocess.Popen(parameters, stdout=subprocess.PIPE)

        while proc.poll() == None:
            nextLine = proc.stdout.readline()
            print(nextLine)
        