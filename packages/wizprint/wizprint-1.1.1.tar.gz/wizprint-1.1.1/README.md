# 🧙wizprint 
## A Small Gimmick that makes printing tasks to console just a bit more fun by introducing a Wizard that will tell your customized message in a bubble, with colors, emoji's and memes.
## Wanna try it first? Try it in a repl.it: https://repl.it/@NamasteJasutin/PlasticAssuredLines

### How to install:
Download from pip:
```
python3 -m pip install wizprint
```

### How to use:
```
# -*- coding: utf-8 -*-
from wizprint import wprint
wprint("Hello, world!") 
```
**This will ouput something like this:**
```
 .://+///:-`   .://+++oo+++++//:-.`-:://////::-
 s+++++++++oo+oo+++++++++++++++++oo+++++++++++os. 
 'o˖˖Hello,˖world!˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖˖oo
  :/+++///::+ooooooo+os+++++s+oooo+oooooooooooo+/`
                        +o++o+`   `````     ```
                        -s+.
                           🧙
```
Standard messages show a small bubble, you can expand this however by adding a signature with the option signed, for example:
```
wprint("Hello, Pythonario", signed="Process Peach", wiz="p")
```
**... will look like this:**
```
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
```

### I want to try this, what do I need to do?
```
python3 -m pip install wizprint

python3
from wizprint import wprint, fnt
wprint("Hello, Pythonario", signed="Process Peach", wiz="p", background=fnt.Y, foreground=fnt.R)
```
*All options:
wprint(message="", background=fnt.black, foreground=fnt.B, bgchar='˖', signed="", wiz="w")

For more font coloring options, use:
```
from wizprint import fnt
```
More info on fnt:
Format console: 
Colors: # For Blue use fnt.B
(P)urple, (B)lue, (G)reen, (Y)ellow, (R)ed.
Properties: # For bold use fnt.b
(b)old, (u)nderline, (i)talic, (c)lear
Example: f"{fnt.B}Blue {fnt.c}I am. {fnt.i}Roses {fnt.c}{fnt.b}are {fnt.R}Red{fnt.c}"
            Blue /     Clear /     Italic /      Clear / Bold /      Red /   Clear /

You can find Emoji's in 
```
fnt.emojis
```
I've included a few:
🧙, 👸, 👵, 👴, 🎅, 👮, 🕵, 👩, 👨, 👩, 🦸, 🧚.


Try loading as module ;)
```
python3 -m wizprint
```

If your Python3 is in PATH, you can now run:
```
wprint -m "  $(date)" -s "$USERNAME"
```
For Windows:
```
python -m pip install wizprint
wprint -m "  $(date)" -s "$ENV:USERNAME"
```
This can be handy when running scripts to let messages stand out, but not take up too much space in the console.

More help on wprint, open a terninal and type:
```
wprint -h
```
