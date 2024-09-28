import argparse
import json
import sys
import os

from datetime import date, datetime


def help():
    """
    Returns help message
    """
    
    return """Convert messages to json and write them to multiple files"""


def set_args(args_parcer:argparse.ArgumentParser):
    """
    Adds arguments to the ArgumentParser object.

    Parameters:
        args_parcer (argparse.ArgumentParser): The ArgumentParser object to which arguments will be added.

    Returns:
        None. This function modifies the ArgumentParser object in-place.
    """
    
    args_parcer.add_argument(
        '-sbd',
        '--separate_by_date',
        action=argparse.BooleanOptionalAction,
        help='Separate files into folders based on date'
    )

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
        None. The function writes the json file in the specified output directory.
    """
    print("\n================================\nWriting output...")
    os.makedirs(os.path.join(sys.path[0], args.outdir), exist_ok=True)
    
    outdir = args.outdir
    last_time = datetime.fromtimestamp(0)
    
    for message in messages:
        if args.separate_by_date:
            msg_time = datetime.fromisoformat(message["timestamp"].replace("Z", "+00:00"))
            
            if msg_time.date() != last_time.date():
                outdir = os.path.join(sys.path[0], args.outdir, msg_time.strftime("%Y-%m-%d"))
                os.makedirs(outdir, exist_ok=True)
            
            last_time = msg_time
        
        with open(os.path.join(sys.path[0], outdir, message["id"]+".json"), "w", encoding="utf-8") as fl:
            fl.write(json.dumps(message))
    print("Success!")