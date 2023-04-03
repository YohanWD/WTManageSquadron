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
    last_update datetime);

CREATE TABLE IF NOT EXISTS activity_history(id integer PRIMARY KEY,
    activity integer NOT NULL,
    squad_member_id INTEGER REFERENCES squad_member(id),
    last_update datetime);


 CREATE TRIGGER sm_insert_update_date AFTER INSERT ON squad_member
    BEGIN
        update squad_member SET last_update = datetime('now') WHERE id = new.ID;
    END;
CREATE TRIGGER sm_update_update_date AFTER UPDATE ON squad_member
    BEGIN
        update squad_member SET last_update = datetime('now') WHERE id = new.ID;
    END;


CREATE TRIGGER ah_insert_update_date AFTER INSERT ON activity_history
    BEGIN
        update activity_history SET last_update = datetime('now') WHERE id = new.ID;
    END;
CREATE TRIGGER ah_update_update_date AFTER UPDATE ON activity_history
    BEGIN
        update activity_history SET last_update = datetime('now') WHERE id = new.ID;
    END;

---------------------------------

------------ TRIGGER ------------
CREATE TRIGGER IF NOT EXISTS update_activity_after_insert_squadron_members 
   AFTER INSERT 
   ON squad_member
BEGIN
 INSERT INTO activity_history (activity,last_update,squad_member_id)
        SELECT  sm.current_activity, sm.last_update, sm.id
        FROM squad_member sm
        WHERE sm.id = new.ID;
END;


CREATE TRIGGER IF NOT EXISTS update_activity_after_update_squadron_members 
   AFTER UPDATE OF 'current_activity'
   ON squad_member
BEGIN
 INSERT INTO activity_history (activity,last_update,squad_member_id)
        SELECT  sm.current_activity, sm.last_update, sm.id
        FROM squad_member sm
        WHERE sm.id = new.ID;
END;
---------------------------------

---------- TEST INSERT/UPDATE ----------
-- INSERT INTO squad_member(squad_num,pseudo,class_perso_esca,current_activity,squad_role,enter_date) VALUES(1,'test',0,10,'Private','2023-01-25');
-- UPDATE squad_member set current_activity=100 where id=1;
---------------------------------
