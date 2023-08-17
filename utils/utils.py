from myclass.squad_member import squad_member_encoder
import csv,json,os,re, gzip,shutil
from discord import SyncWebhook

import logging
logger = logging.getLogger(__name__)

# Remove first n first element of a list
def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

# file_path : ex (/etc/test.csv)
# columns : a list containng all the columns of the csv (ex : ['name','numbers'])
# data_list : a list of list of data to write in the csv file
def write_csv_file(file_path,columns,data_list):
    with open(file_path, 'w', newline='') as f: 
        write = csv.writer(f) 
        write.writerow(columns)
        write.writerows(data_list)

# file_path : ex (/etc/test.json)
# data : the data to write in the file (must be serialisable)
def write_json_file(file_path,data):
    with open(file_path, 'w') as f:
        for el in data :
            json.dump(el, f,ensure_ascii=False, indent=4, cls=squad_member_encoder)

# Delete all file matching a certain patern execpt the exclusion_file_name
def purge(dir, pattern, exlusion_file_name):
    for f in os.listdir(dir):
        if re.search(pattern, f) != None and f != exlusion_file_name:
            os.remove(os.path.join(dir, f))

## Logging
# Used to rotate logging while zipping the previous file
def rotator(source, dest):
    with open(source, 'rb') as f_in:
        with gzip.open(dest, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(source)

# Used to define log name
def namer(name):
    return name +".gz"


# Return a list containing the string in x element smaller than the length
def check_if_string_bigger_than(str,length):
    if len(str)> length:
        nbr_of_line = str.count('\n')
        tmpstr = ""
        for el in str.split('\n',nbr_of_line//2)[:nbr_of_line//2]:
            tmpstr = tmpstr + el + "\n"
        
        list = [tmpstr] + str.split('\n',nbr_of_line//2)[(nbr_of_line//2):]
        return list

    return [str]

# Function who send a message, if message is bigger than X char it will split 
# in smaller message
# Pre : a message needs to be separate by '\n'
def send_discord_notif(webhook_url, message):
    webhook = SyncWebhook.from_url(webhook_url)
    try:
        for el in check_if_string_bigger_than(message,2500):
            logger.debug(f"Sending message (size =  {len(el)}): {el}")
            webhook.send(el)
    except Exception as e:
        logger.critical("Error while sending message to discord : ", e)
