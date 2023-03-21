from bs4 import BeautifulSoup
import re
from utils.utils import *
from datetime import datetime
import requests

# Function that scrap War thunder squadron html page
# Pre : the path to of the html document
# Return a list of squad_members object 
def scrap_squadron_profile_page(web_page_path):
    HTMLFileToBeOpened = open(web_page_path, "r",encoding='utf-8') # need to be close ? 
    contents = HTMLFileToBeOpened.read()
    soup = BeautifulSoup(contents, 'html.parser')

    squad_members = []
    squad_member_html = soup.find("div", {"class": "squadrons-members__table"})# <div class="">

    list_tmp = []

    tmp_el = squad_member_html.find_all('div')

    for el2 in tmp_el:
        list_tmp.append(el2.text.split()[0])

    my_list = list(divide_chunks(list_tmp[6:], 6))

    squad_members = []
    for el in my_list:
        squad_members.append(Squad_member(el)) # not serialisable

    return squad_members

# Return a list containing all the username in the squadron members
# Pre : the path of the html document (squadron page)
def list_of_all_members(web_page_path):
    HTMLFileToBeOpened = open(web_page_path, "r", encoding='utf-8') # need to be close ? 
    contents = HTMLFileToBeOpened.read()
    soup = BeautifulSoup(contents, 'html.parser')

    squad_members = []
    for a in soup.find_all('a', href= re.compile(r'en/community/userinfo/*')):
        squad_members.append(a['href'].split("=")[1])

    return squad_members

# Cloud flare mail protection (billy@psn is not an email...)
# Compare two list to replace [email by the real name
# ex :
# list_squadron_members = [{1,"Jean",...},{2,"[email",...}]
# list_squad_members_name : ["Jean", "billy@psn"]
# output list = [{1,"Jean",...},{2,"billy@psn",...}]
def correct_email_protection(list_squadron_members,list_squad_members_name):
    cpt = 0
    new_list = []
    for el in list_squadron_members:
        if el.name == "[email":
            el.setName(list_squad_members_name[cpt])
        cpt += 1
        
        new_list.append(el)
    
    return new_list

# Download the page in a html file
#
#
def download_web_page(url):
    path_of_file = "tmp_dir/b3m_" + str(datetime.today().strftime('%Y-%m-%d')) + ".html"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    try:
        response = requests.get(url, headers=headers)
        # print(response.content)
        with open(path_of_file,"wb") as f:
            f.write(response.content)
    except Exception as e:
        print(e)
    
    return path_of_file
