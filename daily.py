from utils.scraping import *
import csv

def main():
    
    # Download the page
    url = "https://warthunder.com/en/community/claninfo/Belgian%20Red%20Devils"
    html_file_location = download_web_page(url) # ADD antispam protection ? like if file already exist don't download ? one scrap a day keeps the cloudflare away ?
    
    
    # Scrap the page
    squad_members = correct_email_protection(scrap_squadron_profile_page(html_file_location),
                        list_of_all_members(html_file_location))
    
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
 
if __name__=="__main__":
    main()