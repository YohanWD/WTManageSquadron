import sqlite3
from myclass.squad_member import Squad_member
from sqlite3 import Error

import logging
logger = logging.getLogger(__name__)

# create a new database based on sql script
def create_db_schema(db_name, script_path):
    try:
        con = sqlite3.connect(db_name)
        cursor = con.cursor()
        logger.debug("Connection is established to create db schema")
        with open(script_path, 'r') as sql_file:
            sql_script = sql_file.read()
        cursor.executescript(sql_script)
        
    except Error as e:
        logger.error(f'Db error in fct create_db_schema : {str(e)}')
    finally:
        con.close()

def insert_all_squad(db_name, list_squad_members):
    try:
        con = sqlite3.connect(db_name)
        cursor = con.cursor()
        logger.debug("Connection is established to insert all squad_members")
        # con.executemany("insert into person(firstname, lastname) values (?, ?)", persons)
        for el in list_squad_members:
            mylist = list(el)
            var_string = ', '.join('?' * len(mylist))
            query_string = f"""INSERT INTO squad_member(squad_num,pseudo,class_perso_esca,current_activity,squad_role,enter_date) VALUES ({var_string});"""

            cursor.execute(query_string, mylist)
            logger.debug(f"{el.pseudo} has been added to DB")
        
        con.commit()
    except Error as e:
        logger.error(f'Db error in fct insert_all_squad : {str(e)}')
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
        logger.debug("Connection is established. Updating squad_members")
        for el in list_squad_members:
            query_string = """UPDATE squad_member
                set current_activity=?
                where pseudo=?"""

            cursor.execute(query_string, (el.current_activity,el.pseudo))

        con.commit()
    except Error as e:
        logger.error(f'Db error in fct update_squad_members_activity : {str(e)}')
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
        logger.debug("Connection is established to get all squad members")
        cursor.execute('SELECT * from  squad_member')
        rows = cursor.fetchall()
        for r in rows:
            squad_members_list.append(Squad_member.from_db(r))

    except Error as e:
        logger.error(f'Db error in fct get_all_squad_members : {str(e)}')
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
        logger.debug("Connection to db is established to get squad_members_activity")

        cpt = 0
        for member in squad_members_list:
            cursor.execute('SELECT * from activity_history where squad_member_id = ? ORDER BY last_update',(member.id,))
            rows = cursor.fetchall()
            for r in rows:
                squad_members_list[cpt].appendActivity(r)
            
            cpt +=1

    except Error as e:
        logger.error(f'Db error in fct get_all_squad_members_with_activity : {str(e)}')
    finally:
        con.close()
    
    return squad_members_list

# PRE : A valid number of day, need to be greater than 0 (default = 21)
# VARS : 
# - db_name -> the name of the database to gather info from
# - nb_of_day (integer) -> Number of day to get last activity from all members
# Return : a list of Squad_members with their last X day of activity
def get_all_squad_members_last_x_day_of_activity(db_name,nb_of_day=21):
    nb_of_day = 21 if nb_of_day is None or nb_of_day < 0 else nb_of_day
    squad_members_list = get_all_squad_members(db_name)
    try:
        con = sqlite3.connect(db_name)
        con.row_factory = dict_factory
        cursor = con.cursor()
        logger.debug("Connection to db is established to get get_all_squad_members_last_x_day_of_activity")

        cpt = 0
        for member in squad_members_list:
            str_day = f"-{nb_of_day} day"
            query="""
                SELECT * from activity_history where squad_member_id = ? 
                and last_update > DATETIME('now',?)
                ORDER BY last_update
            """
            cursor.execute(query,(member.id,str_day))
            rows = cursor.fetchall()
            for r in rows:
                squad_members_list[cpt].appendActivity(r)
            
            cpt +=1

    except Error as e:
        logger.error(f'Db error in fct get_all_squad_members_with_activity : {str(e)}')
    finally:
        con.close()
    
    return squad_members_list


def delete_list_of_members(db_name,list_squad_members):
    try:
        con = sqlite3.connect(db_name)
        cursor = con.cursor()
        logger.debug("Connection is established to delete squad members")
        for el in list_squad_members:
            query_string = """Delete from squad_member
                where id=?"""

            cursor.execute(query_string, (el.id,))
            logger.debug(f"{el.pseudo} has been remove from DB")

        con.commit()
    except Error as e:
        logger.error(f'Db error in fct delete_list_of_members : {str(e)}')
    finally:
        con.close()

def get_activity_history_from_members(db_name, members_id):
    mylist = []
    try:
        con = sqlite3.connect(db_name)
        cursor = con.cursor()
        logger.debug("Connection is established to get activity from a member")
        query_string = """select activity,last_update from activity_history
            where squad_member_id=?"""

        cursor.execute(query_string, (members_id,))
        mylist = cursor.fetchall()

    except Error as e:
        logger.error(f'Db error in fct get_activity_history_from_members : {str(e)}')
    finally:
        con.close()    
    
    return mylist