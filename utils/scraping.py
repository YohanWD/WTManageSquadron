from bs4 import BeautifulSoup
import re
from utils.utils import *

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
    HTMLFileToBeOpened = open(web_page_path, "r",encoding='utf-8') # need to be close ? 
    contents = HTMLFileToBeOpened.read()
    soup = BeautifulSoup(contents, 'html.parser')

    squad_members = []
    html_squad_members_el = soup.find_all('a', href = re.compile(r'https://warthunder.com/en/community/userinfo/*'))
    for el in html_squad_members_el:
        squad_members.append(el.text.split()[0])

    return squad_members