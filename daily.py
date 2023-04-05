from utils.scraping import *
import logging, sys, os
from dotenv import load_dotenv

from db_functions.db_funct import *
from utils.members_fct import *

def main():
    # Get variable from environnement
    logging.basicConfig(filename='logfile.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    res = load_dotenv(dotenv_path='.env')
    if res == False:
        logging.critical("Create .env file before running the script! See README.md")
        sys.exit(0)
    
    squad_url = os.getenv('SQUADRON_URL')
    squad_name = os.getenv('SQUAD_NAME')
    db_name = 'test.db' # os.getenv('DB_NAME')
    discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

    # Download the page if wasn't downloaded
    html_file_path = "tmp_dir/" + squad_name + "_" + str(datetime.today().strftime('%Y-%m-%d')) + ".html"
    if os.path.exists(html_file_path) == False:
        if download_web_page(squad_url,html_file_path) == False:
            logging.info("Error during the page download")
            sys.exit(0)
        else:
            logging.debug("HTML page was downloaded")
    else:
        logging.debug("HTML page already downloaded")

    # Scrap the page
    new_squad_members_list = correct_email_protection(scrap_squadron_profile_page(html_file_path),
                        list_of_all_members(html_file_path))
    
    # print(new_squad_members_list[90].pseudo)
    
    # Compare with data in database
    db_squad_list = get_all_squad_members(db_name)
    # print(db_squad_list[90].pseudo)
    list_create_squad, list_to_update, list_leaver  = compare_squads_members(db_squad_list,new_squad_members_list)
    # print("to delete",list_leaver)
    # print("to create", list_create_squad)
    # print("to update", list_to_update)

    # Update database
    update_squad_members_activity(db_name,list_to_update)
    insert_all_squad(db_name,list_create_squad)
    delete_list_of_members(db_name,list_leaver) # Keep an history somewhere ? # TODO#TOTHINK
    
    # Check if we need to warn inactive members 
    for el in get_all_squad_members(db_name):
        if check_if_members_is_inactive(el):
            msg = f"The following members {el.pseudo} is inactive for more than 3 weeks"
            send_discord_notif(discord_webhook_url,msg) # exluce new player ?
    
    # Generate graph
 
    # Delete old HTML file

if __name__=="__main__":
    main()