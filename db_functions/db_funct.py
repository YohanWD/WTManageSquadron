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
        # con.executemany("insert into person(firstname, lastname) values (?, ?)", persons)
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
                where id=?"""

            cursor.execute(query_string, (el.current_activity,el.id))

        con.commit()
    except Error as e:
        print("Error during update ",e)
    finally:
        con.close()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_all_squad_members(db_name):
    squad_members_list = []
    try:
        con = sqlite3.connect(db_name)
        con.row_factory = dict_factory
        cursor = con.cursor()
        print("Connection is established")
        cursor.execute('SELECT * from  squad_member')
        rows = cursor.fetchall()
        for r in rows:
            squad_members_list.append(Squad_member.from_db(r))

    except Error as e:
        print(e)
    finally:
        con.close()
    
    return squad_members_list

# Maybe we can do it better
def get_all_squad_members_with_activity(db_name):
    squad_members_list = get_all_squad_members(db_name)
    try:
        con = sqlite3.connect(db_name)
        con.row_factory = dict_factory
        cursor = con.cursor()
        print("Connection is established")

        cpt = 0
        for member in squad_members_list:
            cursor.execute('SELECT * from activity_history where squad_member_id = ? ORDER BY last_update',(member.id,))
            rows = cursor.fetchall()
            for r in rows:
                squad_members_list[cpt].appendActivity(r)
            
            cpt +=1

    except Error as e:
        print(e)
    finally:
        con.close()
    
    return squad_members_list


def delete_list_of_members(db_name,list_squad_members):
    try:
        con = sqlite3.connect(db_name)
        cursor = con.cursor()
        print("Connection is established")
        for el in list_squad_members:
            query_string = """Delete from squad_member
                where id=?"""

            cursor.execute(query_string, (el.id,))

        con.commit()
    except Error as e:
        print("Error during members deletion : ", e)
    finally:
        con.close()