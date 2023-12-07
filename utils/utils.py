from myclass.squad_member import squad_member_encoder
import csv
import json
import os
import re
import gzip
import shutil
from discord import SyncWebhook, HTTPException

import logging

logger = logging.getLogger("wt_log")


# Remove first n first element of a list
def divide_chunks(list, n):
    for i in range(0, len(list), n):
        yield list[i : i + n]


# file_path : ex (/etc/test.csv)
# columns : a list containng all the columns of the csv (ex : ['name','numbers'])
# data_list : a list of list of data to write in the csv file
def write_csv_file(file_path, columns, data_list):
    with open(file_path, "w", newline="") as f:
        write = csv.writer(f)
        write.writerow(columns)
        write.writerows(data_list)


# file_path : ex (/etc/test.json)
# data : the data to write in the file (must be serialisable)
def write_json_file(file_path, data):
    with open(file_path, "w") as f:
        for el in data:
            json.dump(el, f, ensure_ascii=False, indent=4, cls=squad_member_encoder)


# Delete all file matching a certain patern execpt the exclusion_file_name
def purge(dir, pattern, exlusion_file_name):
    for f in os.listdir(dir):
        if re.search(pattern, f) is not None and f != exlusion_file_name:
            os.remove(os.path.join(dir, f))


# Logging
# Used to rotate logging while zipping the previous file
def rotator(source, dest):
    with open(source, "rb") as f_in:
        with gzip.open(dest, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(source)


# Used to define log name
def namer(name):
    return name + ".gz"


# Take a long string separate in multiple line by \n
# and split it in smaller piece than the max length
# Return a list of string smaller than the max length
# EX :
# - "test\ntest\ntest\n",5 -> ["test\n","test\n","test\n","test\n"]
# - "test\ntest\ntest\n",10 -> ["test\ntest\n","test\ntest\n"]
# - "test\ntest\ntest\ntest\ntest\n",15 -> ["test\ntest\n","test\ntest\ntest\n"]
# KNOWN ERROR, if string 2 long to be split will have issue
# - "test\n",2 -> None + log error
# - "test\ntest6\n",6 -> ["test\n"] + log error
# - "test\ntest6\ntest\n",6 -> Program crash
def discord_msg_reductor(str, max_length):
    list_str = []

    if len(str) <= max_length:
        return [str]
    else:
        nbr_of_line = str.count("\n")
        if nbr_of_line <= 1:
            logger.critical("String too long to be split properly")
            return None
        firstHalf = str.split("\n", nbr_of_line // 2)[: nbr_of_line // 2]
        secondHalf = str.split("\n", nbr_of_line // 2)[(nbr_of_line // 2) :]
        cpt = 0
        isTooBig = False
        goodLenghtStr, badLenghtStr = "", ""
        while cpt < len(firstHalf):
            if not isTooBig:
                if len(goodLenghtStr + firstHalf[cpt] + "\n") <= max_length:
                    goodLenghtStr = goodLenghtStr + firstHalf[cpt] + "\n"
                else:
                    isTooBig = True
                    badLenghtStr = badLenghtStr + firstHalf[cpt] + "\n"
            else:
                badLenghtStr = badLenghtStr + firstHalf[cpt] + "\n"

            cpt += 1

        list_str.append(goodLenghtStr)
        discord_msg_reductor2(badLenghtStr + secondHalf[0], max_length, list_str)

    return list_str


def discord_msg_reductor2(str, max_length, list_str):
    if len(str) <= max_length:
        return list_str.append(str)
    else:
        nbr_of_line = str.count("\n")
        if nbr_of_line <= 1:
            logger.critical("String too long to be split properly")
            return None
        firstHalf = str.split("\n", nbr_of_line // 2)[: nbr_of_line // 2]
        secondHalf = str.split("\n", nbr_of_line // 2)[(nbr_of_line // 2) :]
        cpt = 0
        isTooBig = False
        goodLenghtStr, badLenghtStr = "", ""
        while cpt < len(firstHalf):
            if not isTooBig:
                if len(goodLenghtStr + firstHalf[cpt] + "\n") <= max_length:
                    goodLenghtStr = goodLenghtStr + firstHalf[cpt] + "\n"
                else:
                    isTooBig = True
                    badLenghtStr = badLenghtStr + firstHalf[cpt] + "\n"
            else:
                badLenghtStr = badLenghtStr + firstHalf[cpt] + "\n"
            cpt += 1

        list_str.append(goodLenghtStr)
        discord_msg_reductor2(badLenghtStr + secondHalf[0], max_length, list_str)

    return list_str


# Function who send a message, if message is bigger than X char it will split
# in smaller message
# Pre : a message needs to be separate by '\n'
def send_discord_notif(webhook_url, message):
    try:
        webhook = SyncWebhook.from_url(webhook_url)
        for el in discord_msg_reductor(message, 1950):
            logger.info(f"Sending message (size =  {len(el)}): {el}")
            webhook.send(el)
    except HTTPException as e:
        # Error whit send , not printed in the log... (async ? impossible to catch ? )
        logger.critical("Error while sending message to webhook : ", e)
    except Exception as e:
        logger.critical("Error while sending message to discord : ", e)
