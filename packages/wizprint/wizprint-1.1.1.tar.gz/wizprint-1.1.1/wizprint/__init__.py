# -*- coding: utf-8 -*-
import random
"""
wprint; A Small Gimmick that makes printing tasks to console just a bit more fun by introducing a Wizard that will tell you your customized message in a bubble

wprint("Hello, world!") 

 .://+///:-`   .://+++oo+++++//:-.`-:://////::-
 s+++++++++oo+oo+++++++++++++++++oo+++++++++++os. 
 'o˖˖Hello,˖world!˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖oo
  :/+++///::+ooooooo+os+++++s+oooo+oooooooooooo+/`
                        +o++o+`   `````     ```
                        -s+.
                           🧙

Standard messages show a small bubble, you can expand this however by adding a signature with the option signed="Pythonuigi"
wprint("Hello, Pythonario", signed="Process Peach", wiz="p")

  .://+///:-`  .://+++oo++++//:-.`-:://////::-
   s+++++++++oo+oo++++++++++++++++oo++++++++++os. 
 /s˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖os`
 :s˖˖Hello,˖Pythonario˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖os
 :s˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖os
 'o˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖oo
 .os˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖Process˖Peach˖˖˖˖˖˖˖˖˖oo
 'o˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖oo
  :/+++///::+ooooooo+os+++++s+oooo+oooooooooooo+/`
                        +o++o+`   `````     ```
                        -s+.
                           👸

Try it with:
from wizprint import wprint, fnt
wprint("Hello, Pythonario", signed="Process Peach", wiz="p", background=Y, foreground=R)
All options:
wprint(message="", background=black, foreground=B, bgchar='˖', signed="", wiz="w")

import wizprint.fnt for more font coloring options.

More info on fnt:
    Format console: 
    Colors: # For Blue use B
    (P)urple, (B)lue, (G)reen, (Y)ellow, (R)ed.
    Properties: # For bold use b
    (b)old, (u)nderline, (i)talic, (c)lear
    Example: f"{fnt.opt['B']}Blue {fnt.opt['c']}I am. {fnt.opt['i']}Roses {fnt.opt['c']}{fnt.opt['b']}are {fnt.opt['R']}Red{fnt.opt['c']}"
                Blue /            Clear /           Italic /             Clear /        Bold /              Red /           Clear /

You can find Emoji's in fnt.emojis, I've included a few:
🧙, 👸, 👵, 👴, 🎅, 👮, 🕵, 👩, 👨, 👩, 🦸, 🧚.
"""
class fnt: # Font formatting
    """
Format console: 
Colors: # For Blue use fnt.opt['B']
(P)urple, (B)lue, (G)reen, (Y)ellow, (R)ed.
Properties: # For bold use fnt.opt['b']
(b)old, (u)nderline, (i)talic, (c)lear
Example: f"{fnt.opt['B']}Blue {fnt.opt['c']}I am. {fnt.opt['i']}Roses {fnt.opt['c']}{fnt.opt['b']}are {fnt.opt['R']}Red{fnt.opt['c']}"
            Blue /     Clear /     Italic /      Clear / Bold /      Red /   Clear /

You can find Emoji's in fnt.emojis, I've included a few:
"w": "🧙", "p": "👸", "m": "👵", "k": "👴" 
"x": "🎅", "c": "👮", "d": "🕵", "f": "👩" 
"a": "👨", "b": "👩", "s": "🦸", "t": "🧚"
"""
    opt = {
        "T" : "\033[96m", # Teal
        "P" : "\033[95m", # Purple
        "B" : "\033[94m", # Blue
        "Y" : "\033[93m", # Yellow
        "G" : "\033[92m", # Green
        "R" : "\033[91m", # Red
        "hb": "\033[40m", # Highlight black
        "hR": "\033[41m", # Highlight Red
        "hG": "\033[42m", # Highlight Green
        "hY": "\033[43m", # Highlight Yellow
        "hB": "\033[44m", # Highlight Blue
        "hP": "\033[45m", # Highlight Purple
        "hT": "\033[46m", # Highlight Teal
        "hw": "\033[47m", # Highlight white
        "wh": "\033[97m", # White
        "bl" : "\033[90m", # Grey/Black
        "c" : "\033[0m", # Clear formatting
        "b" : "\033[1m", # *Bold*
        "t" : "\033[2m", # thin
        "i" : "\033[3m", # /Italic/
        "u" : "\033[4m", # _Underline_
        "h" : "\033[7m", # Highlighted text
        "d" : "\033[8m", # Delete text (It's there but same color as bg(?))
    }
    emojis = {
        "w": "🧙",
        "p": "👸",
        "m": "👵", 
        "k": "👴",
        "x": "🎅",
        "c": "👮",
        "d": "🕵",
        "f": "👩",
        "a": "👨",
        "b": "👩",
        "s": "🦸",
        "t": "🧚",
    }

