from utils.scraping import *
import logging, sys, os
from dotenv import load_dotenv

def main():
    # Get variable from environnement
    logging.basicConfig(filename='logfile.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    res = load_dotenv(dotenv_path='.env')
    if res == False:
        logging.critical("Create .env file before running the script! See README.md")
        sys.exit(0)
    
    squad_url = os.getenv('SQUADRON_URL')
    squad_name = os.getenv('SQUAD_NAME')

    # Download the page if wasn't downloaded
    html_file_path = "tmp_dir/b3m_" + str(datetime.today().strftime('%Y-%m-%d')) + ".html"
    if os.path.exists(html_file_path) == False:
        if download_web_page(squad_url,html_file_path):
            logging.info("Error during the page download")
    else:
        logging.debug("HTML page already downloaded")
    
    # 
    
    
    # Scrap the page
    squad_members = correct_email_protection(scrap_squadron_profile_page(html_file_path),
                        list_of_all_members(html_file_path))
    
    # Compare with data in database
    # get_db_squad_members(db_name)
    # list_new, list_leaver, list_to_update = compare_squads_members(list1,list2)
    
    # Update database
    # update_members (list_to_update)
    # insert_members (list_new)
    # delete_members (list_leaver) # Keep an history somewhere ? # TODO#TOTHINK
    
    # Check if we need to warn inactive members
    # for el in squadmembers calculate_activity # exluce new player ?
    
    # Generate graph
 
    # Delete old HTML file

if __name__=="__main__":
    main()