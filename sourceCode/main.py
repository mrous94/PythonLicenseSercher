import os
import json
import re
import pathlib
from itertools import islice


def search(list, element):
    if len(list)>0:
        for i in range(len(list)):
    
            if list[i] == element:
                return True
    return False        



with open('database.json', 'r') as file:
    licenseDatabase = file.read()

data = json.loads(licenseDatabase)


print()
print("This is program will check licenses of files in your repository. Enjoy.")
print()

pathexists=False
while pathexists==False:
    project_directory = input("Enter path to your repository: ")
    pathexists = os.path.isdir(project_directory)
    if pathexists == False:
        print("Your path is worng, please enter correct path.")
    
    
while True:
    save_directory = input("Name folder where files with licenses will be saved: ")
    if save_directory == '':
        print("No folder name was passed. Please enter folder name")
        continue
    else:break





database = []
how_many_files =0
print("work in progres...")
#Walking though files in directory:
for root, dirs, files in os.walk(project_directory):
    for file in [root + '\\' + x for x  in files if not ".exe" in x ]:
        with open(file, 'r', encoding='utf-8') as myfile:
            #fileData = myfile.read()
            fileData = str(list(islice(myfile, 40)))

            newShortname = []
            shortname = []
            name =[]
            text=[]
            
            #Comparing 
            for info in data['licenses']:
                shortnameTemp= []
                fullnameTemp=[]
                textTemp = []
                shortnameTemp = re.findall("SPDX-License-Identifier: " +info['shortname'] , fileData)
                fullnameTemp = re.findall( info['fullname'] , fileData)
               
               
                if len(shortnameTemp)>0: 
                    shortname.append(shortnameTemp[0])
                if len(fullnameTemp)>0: 
                    name.append(fullnameTemp[0])
                    shortname.append(info['shortname'])
                
            
                   
            #cutinng space at the begining of each found shortname;
            for string in shortname:
                new_string = string.replace("SPDX-License-Identifier: ", "")    
                newShortname.append(new_string)

            #appendig founded licenses to database and file names
            filename = file.replace(project_directory,'')
            database.append({
            'fullname': name,
            'shortname': newShortname,
            'text': text,
            'filename': filename,
            })
            how_many_files +=1
    print("work in progres...")

file = open("AllFound.json","w")
print (json.dumps(database),file = file)
file.close()
            
            
          
#Varaibles to categorize licenses to file.            
top1 ="SHORT IDENTIFIER SPDX" 
top2 ="FULL NAME LICENCSE FOUND"
top3 ="FILE NAME"
shortgpl = ['NGPL','LGPLLR','LGPL-3.0','LGPL-3.1','LGPL-2.0','GPL-3.0','GPL-2.0','GPL-1.0','AGPL-1.0','AGPL-3.0' ]
longgpl = ['Affero General Public License v1.0 only','Affero General Public License v1.0 only or later',
'Affero General Public License v3.0 only','Affero General Public License v3.0 only or later',
'GNU General Public License v1.0 only','GNU General Public License v1.0 only or later','GNU General Public License v2.0 only','GNU General Public License v2.0 later',
'GNU General Public License v3.0 only','GNU General Public License v3.0 only or later','GNU Library General Public License v2 only',
'GNU Library General Public License v2 only or later','GNU Lesser General Public License v2.1 only','GNU Lesser General Public License v2.1 only or later',
'GNU Lesser General Public License v3.0 only','GNU Lesser General Public License v3.0 only or later']
gpl_json =[]
mit_json =[]
other_json =[]
how_many_MIT=0
how_many_GPL=0
how_many_other =0
how_many_not_specified=0
def file_header():
    return '{:<30} {:<30}\n'.format(top1, top3,)

#Creating directory and files 
pathlib.Path('./'+save_directory).mkdir(parents =True, exist_ok=True)
fileGPL =open('./'+save_directory+'/GplLicenses.txt', 'w')
fileGPL.write(file_header())
fileMIT =open('./'+save_directory+'/MitLicenses.txt', 'w')
fileMIT.write(file_header())
fileSPDXOther =open('./'+save_directory+'/OtherLicenses.txt', 'w')
fileSPDXOther.write(file_header())
fileNotSpecified = open('./'+save_directory+'/NotSpecifiedLicenses.txt', 'w')
fileNotSpecified.write('{:<30}\n'.format("FILENAME"))

def format_file_list():
    return '{:<30}\n'.format(str(info['filename']))

def format_other_liceenses():
    return '{:<30} {:<30} \n'.format(str(info['shortname']),str(info['filename']))



#Writing to the files
for info in database:
    if info['shortname'] != []:

        if any(item in shortgpl for item in info['shortname']):
            fileGPL.write(format_other_liceenses())
            gpl_json.append({
            'fullname': info['fullname'],
            'shortname': info['shortname'],
            'filename': info['filename']
            })
            how_many_GPL +=1
        elif "MIT" in info['shortname']:
            fileMIT.write(format_other_liceenses())
            mit_json.append({
            'fullname': info['fullname'],
            'shortname': info['shortname'],
            'filename': info['filename']
            })
            how_many_MIT +=1
        else:
            fileSPDXOther.write(format_other_liceenses())
            other_json.append({
            'fullname': info['fullname'],
            'shortname': info['shortname'],
            'filename': info['filename']
            })
            how_many_other +=1
    elif info['fullname'] != []:
        if any(item in longgpl for item in info['fullname']):
            fileGPL.write(format_other_liceenses())
            gpl_json.append({
            'fullname': info['fullname'],
            'shortname': info['shortname'],
            'filename': info['filename']
            })
            how_many_GPL +=1
        elif "MIT License" in info['fullname']:
            fileMIT.write(format_other_liceenses())
            mit_json.append({
            'fullname': info['fullname'],
            'shortname': info['shortname'],
            'filename': info['filename']
            })
            how_many_MIT +=1
        else:
            fileSPDXOther.write(format_other_liceenses())
            other_json.append({
            'fullname': info['fullname'],
            'shortname': info['shortname'],
            'filename': info['filename']
            })
            how_many_other +=1        
    else:
        fileNotSpecified.write(str(info['filename'] + "\n"))
        how_many_not_specified +=1         

fileGPL.close()
fileMIT.close()
fileSPDXOther.close()
fileNotSpecified.close()

file = open('./'+save_directory+"/Gpl.json","w")
print (json.dumps(gpl_json),file = file)
file.close()
file = open('./'+save_directory+"/Mit.json","w")
print (json.dumps(mit_json),file = file)
file.close()
file = open('./'+save_directory+"/Other.json","w")
print (json.dumps(other_json),file = file)
file.close()

print("Succes! Files with licenses found can be found in folder "+str(pathlib.Path.cwd())+"\\"+save_directory)
print("There was "+ str(how_many_files) + " files in your directory.")
print("MIT licenses found: "+str(how_many_MIT)+"." )
print("GPL licenses found: "+str(how_many_GPL)+"." )
print("Other licenses found: "+str(how_many_other)+"." )
print("Files with not specifed licenses: "+str(how_many_not_specified)+"." )
input()
#FINITO?




