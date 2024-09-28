
from datetime import datetime

import sys
import os

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Messages</title>
        {css}
    </head>
    <body>
        {output}
    </body>
</html>
'''

REPLY_TEMPLATE = """<a href="#{id}">┏━━ <strong>{author}</strong>: {message}{file_img}</a>"""
MESSAGE_TEMPLATE = """
<div class="message" id="#{id}">
    <div class="reply">{reply}</div>
    <img class="pfp" src="{author_pfp}">
    <div class="message_container">
        <strong>{author}</strong><small>{time}</small> 
        <div class="text">{message}</div>
    </div>
    {attachments}
</div>
"""


def help():
    """
    Returns help message
    """
    
    return """Convert chat to html page"""


import argparse

def set_args(args_parcer:argparse.ArgumentParser):
    """
    Adds arguments to the ArgumentParser object.

    Parameters:
        args_parcer (argparse.ArgumentParser): The ArgumentParser object to which arguments will be added.

    Returns:
        None. This function modifies the ArgumentParser object in-place.
    """
    args_parcer.add_argument(
        '-css', '--css_path',
        type=str,
        default=os.path.join(sys.path[0], "process", "html", "pretty.css"),
        help='Path to CSS file'
    )
    args_parcer.add_argument(
        '-pack', '--pack_css_in_html',
        action=argparse.BooleanOptionalAction,
        help='Pack CSS file into HTML page'
    )

def check_args(args:argparse.Namespace):
    return os.path.exists(args.css_path)


def process_attachments(attachments):
    if attachments == [] or not attachments:
        return ""
    
    output = "<ul class=\"attachments\">"
    for attachment in attachments:
        if attachment["content_type"].split("/")[0] == "image":
            output += f'<li><img src="{attachment["url"]}" /></li>'
        else:
            output += f'<li><a href="{attachment["url"]}">{attachment["filename"]}</a></li>'
    
    output += "</ul>"
    
    return output

def process_messages(messages, args):
    """
    Processes a list of messages and generates an html page.

    Parameters:
        messages (list): A list of messages to process

        args (Namespace): An object containing command-line arguments. It should have an attribute "outdir" (str)
            representing the output directory path.

    Returns:
        None. The function writes the html file in the specified output directory.
    """
    messages = messages[::-1]

    output = []

    prev_time = None
    print("\n================================\nMessages processing...")
    for i, message in enumerate(messages):
        print(f"Process message {message['id']}")
        msg_time = datetime.fromisoformat(message["timestamp"].replace("Z", "+00:00"))

        if prev_time:
            sub = msg_time - prev_time

            if msg_time.day - prev_time.day != 0 or msg_time.day - prev_time.day < 0:
                output.append(f"<div class=\"new-day\">{msg_time.year}-{msg_time.month}-{msg_time.day}</div>\n")
            elif sub.total_seconds() > 60*5:
                output.append("<div class=\"5min-separator\"></div>")
            elif (msg_time - prev_time).total_seconds() > 60:
                output.append("<br>")

        reply = ""
        if "message_reference" in message:
            for j, msg in enumerate(messages[::-1], i):
                if msg["id"] == message["message_reference"]["message_id"]:
                    cont = msg["content"].replace("<", "").replace(">", "").replace("```", "")
                    reply = (REPLY_TEMPLATE.format(
                        id       = msg["id"],
                        author   = msg["author"]["global_name"] if msg["author"]["global_name"] else msg["author"]["username"],
                        message  = cont if len(cont) <= 60 else cont[0:60]+"...",
                        file_img = " <i class='fas fa-paperclip'></i>" if message["attachments"] != [] else ""
                    ))
                    break

        output.append(MESSAGE_TEMPLATE.format( #TODO: доделать css для reply
            id          = message["id"],
            reply       = reply,
            author_pfp  = f"https://cdn.discordapp.com/avatars/{message["author"]["id"]}/{message["author"]["avatar"]}.png?size=4096",
            time        = msg_time.strftime("%Y-%m-%d %H:%M:%S"),
            author      = message["author"]["global_name"] if message["author"]["global_name"] else message["author"]["username"],
            message     = message["content"].replace("```", "<code>"),
            attachments = process_attachments(message["attachments"])
        ))

        prev_time = msg_time

    print("\n================================\nWriting output...")
    with open(os.path.join(sys.path[0], args.outdir), "w", encoding="utf-8") as fl:
        if args.pack_css_in_html:
            with open(args.css_path, "r", encoding="utf-8") as css_fl:
                css = css_fl.read()

            fl.write(HTML_TEMPLATE.format(
                css = f"<style>{css}</style>",
                output = "\n".join(output)
            ))
        else:
            fl.write(HTML_TEMPLATE.format(
                    css = f"<link rel=\"stylesheet\" href=\"{args.css_path}\">",
                    output = "\n".join(output)
                ))
    print("Success!")