import sqlite3
from myclass.squad_member import Squad_member
from sqlite3 import Error

# create a new database based on sql script
def create_db_schema(db_name, script_path):
    try:
        con = sqlite3.connect(db_name)
        cursor = con.cursor()
        print("Connection is established")
        with open(script_path, 'r') as sql_file:
            sql_script = sql_file.read()
        cursor.executescript(sql_script)
        
    except Error as e:
        print(e)
    finally:
        con.close()

def insert_all_squad(db_name, list_squad_members):
    try:
        con = sqlite3.connect(db_name)
        cursor = con.cursor()
        print("Connection is established")
        for el in list_squad_members:
            mylist = list(el)
            var_string = ', '.join('?' * len(mylist))
            query_string = f"""INSERT INTO squad_member(squad_num,pseudo,class_perso_esca,current_activity,squad_role,enter_date) VALUES ({var_string});"""

            cursor.execute(query_string, mylist)
        
        con.commit()
    except Error as e:
        print(e)
    finally:
        con.close()

# Update
# Update le role aussi a terme
# 
# db_name : the name of the db to update row
# list_squad_members : a list of squad_members
def update_squad_members_activity(db_name, list_squad_members):
    try:
        con = sqlite3.connect(db_name)
        cursor = con.cursor()
        print("Connection is established")
        for el in list_squad_members:
            query_string = """UPDATE squad_member
                set current_activity=?
                where id=?;"""

            cursor.execute(query_string, el.current_activity,el.id)

        con.commit()
    except Error as e:
        print(e)
    finally:
        con.close()

