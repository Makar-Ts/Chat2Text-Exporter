from datetime import datetime

import argparse
import sys
import os


REPLY_TEMPLATE = """\nReply | {author}: {message}{file_img}"""
MESSAGE_TEMPLATE = """{time} | {author}: {message}{attachments}"""

def help():
    """
    Returns help message
    """
    
    return """Convert messages to one text file"""


import argparse

def set_args(args_parcer:argparse.ArgumentParser):
    """
    Adds arguments to the ArgumentParser object.

    Parameters:
        args_parcer (argparse.ArgumentParser): The ArgumentParser object to which arguments will be added.

    Returns:
        None. This function modifies the ArgumentParser object in-place.
    """
    pass

def check_args(args:argparse.Namespace):
    return True


def process_messages(messages, args):
    """
    Processes a list of messages and generates a formatted output.

    Parameters:
        messages (list): A list of messages to process

        args (Namespace): An object containing command-line arguments. It should have an attribute "outdir" (str)
            representing the output directory path.

    Returns:
        None. The function writes the formatted output to a file in the specified output directory.
    """
    messages = messages[::-1]
    
    output = []

    prev_time = None
    print("\n================================\nMessages processing...")
    for i, message in enumerate(messages):
        print(f"Process message {message["id"]}")
        msg_time = datetime.fromisoformat(message["timestamp"].replace("Z", "+00:00"))
        
        if prev_time:
            sub = msg_time - prev_time
            
            if msg_time.day - prev_time.day != 0 or msg_time.day - prev_time.day < 0:
                output.append(f"\n====================================\n{msg_time.year}-{msg_time.month}-{msg_time.day}\n")
            elif sub.total_seconds() > 60*5:
                output.append("\n\n")
            elif (msg_time - prev_time).total_seconds() > 60:
                output.append("")
        
        if "message_reference" in message:
            for j, msg in enumerate(messages[::-1], i):
                if msg["id"] == message["message_reference"]["message_id"]:
                    cont = msg["content"].replace("<", "").replace(">", "").replace("```", "")
                    
                    output.append(REPLY_TEMPLATE.format(
                            author  =msg["author"]["global_name"] if msg["author"]["global_name"] else msg["author"]["username"],
                            message =cont if len(cont) <= 60 else cont[0:60]+"...",
                            file_img=" 📁" if message["attachments"] != [] else ""
                        ))
                    break
        
        output.append(MESSAGE_TEMPLATE.format(
                time        =msg_time.strftime("%Y-%m-%d %H:%M:%S"),
                author      =message["author"]["global_name"] if message["author"]["global_name"] else message["author"]["username"],
                message     =message["content"].replace("```", "\n```"),
                attachments ="\n - "+"\n - ".join([f"{att["filename"]} ({att["url"]})" for att in message["attachments"]])+"\n" if message["attachments"] != [] else ""
            ))

        prev_time = msg_time

    print("\n================================\nWriting output...")
    with open(os.path.join(sys.path[0], args.outdir), "w", encoding="utf-8") as fl:
        fl.write("\n".join(output))
    print("Success!")
