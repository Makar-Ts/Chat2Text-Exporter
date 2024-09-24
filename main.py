# pylint: disable=line-too-long, invalid-name, import-error, multiple-imports, unspecified-encoding, broad-exception-caught, trailing-whitespace, no-name-in-module, unused-import

from os import listdir

import configparser
import importlib
import argparse
import time
import math
import sys
import os
import requests

import local.files_check
local.files_check.main(0, "local") # check for config.ini



#=======================================================================
#============================= Args set ================================
#=======================================================================


parser = argparse.ArgumentParser(description='From discord channel to markdown file')
parser.add_argument(
    'channel_id', 
    type=int,
    help='Discord Channel ID'
)
parser.add_argument(
    'outdir', 
    type=str, 
    help='Output dir for markdown file'
)
parser.add_argument(
    'process_type', 
    type=str, 
    help='Process type'
)
parser.add_argument(
    '-ml',
    '--messages_limit',
    type=int,
    default=50,
    help='Messages limit per request'
)
parser.add_argument(
    '-b',
    '--before',
    type=int,
    default=None,
    help='Get messages before this message (id)'
)
parser.add_argument(
    '-a',
    '--after',
    type=int,
    default=None,
    help='Get messages after this message (id)'
)
parser.add_argument(
    '-t',
    '--timeout',
    type=int,
    default=0,
    help='Pause between requests in miliseconds. Needed if you get more than 100 messages = more than 1 request (for safety)'
)
parser.add_argument(
    '--all',
    type=bool,
    default=False,
    help='NOT RECOMMENDED FOR USE!!! Get all messages in the channel'
)
args = parser.parse_args()



#=======================================================================
#============================ Args check ===============================
#=======================================================================


if args.messages_limit <= 0:
    print("Invalid messages_limit! Value should be more than 0")
    exit(1)


def get_all_process_types(path, prefix=""):
    processes = []
    
    for part in listdir(path):
        if part == "__pycache__":
            continue
        
        if os.path.isfile(os.path.join(path, part)):
            if part.split(".")[-1] == "py":
                processes.append(prefix+part.split(".")[0])
        else:
            processes += get_all_process_types(os.path.join(path, part), prefix+part+".")
    
    return processes

    
path = os.path.join(sys.path[0], "process")
process_types = get_all_process_types(path)
# getting all files from ./process and delete .py in the end

if args.process_type not in process_types:
    print("Invalid process_type!")
    print(f"Available process types: {"\n - "+"\n - ".join(map(lambda x: x+"\n    "+importlib.import_module("process."+x, package=None).help(), process_types))}")
    exit(1)



#=======================================================================
#============================== Config =================================
#=======================================================================


config = configparser.ConfigParser()
config.read(os.path.join(sys.path[0], "local", "config.ini")) #["DISCORD_LOGIN"]["TOKEN"]

if config["DISCORD_LOGIN"]["TOKEN"] == "token" or not config["DISCORD_LOGIN"]["TOKEN"]:
    print("Please paste your Discord token to ./local/config.ini")
    exit(1)



#=======================================================================
#=========================== Request Init ==============================
#=======================================================================


print("\n================================")
print("Request to the server...")



#=======================================================================
#========================= All-Out Request =============================
#=======================================================================

if args.all:
    print("\nWARNING: Program will send more than 1 request\n")
    messages = []
    
    last_message = None
    limit = -1 # Python hasn't do-while statement T-T
    mes_json = []
    
    counter = 0
    
    while len(mes_json) >= limit:
        limit = 100
        
        print(f"Request number {counter}. Init request...")
        messages_req = requests.get(
                            f"""https://discord.com/api/channels/{
                                args.channel_id}/messages?limit={limit}{
                                "&before="+last_message if last_message else ""}{
                                "&after="+args.after if args.after else ""}""",
                            headers={'Authorization': config["DISCORD_LOGIN"]["TOKEN"]},
                            timeout=300)
        
        if messages_req.status_code != 200:
            print(f"Error fetching messages: {messages_req.status_code}")
            exit(1)
        print("Success!")
        
        mes_json = messages_req.json()
        messages += mes_json
        
        
        last_message = messages[-1]["id"]
        counter += 1
        
        time.sleep(args.timeout/1000)



#=======================================================================
#===================== Multi Request (limit>100) =======================
#=======================================================================

elif args.messages_limit > 100:
    print("\nWARNING: If messages_limit is greater than 100 program will send more than 1 request\n")
    messages = []
    
    request_count = args.messages_limit/100 # 1 request = 100 messages max
    last_message = None

    while request_count > 0:
        limit = math.floor(max(0, min(1, request_count))*100) # clamp
        
        print(f"Request count: {request_count}. Init request...")
        messages_req = requests.get(
                            f"""https://discord.com/api/channels/{
                                args.channel_id}/messages?limit={limit}{
                                "&before="+last_message if last_message else ""}{
                                "&after="+args.after if args.after else ""}""",
                            headers={'Authorization': config["DISCORD_LOGIN"]["TOKEN"]},
                            timeout=300)
        
        if messages_req.status_code != 200:
            print(f"Error fetching messages: {messages_req.status_code}")
            exit(1)
        print("Success!")
        
        mes_json = messages_req.json()
        messages += mes_json
        
        
        if len(mes_json) < limit:
            print("Channel start reached, no more requests")
            break
        
        request_count -= 1
        last_message = messages[-1]["id"]
                
        time.sleep(args.timeout/1000)
        
        
        
#=======================================================================
#========================== Single Request =============================
#=======================================================================

else:
    req_args = []
    if args.before:
        req_args.append(f"before={args.before}")
    if args.after:
        req_args.append(f"after={args.after}")
    if args.messages_limit:
        req_args.append(f"limit={args.messages_limit}")
    
    messages_req = requests.get(
                            f"https://discord.com/api/channels/{args.channel_id}/messages?{"&".join(req_args)}",
                            headers={'Authorization': config["DISCORD_LOGIN"]["TOKEN"]},
                            timeout=300)

    if messages_req.status_code != 200:
        print(f"Error fetching messages: {messages_req.status_code}")
        exit(1)
    
    messages = messages_req.json()[::-1]
    print("Success!")



#=======================================================================
#======================= Messages Processing ===========================
#=======================================================================


print(f"\nProcess module is {"process."+args.process_type}")

process_module = importlib.import_module("process."+args.process_type, package=None)
process_module.process_messages(messages, args)
