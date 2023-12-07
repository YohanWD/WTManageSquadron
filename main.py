import logging
import sys
import os
import logging.handlers

from db_functions import db_funct

from utils import members_fct, scraping, utils, graph, load_env_var

from datetime import datetime


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Loading all env variables
    path_to_env = os.path.join(dir_path, ".env")
    try:
        (
            squad_url,
            squad_name,
            db_name,
            discord_webhook_url,
            path_to_save_graph,
            path_to_save_html,
        ) = load_env_var.laod_required_vars(path_to_env)
        (
            nb_inac_day,
            min_act_req,
            log_file_path,
            NB_OF_LOG_FILE,
        ) = load_env_var.load_optional_vars(path_to_env)
    except Exception as e:
        msg = f"Error while loading variable : {e}"
        print(msg)
        exit(0)

    # Setting up logging system
    log_handler = logging.handlers.RotatingFileHandler(
        log_file_path, mode="w", backupCount=NB_OF_LOG_FILE
    )
    log_handler.rotator = utils.rotator
    log_handler.namer = utils.namer
    FORMAT = logging.Formatter("%(asctime)-15s %(levelname)s --- %(message)s")
    log_handler.setFormatter(FORMAT)

    my_logger = logging.getLogger("wt_log")
    my_logger.setLevel(logging.INFO)
    my_logger.addHandler(log_handler)

    # Checking if we need to create a new the database
    if not os.path.exists(db_name):
        db_funct.create_db_schema(db_name, dir_path + "/db_functions/schema.sql")
        my_logger.info("New db is initialised")
    else:
        my_logger.info("No need to create DB")

    already_updated = False
    # Download the page if wasn't downloaded
    html_file_name = (
        squad_name + "_" + str(datetime.today().strftime("%Y-%m-%d")) + ".html"
    )
    html_file_path = path_to_save_html + "/" + html_file_name
    if not os.path.exists(html_file_path):
        if not scraping.download_web_page(squad_url, html_file_path):
            my_logger.critical("Error during the page download")
            sys.exit(0)
        else:
            my_logger.info("HTML page was downloaded")
    else:
        my_logger.info("HTML page already downloaded, skipping insert in DB")
        already_updated = True

    # Update database
    discord_msg = ""
    if not already_updated:
        # Scrap the page
        new_squad_members_list = scraping.correct_email_protection(
            scraping.scrap_squadron_profile_page(html_file_path),
            scraping.list_of_all_members(html_file_path),
        )
        # Compare with data in database
        db_squad_list = db_funct.get_all_squad_members(db_name)
        (
            list_create_squad,
            list_to_update,
            list_leaver,
        ) = members_fct.compare_squads_members(db_squad_list, new_squad_members_list)

        db_funct.update_squad_members_activity(db_name, list_to_update)

        # Inserting/deleting members to DB + adding msg to discord string
        db_funct.insert_all_squad(db_name, list_create_squad)
        for el in list_create_squad:
            discord_msg = (
                discord_msg
                + f":heart: A new member has joined squadron ! Welcome {el.pseudo}\n"
            )
        db_funct.delete_list_of_members(
            db_name, list_leaver
        )  # Keep an history somewhere ? # TODO#TOTHINK
        for el in list_leaver:
            discord_msg = (
                discord_msg
                + f":broken_heart: A member has left squadron ! Bye bye {el.pseudo}\n"
            )

        # Generate graph
        graph.generate_activity_graph(db_name, path_to_save_graph)

    # Check if we need to warn for inactive members
    for el in db_funct.get_all_squad_members_last_x_day_of_activity(
        db_name, nb_inac_day
    ):
        if members_fct.check_if_members_is_inactive(el, nb_inac_day, min_act_req):
            discord_msg = (
                discord_msg
                + f"{el.pseudo} is inactive for more than {nb_inac_day} days\n"
            )

    if discord_msg != "":
        utils.send_discord_notif(
            discord_webhook_url, discord_msg
        )  # exclude new player ?

    # Delete old HTML file
    utils.purge(path_to_save_html, f"{squad_name}_.*.html", html_file_name)

    # Rotate the log
    log_handler.doRollover()

    sys.exit(0)


if __name__ == "__main__":
    main()
