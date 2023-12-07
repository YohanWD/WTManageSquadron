import os
import sys
from dotenv import load_dotenv


def load_env_file(abs_path_to_env_file):
    res = load_dotenv(dotenv_path=abs_path_to_env_file)
    if not res:
        print("Create .env file before running the script! See README.md")
        sys.exit(0)


def laod_required_vars(abs_path_to_env_file):
    load_env_file(abs_path_to_env_file)
    try:
        squad_url = os.environ["SQUADRON_URL"]
        squad_name = os.environ["SQUAD_NAME"]
        db_name = os.environ["DB_NAME"]
        discord_webhook_url = os.environ["DISCORD_WEBHOOK_URL"]
        path_to_save_graph = os.environ["path_to_save_graph"]
        path_to_save_html = os.environ["path_to_save_html_file"]

    except Exception as e:
        msg = (
            "One or more env variable are not set, "
            f"please verify following variable : {e}"
        )
        print(msg)
        exit(0)

    return (
        squad_url,
        squad_name,
        db_name,
        discord_webhook_url,
        path_to_save_graph,
        path_to_save_html,
    )


def load_optional_vars(abs_path_to_env_file):
    load_env_file(abs_path_to_env_file)
    try:
        log_file_path = os.getenv("LOGFILE_LOCATION")
        log_file_path = (
            "squadron_script.log" if log_file_path is None else log_file_path
        )
        NB_OF_LOG_FILE = os.getenv("NB_OF_LOG_FILE")
        NB_OF_LOG_FILE = 8 if NB_OF_LOG_FILE is None else int(NB_OF_LOG_FILE)
        inactivity_in_day = os.getenv(
            "consecutive_day_of_inactivty"
        )  # Can be None (retrocompatIssue)
        inactivity_in_day = 21 if inactivity_in_day is None else int(inactivity_in_day)
        min_activiy_required = os.getenv("min_activity_required")
        min_activiy_required = (
            0 if min_activiy_required is None else int(min_activiy_required)
        )
        # day_of_grace  = os.getenv('nb_day_of_grace')
        # day_of_grace = 0 if day_of_grace is None else int(day_of_grace)

        if NB_OF_LOG_FILE < 0:
            NB_OF_LOG_FILEvalue_error = ValueError(
                "NB_OF_LOG_FILE should be a positive number (>=0)"
            )
            raise NB_OF_LOG_FILEvalue_error

        if inactivity_in_day < 0:
            inactivity_in_day_value_error = ValueError(
                "inactivity_in_day should be a positive number (>=0)"
            )
            raise inactivity_in_day_value_error

        if min_activiy_required < 0:
            min_activiy_required_value_error = ValueError(
                "min_activiy_required should be a positive number (>=0)"
            )
            raise min_activiy_required_value_error

        # if day_of_grace < 0:
        #     day_of_grace_value_error = ValueError('day_of_grace should
        #                                   be a positive number (>=0)')
        #     raise day_of_grace_value_error
    except Exception as e:
        raise e

    return (
        inactivity_in_day,
        min_activiy_required,
        log_file_path,
        NB_OF_LOG_FILE,
    )  # day_of_grace
