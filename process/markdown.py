from datetime import datetime

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
        None. The function writes the formatted output to a file in the specified output directory.
    """
    
    output = []

    prev_time = None
    print("\n================================\nMessages processing...")
    for i, message in enumerate(messages):
        print(f"Process message {message["id"]}")
        msg_time = datetime.fromisoformat(message["timestamp"].replace("Z", "+00:00"))
        if prev_time:
            sub = msg_time - prev_time
            if msg_time.day - prev_time.day != 0 or msg_time.day - prev_time.day < 0:
                output.append(f"\n---\n**{msg_time.year}-{msg_time.month}-{msg_time.day}**\n")
            elif sub.total_seconds() > 60*5:
                output.append("\n")
            elif (msg_time - prev_time).total_seconds() > 60:
                output.append("")
        
        if "message_reference" in message:
            for j, msg in enumerate(messages[::-1], i):
                if msg["id"] == message["message_reference"]["message_id"]:
                    cont = msg["content"].replace("<", "").replace(">", "").replace("```", "")
                    
                    output.append(f"<sub>Reply | {msg["author"]["global_name"] if msg["author"]["global_name"] else msg["author"]["username"]}: {cont if len(cont) <= 60 else cont[0:60]+"..."}{" :memo:" if message["attachments"] != [] else ""}</sub>")
                    break
        
        output.append(f"""{msg_time.strftime("%Y-%m-%d %H:%M:%S")} | **{
            message["author"]["global_name"] if message["author"]["global_name"] else message["author"]["username"]
                            }**: {message["content"].replace("```", "\n```")} {"\n - "+"\n - ".join([f"[{att["filename"]}]({att["url"]}) ({att["width"]}x{att["height"]})" for att in message["attachments"]])+"\n" if message["attachments"] != [] else ""}""")

        prev_time = msg_time

    print("\n================================\nWriting output...")
    with open(os.path.join(sys.path[0], args.outdir), "w", encoding="utf-8") as fl:
        fl.write("\n".join(output))
    print("Success!")