def wprint(message="", background="bl", foreground="B", bgchar='˖', signed="", wiz="w", fghighlight="", bghighlight=""):
    """
wprint; A Small Gimmick that makes printing tasks to console just a bit more fun by introducing a Wizard that will tell you your customized message in a bubble

wprint("Hello, world!") 

 .://+///:-`   .://+++oo+++++//:-.`-:://////::-
 s+++++++++oo+oo+++++++++++++++++oo+++++++++++os. 
 'o˖˖Hello,˖world!˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖oo
  :/+++///::+ooooooo+os+++++s+oooo+oooooooooooo+/`
                        +o++o+`   `````     ```
                        -s+.
                           🧙

Standard messages show a small bubble, you can expand this however by adding a signature with the option signed="Pythonuigi"
wprint("Hello, Pythonario", signed="Process Peach", wiz="p")

  .://+///:-`  .://+++oo++++//:-.`-:://////::-
   s+++++++++oo+oo++++++++++++++++oo++++++++++os. 
 /s˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖os`
 :s˖˖Hello,˖Pythonario˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖os
 :s˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖os
 'o˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖oo
 .os˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖Process˖Peach˖˖˖˖˖˖˖˖˖oo
 'o˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖oo
  :/+++///::+ooooooo+os+++++s+oooo+oooooooooooo+/`
                        +o++o+`   `````     ```
                        -s+.
                           👸

Try it with:
from wizprint import wprint, fnt
wprint("Hello, Pythonario", signed="Process Peach", wiz="p", background=fnt.Y, foreground=fnt.R)
All options:
wprint(message="", background=fnt.black, foreground=fnt.B, bgchar='˖', signed="", wiz="w")
# wprint(message="Hi Justin, the time is 16:20:420", signed="January the fucking 1st, 2020")
import wizprint.fnt for more font coloring options.
    """
    if message == "":
        message = "Process Toadstool has completed her task and may now continue her journey."
        signed = "Process Peach"
    if message != "":
        message = message
        if signed != "":
            siglen = len(signed)
            msglen = 42 
            if len(signed) >= (msglen -3):
                msglen = 2*(msglen -3)
            start = (msglen - siglen) - 3
            if msglen > 42:
                start = 3
            message += "\n\n\n" # Add some space for the signature to take place
            signed = f"{' ' * start}{signed}."
            message += f"{signed}\n"
    # Foreground Selector    
    try:
        if foreground != "":
            foreground = fnt.opt.get(str(foreground[0:2])) # Try to get a suggested letter
    except:
        pass
    if foreground == None:
        foreground = fnt.opt.get("B") # Set to Blue if not found
    # Background Selector    
    try:
        if background != "":
            background = fnt.opt.get(str(background[0:2])) # Try to get a suggested letter
    except:
        pass
    if background == None:
        background = fnt.opt.get("bl") # Set to black if not found
    # Emoji Selector
    try:
        if wiz != "":
            wiz = fnt.emojis.get(str(wiz[0])) # Try to get a suggested letter
    except:
        pass
    if wiz == None:
        wiz = fnt.emojis.get("w") # Get The Wizard if not found
    bgchar = bgchar[0:1:1]
    try:
        if fghighlight != "":
            fghighlight = fnt.opt.get(str(fghighlight[0:2])) # Try to get a suggested letter
    except:
        pass
    if fghighlight == None:
        fghighlight = fnt.opt.get("") # Set to Blue if not found
    try:
        if bghighligh != "":
            bghighlight = fnt.opt.get(str(bghighlight[0:2])) # Try to get a suggested letter
    except:
        pass
    if bghighlight == None:
        bghighlight = fnt.opt.get("") # Set to Blue if not found
    # Format Message
    header = f"""
    {fnt.opt['bl']}.://+///:-` .://+++oo++++//:-.`-:://////::-{fnt.opt['c']}   
   {fnt.opt['bl']}s+++++++++oo+oo++++++++++++++++oo++++++++++os.{fnt.opt['c']} """ 
    bubble = [f" {fnt.opt['bl']}.o{fnt.opt['c']}--++++++++++++++++++++++++++++++++++++++++--{fnt.opt['bl']}y`{fnt.opt['c']}",
    f" {fnt.opt['bl']}.os{fnt.opt['c']}-++++++++++++++++++++++++++++++++++++++++--{fnt.opt['bl']}oo{fnt.opt['c']}",
    f" {fnt.opt['bl']}:s{fnt.opt['c']}--++++++++++++++++++++++++++++++++++++++++--{fnt.opt['bl']}os{fnt.opt['c']}",
    f" {fnt.opt['bl']}'o{fnt.opt['c']}--++++++++++++++++++++++++++++++++++++++++--{fnt.opt['bl']}oo{fnt.opt['c']}",
    f" {fnt.opt['bl']}/s{fnt.opt['c']}--++++++++++++++++++++++++++++++++++++++++--{fnt.opt['bl']}os`{fnt.opt['c']}",
    f"  {fnt.opt['bl']}os{fnt.opt['c']}-++++++++++++++++++++++++++++++++++++++++--{fnt.opt['bl']}so.{fnt.opt['c']}",
    f"  {fnt.opt['bl']}/s{fnt.opt['c']}-++++++++++++++++++++++++++++++++++++++++-{fnt.opt['bl']}oo{fnt.opt['c']}",]
    footer = f"""  {fnt.opt['bl']}:/+++///::+ooooooo+os+++++s+oooo+oooooooooooo+/`
         ````````     +o++o+`   `````     ```     
                        -s+.{fnt.opt['c']}  
                           {wiz}"""

    messages = str(message).replace("\t", "    ").replace("\b","").split("\n")
    newMsg = []
    bubbleLen = 40
    for msg in messages:
        while len(msg) > bubbleLen:
            msg1 = msg[:bubbleLen]
            newMsg.append(msg1)
            msg = msg[bubbleLen:]
        newMsg.append(msg)

    finalMsg = []
    if signed != "":
        finalMsg.append(bubble[(random.randint(0,6))])
    for msg in newMsg:
        selectBubble = bubble[(random.randint(0,6))]
        for i in msg:
            if i != " ":
                selectBubble = str(selectBubble.replace('+',  f"{fghighlight}{foreground}{fnt.opt['b']}{i}{fnt.opt['c']}", 1))
            else:
                selectBubble = str(selectBubble.replace('+',  "-", 1))
        selectBubble = str(selectBubble).replace('+', '-')
        finalMsg.append(selectBubble)

    userMessage = ""
    for line in finalMsg:
        userMessage += "\n"
        for i in line:
            userMessage += i
    
    userMessage = userMessage.replace('\n', '', 1)
    userMessage = userMessage.replace("-", f"{bghighlight}{background}{bgchar}{fnt.opt['c']}").replace("+", f"{background}{bgchar}{fnt.opt['c']}")
    output = ""
    for line in header, userMessage, footer:
        output += "\n"
        for i in line:
            output += i
    output += "\n"

    output = output # .replace("-", f"{background}ʾ{fnt.opt['c']}").replace("+", f"{background}ʾ{fnt.opt['c']}")
    print(output)