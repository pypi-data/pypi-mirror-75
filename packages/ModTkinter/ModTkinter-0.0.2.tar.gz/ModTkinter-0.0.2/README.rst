'''
Tkinter Package for password bindings and configuring place holders

This is a package to create password bindings and configuring place holders
With this package, you will be able to create placeholding fields, password systems and others....

Installation

-pip install DamPch

The Use

When Using this function make sure to import tkinter  in this format
-import tkinter
-from tkinter import *

-import DamPch
-from DamPch import*

(OR)

-import DamPch
-from DamPch import PCH


Functions Supported

To Use This Package, Instantiate a class object
...
Here We will just be using PCH, which is the class itself

1)
PCH.dampch(root,  placeholder,kbind, bfg, afg, afont, bfont)

Where root is the name of your "tkinter-Widget"
While other fields can be left unfilled since there are default values

kbind- This is if you want to bind your widget with "<Key>".
Because the module itself binds the widget with "<Key>" you need to fill the field so that both functions can be carried out at the same
time of being binded.

bfg= placeholder's foreground
afg= fg foreground

afont= placeholder's font
bfont= fg font

Wigets Supported-

1> Entry
2> Text
3> Listbox


eg. PCH.dampch(search, "Search" )...

2)
PCH.AddSuggestion(root, route, op ,pph, xx, yy, cfg, cfont, cbg)

and PCH.AddSugCustom(root, route, op ,pph, xx, yy, cfg, cfont, cbg, listbg, listfg)# This one can even customize the suggestions

This route here is the Tk window, the name of the top level that user defined as Tk()

root is as usual, the determined widget

op- is the Options
You will pass it as a list or iterable

xx- the x coordinate you want to put the suggestion box
yy- the y coordinate you want to put the suggestion box
With These two you can adjust the position as compatible as possible with the widget.

cfg= widget's foreground
cfont= widget's background

Wigets Supported-

1> Entry

eg. PCH.AddSuggestion(search, tkroot ,['tomatoes','onions'],'Search Meals Ingridients', 180, 221)...



3)
PCH.AuthName(root,  placeholder, bfg, afg, afont, bfont)


This is a field where you can add placeholders like emails, gmail, yahoo acc, '.com'

When input is not in satisfied format it will automatically change the format

Say- input: Mrblahblah

Then It will automatically becomes Mrblahblah@gmail.com if placeholder was gmail.com

The terms are the same so that they will not be described again

>>>Wigets Supported-

1> Entry

eg. PCH.AuthName(emails,"gmail.com")


4)
PCH.dampsw(root,  placeholder, bfg, afg, afont, bfont)

This is a function that could configure your Entry Widget into 

The format is the same as the others.

Wigets Supported-

1> Entry

eg. PCH.dampsw(passwd,"password here")

5)ShowPassWord(widget)
return password

6)DelPassWord(widget)
return blank widget


The Great Purpose

The purpose of this package is to allow most GUI users to run as up-to-date app(GUIs) as possible. The great usage of sensitive placeholders has
shape the century's core and web applications.

As you can see in most of the web developement area,s placeholders make work a lot easier
Instead of presenting the required fields with Labels, technology has taught us to use placeholders.
But unfortunately for database and Desktop app tkinter GUI framework presents still have no options for placeholders.
Here You will get a chance to build a Desktop Application just like the very same graphics of the web.

With DamPch you just have to write a line of code and will even have a chance to change the colors and fonts of the fields and also bind with
other functions

You Will have to write exactly three lines to create a whole password-access app, two of which Widget Presentation and position which are not
DamPchic but Pythonic.

With Hope Users will find satisfaction !!!!!!



END_OF_README


'''





