import json
import sys
import os



def help():
    """
    Returns help message
    """
    
    return """Convert messages to json and write them to one file"""


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
        None. The function writes the json file in the specified output directory.
    """
    print("\n================================\nWriting output...")
    with open(os.path.join(sys.path[0], args.outdir), "w", encoding="utf-8") as fl:
        fl.write(json.dumps(messages))
    print("Success!")