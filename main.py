from utils.scraping import *
import logging, sys, os
import logging.handlers
from dotenv import load_dotenv

from db_functions import db_funct

from utils import members_fct,scraping,utils

import matplotlib.pyplot as plt
from datetime import datetime

def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    res = load_dotenv(dotenv_path=dir_path+'/.env')
    if res == False:
        logging.critical("Create .env file before running the script! See README.md")
        sys.exit(0)
    
    try: 
        squad_url = os.environ['SQUADRON_URL']
        squad_name = os.environ['SQUAD_NAME']
        db_name = os.environ['DB_NAME']
        discord_webhook_url = os.environ['DISCORD_WEBHOOK_URL']
        path_to_save_graph = os.environ['path_to_save_graph']
        path_to_save_html = os.environ['path_to_save_html_file']
        
        log_file_path = os.environ['LOGFILE_LOCATION']
        NB_OF_LOG_FILE = int(os.environ['NB_OF_LOG_FILE'])
    except Exception as e:
        msg = f"One or more env variable are not set, please verify following variable : {e}"
        print(msg)
        exit(0)

    # Get variable from environnement
    log_handler = logging.handlers.RotatingFileHandler(log_file_path, mode='w', backupCount=NB_OF_LOG_FILE)
    log_handler.rotator = utils.rotator
    log_handler.namer = utils.namer
    FORMAT = logging.Formatter('%(asctime)-15s %(levelname)s --- %(message)s')
    log_handler.setFormatter(FORMAT)

    my_logger = logging.getLogger()
    my_logger.setLevel(logging.DEBUG)
    my_logger.addHandler(log_handler)

    # Checking if we need to create the database
    if os.path.exists(db_name) == False:
        db_funct.create_db_schema(db_name,dir_path+'/db_functions/schema.sql')
        print('New db is initialised')
    else:
        print('No need to create DB')

    already_updated = False
    # Download the page if wasn't downloaded
    html_file_name = squad_name + "_" + str(datetime.today().strftime('%Y-%m-%d')) + ".html"
    html_file_path = path_to_save_html + "/" + html_file_name
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
    discord_msg = ""
    if already_updated == False:
        # Scrap the page
        new_squad_members_list = scraping.correct_email_protection(scraping.scrap_squadron_profile_page(html_file_path),
                            scraping.list_of_all_members(html_file_path))
        # Compare with data in database
        db_squad_list = db_funct.get_all_squad_members(db_name)
        list_create_squad, list_to_update, list_leaver  = members_fct.compare_squads_members(db_squad_list,new_squad_members_list)

        db_funct.update_squad_members_activity(db_name,list_to_update)
        
        # Inserting/deleting members to DB + notifaction to discord
        db_funct.insert_all_squad(db_name,list_create_squad)
        for el in list_create_squad:
            discord_msg = discord_msg + f":heart: A new member has joined squadron ! Welcome {el.pseudo}\n"
        db_funct.delete_list_of_members(db_name,list_leaver) # Keep an history somewhere ? # TODO#TOTHINK
        for el in list_leaver:
            discord_msg =  discord_msg + f":broken_heart: A member has left squadron ! Bye bye {el.pseudo}\n"

        # Generate graph
        for el in db_funct.get_all_squad_members(db_name):
            history_list = db_funct.get_activity_history_from_members(db_name, el.id)
            x_list = []
            y_list = []
            for elem1, elem2 in history_list:
                tmptime = datetime.strptime(elem2, '%Y-%m-%d %H:%M:%S')
                x_list.append(datetime.strptime(tmptime.strftime('%Y-%m-%d'),'%Y-%m-%d'))
                y_list.append(elem1)
                
            plt.clf()
            plt.xlabel('x - time')
            plt.ylabel('y - activity')
            plt.ylim(0, 4000)
            for i in range(len(x_list)):
                plt.annotate(y_list[i], xy=(i, y_list[i]),xytext=(-12.5,7), textcoords='offset points')
            plt.gcf().autofmt_xdate()
            plt.plot_date(x_list,y_list,color='green', linestyle='-', linewidth = 2,
                markerfacecolor='blue', markersize=7,xdate=True)
            plt.title(f'Activity history of {el.pseudo}')
            plt.savefig(f'{path_to_save_graph}/{el.pseudo}.png')
    
    # Check if we need to warn inactive members
    for el in db_funct.get_all_squad_members_with_activity(db_name):
        if members_fct.check_if_members_is_inactive(el):
            discord_msg =  discord_msg + f"This members : {el.pseudo} is inactive for more than 3 weeks\n"
    
    utils.send_discord_notif(discord_webhook_url,discord_msg) # exclude new player ?

    # Delete old HTML file
    utils.purge(path_to_save_html,f"{squad_name}_.*.html",html_file_name)
    
    # Rotate the log
    log_handler.doRollover()
    
    sys.exit(0)

if __name__=="__main__":
    main()