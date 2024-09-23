import json
import sys
import os

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