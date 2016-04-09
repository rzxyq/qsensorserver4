import json 
import requests 
from time import sleep 

# read a text file as a list of lines
# find the last line, change to a file you have
while(True): 
    # url = "http://127.0.0.1:8000/data/post_data"
    
    url = "https://qsensorserver2.herokuapp.com/data/post_data"

    fileHandle = open('./screenlog.0')
    lineList = fileHandle.readlines()
    fileHandle.close()
    data = lineList[-1]
    data = data.replace("\r\n", "")


    # Try because sometimes catch data midstream 
    try: 
        data_array = data.split(",")


        if (data_array[0] == 'C' or data_array[0] == 'c'): 
            data_array[0] = 10 # Modify for 10's 


        info = {
            'data': data, # Text-based data
            'seconds': data_array[0],
            'x_coord': data_array[1],
            'y_coord': data_array[2],
            'z_coord': data_array[3],
            'unknown': data_array[4],
            'temp': data_array[5],
            'eda': data_array[6],
        }

    # Catch any exceptions as necessary 
    except Exception as e: 
        info = {
            'data': "Error",
        }

    sleep(0.3)


    r = requests.post(url, data=json.dumps(info), verify=False)



