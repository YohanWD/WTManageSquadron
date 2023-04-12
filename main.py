from utils.scraping import *
import logging, sys, os, glob
from dotenv import load_dotenv

from db_functions.db_funct import *
from utils.members_fct import *

import matplotlib.pyplot as plt
from datetime import datetime

def main():
    # Get variable from environnement
    logging.basicConfig(filename='logfile.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    res = load_dotenv(dotenv_path='.env')
    if res == False:
        logging.critical("Create .env file before running the script! See README.md")
        sys.exit(0)
    
    squad_url = os.getenv('SQUADRON_URL')
    squad_name = os.getenv('SQUAD_NAME')
    db_name = os.getenv('DB_NAME')
    discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

    # Checking if we need to create the database
    if os.path.exists(db_name) == False:
        create_db_schema(db_name,'db_functions/schema.sql')
        print('New db is initialised')
    else:
        print('No need to create DB')

    already_updated = False
    # Download the page if wasn't downloaded
    html_file_name = squad_name + "_" + str(datetime.today().strftime('%Y-%m-%d')) + ".html"
    html_file_path = "tmp_dir/" + html_file_name
    if os.path.exists(html_file_path) == False:
        if download_web_page(squad_url,html_file_path) == False:
            logging.info("Error during the page download")
            sys.exit(0)
        else:
            logging.debug("HTML page was downloaded")
    else:
        logging.debug("HTML page already downloaded, skipping insert in DB")
        already_updated = True

    # Update database
    if already_updated == False:
        # Scrap the page
        new_squad_members_list = correct_email_protection(scrap_squadron_profile_page(html_file_path),
                            list_of_all_members(html_file_path))
        # Compare with data in database
        db_squad_list = get_all_squad_members(db_name)
        list_create_squad, list_to_update, list_leaver  = compare_squads_members(db_squad_list,new_squad_members_list)

        update_squad_members_activity(db_name,list_to_update)
        insert_all_squad(db_name,list_create_squad)
        delete_list_of_members(db_name,list_leaver) # Keep an history somewhere ? # TODO#TOTHINK

        # Generate graph
        for el in get_all_squad_members(db_name):
            history_list = get_activity_history_from_members(db_name, el.id)
            x_list = []
            y_list = []
            for elem1, elem2 in history_list:
                x_list.append(datetime.strptime(elem2, '%Y-%m-%d %H:%M:%S'))
                y_list.append(elem1)

            plt.clf()
            plt.xlabel('x - time')
            plt.ylabel('y - activity')
            plt.plot(x_list, y_list, color='green', linestyle='dashed', linewidth = 3,
                    marker='o', markerfacecolor='blue', markersize=12)

            plt.gcf().autofmt_xdate()
            plt.title(f'Activity plot for {el.pseudo}')
            plt.savefig(f'tmp_dir/graph/{el.pseudo}.png')
    
    # Check if we need to warn inactive members
    for el in get_all_squad_members(db_name):
        if check_if_members_is_inactive(el):
            msg = f"The following members {el.pseudo} is inactive for more than 3 weeks"
            send_discord_notif(discord_webhook_url,msg) # exclude new player ?

    # Delete old HTML file
    purge('tmp_dir',f"{squad_name}_.*.html",html_file_name)
    
if __name__=="__main__":
    main()