from myclass.squad_member import Squad_member, squad_member_encoder
import csv,json,os,re

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