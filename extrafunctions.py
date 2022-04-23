import json
import os
def abs_path(filepath:str):
    if os.path.isabs(filepath):
        return(filepath)
    components = filepath.split(os.path.sep) # / in Mac/Linux; \ in Windows
    dir_path = os.path.dirname(os.path.realpath(__file__))
    components.insert(0,dir_path)
    final_path = os.path.join(*components)
    os.makedirs(os.path.join(*components[:-1]),exist_ok=True) # In windows error is thrown if folder containing file is not present. makedirs makes folders recursively. The exist_ok flag when set True doesn't raise error if folder already exists
    return(final_path)

def convertDictToObject(dic:dict):
    '''This function converts a dictionary into an Object'''
    class Data:
        def __init__(self,dictionary):
            self.__dict__.update(dictionary)
    
    return(json.loads(json.dumps(dic),object_hook=Data))

def convertJsonToObject(filepath):
    class Data:
        def __init__(self,dictionary):
            self.__dict__.update(dictionary)
    with open(abs_path(filepath),"r") as jsonfile:
        obj = json.load(jsonfile,object_hook=Data)
    return(obj)
def convertObjectToJson(obj,filepath,filemode="w"): #This can also convert Dict to JSON file
    with open(abs_path(filepath),filemode) as jsonfile:
        json.dump(obj,jsonfile,indent=4)
        jsonfile.write('\n')
def convertJSONToDict(filepath):
    with open(abs_path(filepath),"r") as jsonfile:
        dic = json.load(jsonfile)
    return(dic)

def fileToString(filepath):
    with open(abs_path(filepath),'r') as f:
        string = f.read()
    return(string)
def main():
    # print(abs_path('src\\abc\\def.txt'))
    # rssfeed = convertJsonToObject('onion.json')
    # print(rssfeed.feed.title)
    path = abs_path('main.py')
    print(path)
    print(abs_path(path))
if __name__ == '__main__':
    main()