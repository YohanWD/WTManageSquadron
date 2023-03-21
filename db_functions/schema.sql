------------ TABLE CREATION ------------
-- DROP TABLE activity_history;
-- DROP TABLE squad_members;

CREATE TABLE IF NOT EXISTS squad_member(id integer PRIMARY KEY,
    squad_num integer NOT NULL,
    pseudo varchar(64) NOT NULL, 
    class_perso_esca integer NOT NULL,
    current_activity integer NOT NULL,
    squad_role varchar(64) CHECK (squad_role in ('Private','Commander','Officer','Deputy','Sergeant')) NOT NULL,
    enter_date varchar(64) NOT NULL,
    last_update varchar(64) NOT NULL);

CREATE TABLE IF NOT EXISTS activity_history(id integer PRIMARY KEY,
    activity integer NOT NULL,
    last_update string NOT NULL,
    squad_member_id INTEGER REFERENCES squad_member(id));
---------------------------------

------------ TRIGGER ------------
CREATE OR REPLACE TRIGGER update_activity 
   AFTER INSERT 
   ON squad_member
BEGIN
 INSERT INTO activity_history (activity,last_update,squad_member_id)
        SELECT  sm.current_activity, sm.last_update, sm.id
        FROM squad_member sm
        WHERE sm.id = new.ID;
END;

---------------------------------

---------- TEST INSERT ----------
-- INSERT INTO squad_member(squad_num,pseudo,class_perso_esca,current_activity,squad_role,enter_date,
-- last_update) VALUES(1,'test',0,0,'Private','2023-01-25','2023-02-02');
---------------------------------