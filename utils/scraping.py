from bs4 import BeautifulSoup
import re

# Function that scrap War thunder squadron html page
# Pre : the path to of the html document
# Return a list of object squad_members
# TODO
def scrap_squadron_profile_page(web_page_path):
    HTMLFileToBeOpened = open(web_page_path, "r")
    contents = HTMLFileToBeOpened.read()
    soup = BeautifulSoup(contents, 'html.parser')

    squad_members = []

    return squad_members

# Return a list containing all the username in the squadron members
# Pre : the path of the html document (squadron page)
def list_of_all_members(web_page_path):
    HTMLFileToBeOpened = open(web_page_path, "r") # need to be close ? 
    contents = HTMLFileToBeOpened.read()
    soup = BeautifulSoup(contents, 'html.parser')

    squad_members = []
    html_squad_members_el = soup.find_all('a', href = re.compile(r'https://warthunder.com/fr/community/userinfo/*'))
    for el in html_squad_members_el:
        squad_members.append(el.text.split()[0])

    return squad_members