-- DROP TABLE IF EXISTS squad_member;

CREATE TABLE IF NOT EXISTS squad_member(id integer PRIMARY KEY,
    squad_num integer NOT NULL,
    pseudo varchar(64) NOT NULL, 
    class_perso_esca integer NOT NULL,
    current_activity integer NOT NULL,
    squad_role varchar(64) CHECK (squad_role='Private' OR squad_role='Commander' OR squad_role='Officer' OR squad_role='Deputy' OR squad_role='Sergeant') NOT NULL,
    enter_date varchar(64) NOT NULL,
    last_update varchar(64) NOT NULL,
    prev_activity integer);

-- INSERT INTO squad_member(squad_num,pseudo,class_perso_esca,current_activity,squad_role,enter_date,
-- last_update) VALUES(1,'test',0,0,'Private','2023-01-25','2023-02-02');