# -*- coding: utf-8 -*-
from wizprint import wprint, fnt
import sys, getopt

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    message = ''
    background= "black"
    foreground= "B"
    bgchar= '˖'
    signed= ""
    wiz= "w"
    helpmsg = f"""{fnt.opt['b']}wprint {fnt.opt['G']}-m "Message"{fnt.opt['c']} {fnt.opt['R']}-b R {fnt.opt['B']}-f B {fnt.opt['c']}{fnt.opt['Y']}-s "Process Peach" {fnt.opt['B']}-c "x" {fnt.opt['c']}-w "p"{fnt.opt['c']}
{fnt.opt['G']}-m --message     {fnt.opt['R']}STRING             {fnt.opt['B']}# "Message to be printed"{fnt.opt['c']}
{fnt.opt['G']}-b --background  {fnt.opt['R']}SINGLE LETTER      {fnt.opt['B']}# Background Color *See Colors below{fnt.opt['c']}
{fnt.opt['G']}-f --foreground  {fnt.opt['R']}SINGLE LETTER      {fnt.opt['B']}# Foreground Color *See Colors below{fnt.opt['c']}
{fnt.opt['G']}-c --bgchar      {fnt.opt['R']}SINGLE CHARACTER   {fnt.opt['B']}# Character to fill background spaces{fnt.opt['c']}
{fnt.opt['G']}-s --signed      {fnt.opt['R']}STRING             {fnt.opt['B']}# "Process Peach" Shows the name as a signature, also makes the bubble bigger.{fnt.opt['c']}
{fnt.opt['G']}-w --wiz         {fnt.opt['R']}SINGLE LETTER      {fnt.opt['B']}# Chooses from a set of emoji's build-in current options:
            "w": "🧙", "p": "👸", "m": "👵", "k": "👴" 
            "x": "🎅", "c": "👮", "d": "🕵", "f": "👩" 
            "a": "👨", "b": "👩", "s": "🦸", "t": "🧚"{fnt.opt['c']}

{fnt.opt['G']}Formatting -b -f
{fnt.opt['B']}Colors: # For Blue use B
{fnt.opt['P']}(P)urple{fnt.opt['c']}, {fnt.opt['B']}(B)lue{fnt.opt['c']}, {fnt.opt['G']}(G)reen{fnt.opt['c']}, {fnt.opt['Y']}(Y)ellow{fnt.opt['c']}, {fnt.opt['R']}(R)ed{fnt.opt['c']}.
Properties: # For bold use b
{fnt.opt['b']}(b)old{fnt.opt['c']}, {fnt.opt['u']}(u)nderline{fnt.opt['c']}, {fnt.opt['i']}(i)talic{fnt.opt['c']}, {fnt.opt['c']}(c)lear
"""
    try:
       opts, args = getopt.getopt(argv,"hm:b:f:c:s:w",["message=","background=","foreground=", "bgchar=", "signed=", "wiz="])
    except getopt.GetoptError:
       print(helpmsg)
       sys.exit(2)
    for opt, arg in opts:
        if len(args) == 1:
            message = args[0]
        if opt == '-h':
            print(helpmsg)
            sys.exit(420)
        elif opt in ("-m", "--message"):
            message = arg
        elif opt in ("-b", "--background"):
            background = arg
        elif opt in ("-f", "--foreground"):
            foreground = arg
        elif opt in ("-c", "--bgchar"):
            bgchar = arg
        elif opt in ("-s", "--signed"):
            signed = arg
        elif opt in ("-w", "--wiz"):
            wiz = arg
         

    wprint(message=message, background=background, foreground=foreground, bgchar=bgchar, signed=signed, wiz=wiz)

if __name__ == "__main__":
   main()