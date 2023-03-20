from utils.scraping import *
import csv

def main():
	html_file_location = 'tmp_dir/b3m.html'

	# print(list_of_all_members(html_file_location))

	squad_members = scrap_squadron_profile_page(html_file_location)
	json_file_location = 'tmp_dir/squad_members.json'
	write_json_file(json_file_location,squad_members)


	csv_file_location = 'tmp_dir/squad_members.csv'
	details = ['number', 'name', 'class_perso_esca', 'current_activity','role','enter_date','last_update','prev_activity']  
	write_csv_file(csv_file_location,details,squad_members)
 
if __name__=="__main__":
    main()