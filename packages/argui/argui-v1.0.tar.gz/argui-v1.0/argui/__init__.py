'''
    This is a importable program for creating a GUI for command line program argument input.
    Copyright (C) 2020 Mason Kuan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    For more information please email: palm.tree6555365@gmail.com
'''

import tkinter as tk
from tkinter import messagebox as msgbox
from tkinter import simpledialog as dialog
import math
##import argparse # Not used, at least not currently
import sys
import os
import time
import subprocess
import shlex
import re

lang = 'en-us'
style_lang = {'en-us':{'default': '',
                       'require': 'required',
                       'integer': 'integer',
                       'double': 'double',
                       'float': 'floating point number',
                       'string': 'string'}}
style_aliases = {'d': 'default',
                 'r': 'require',
                 'int': 'integer',
                 'db': 'double',
                 'f': 'float',
                 'str': 'string',
                 'b':'default',
                 'base':'default'}
style_check = {'default':lambda x:True, # No reqs for the default check
               'require':lambda x:x, # An empty string results in false
               'integer':lambda x:x == '' or x.isdigit(), # All digits = return
               'double':lambda x:x == '' or x.replace('.','',1).isdigit(), # Only 1 decimal point allowed (replace removes one instance of the decimal)
               'float':lambda x:x == '' or '.' in x and x.replace('.','',1).isdigit() and len(x.split('.')[0]) and len(x.split('.')[1]), # Same as double, but requires a decimal
               'string':lambda x:True} # An empty string is still a string
style_error_priority = "require integer double float string default"

class FieldData(object):
    def __init__(self, frame, label, text, style='default', insert_name=False, regex=None):
        self.frame = frame
        self.label = label
        self.text = text
        self.style = style
        self.styles = []
        for s in style.lower().split():
            if s in style_aliases:
                self.styles += [style_aliases[s]]
            else:
                self.styles += [s]
        self.insert_name = insert_name
        self.regex = regex
    def validate(self):
        flagged = False
        flagged_styles = []
        field_input = self.text.get('1.0', 'end-1c')
        field_name = self.label.cget('text')
        for style in self.styles:
            if not style_check[style](field_input):
                flagged = True
                flagged_styles += [style]
        if flagged:
            flagged_string = ""
            for style in style_error_priority.split():
                if style in self.styles:
                    flagged_string += style_lang[lang][style]
                    flagged_string += " "
            startswith_vowel = False
            for vowel in 'aeiou':
                if flagged_string.startswith(vowel):
                    startswith_vowel = True
            if startswith_vowel:
                error_str = "An " + flagged_string
            else:
                error_str = "A " + flagged_string
            error_str += "input"
            msgbox.showerror("Input Validation", "Inputted data for %s did not match input type: %s" % (field_name, error_str))
        if not (self.regex is None):
            if not self.regex.check(field_input):
                flagged = True
                msgbox.showerror("Regex Input Validation", "Inputted data for %s did not match the regex: %s with description: %s" % (field_name, self.regex.expression, self.regex.description))
        return not flagged

class Regex(object):
    def __init__(self, expression, description):
        self.expression = expression
        self.description = description
        self.internal = re.compile(expression)
    def check(self, data):
        return not (self.internal.fullmatch(data) is None)

class Argui(tk.Frame):
    def __init__(self, parent=None, target=None, filename=None):
        if parent is None:
            raise TypeError("Must provide tkinter.Tk() root window, not NoneType")
        super().__init__(parent)
        self.parent = parent
        self.fields = []
        self.mainFrame = tk.Frame(relief=tk.RAISED, borderwidth=1, padx=15, pady=15)
        self.mainFrame.pack(fill=tk.BOTH, expand=True)
        self.initTitle()
        if target is None:
            self.addField('Program Name', style='require')
            self.target = ""
        else:
            self.target = target + " "
        if filename is None:
            self.filenameInput()
            self.filename = ""
        else:
            self.filename = filename
            self.filenameField = None

    def initTitle(self, name="GUI for command line options"):
        self.parent.title(name)
        self.titleWidget = tk.Label(self.mainFrame, text=name, padx=5, pady=5)
        self.titleWidget.pack()
##        self.widget_title = tk.Text(self.mainFrame)
##        self.widget_title.insert(1.0, name)
##        self.widget_title.config(state=tk.DISABLED, width=28, height=1, padx=5, pady=5)
##        self.widget_title.pack()

    def addField(self, argname, style='default', width=28, insert_name=False, regex=None):
        frame = tk.Frame(self.mainFrame, padx=5, pady=5)
        label = tk.Label(frame, text=argname, padx=5, pady=5)
        text = tk.Text(frame, padx=0, pady=0, width=width, height=1, font=('Consolas', 10))
        data = FieldData(frame, label, text, style, insert_name, regex)
        data.frame.pack(fill=tk.BOTH, expand=True)
        data.label.pack(side=tk.LEFT)
        data.text.pack(side=tk.RIGHT)
        self.fields += [data]

    def filenameInput(self):
        frame = tk.Frame(self.mainFrame, padx=5, pady=5)
        label = tk.Label(frame, text='Output Filename', padx=5, pady=5)
        text = tk.Text(frame, padx=0, pady=0, width=28, height=1, font=('Consolas', 10))
        data = FieldData(frame, label, text)
        data.frame.pack(fill=tk.BOTH, expand=True)
        data.label.pack(side=tk.LEFT)
        data.text.pack(side=tk.RIGHT)
        self.filenameField = data

    def finishSetup(self):
        self.bottomFrame = tk.Frame(self.mainFrame, relief=tk.RAISED, borderwidth=0, padx=5, pady=5)
        self.bottomFrame.pack(fill=tk.BOTH, expand=True)
        self.generateButton = tk.Button(self.bottomFrame, text="Generate", command=self.handleButton)
        self.generateButton.pack(padx=5, pady=5)
        self.generateScript = tk.Button(self.bottomFrame, text="Generate Script", command=self.generateScript)
        self.generateScript.pack(padx=5, pady=5)
        self.resultText = tk.Text(self.bottomFrame, state=tk.DISABLED, padx=0, pady=0, height=1, font=('Consolas', 10), bg='black', fg='white')
        self.resultText.pack()
        self.runButton = tk.Button(self.bottomFrame, text="Run", command=self.runCommand)
        self.runButton.pack(padx=5, pady=5)
        self.copyright = tk.Label(self.mainFrame, text="Tool Created By Mason Kuan", padx=0, pady=0, font=('Consolas', 10))
        self.copyright.pack(side=tk.BOTTOM)

    def handleButton(self):
        command = self.target
        for field in self.fields:
            if not field.validate():
                return
            text = str(field.text.get('1.0', 'end-1c')) # Read from line 1 column 0, until the end minus newline char
            if text == "":
                continue
            if field.insert_name:
                command += field.label.cget('text')
                command += " "
            command += "\""
            command += text
            command += "\" "
        self.resultText.config(state=tk.NORMAL)
        self.resultText.delete('1.0', 'end')
        self.resultText.insert('1.0', command)
        self.resultText.config(state=tk.DISABLED)

    def runCommand(self):
        self.handleButton()
        if self.filename is not None:
            fnF = self.filenameField.text.get('1.0','end-1c')
            if fnF == "":
                f = None
            else:
                f = open(fnF, "w")
        else:
            f = open(self.filename, "w")
        subprocess.Popen(shlex.split(self.resultText.get('1.0','end-1c')), stdout=f, stderr=subprocess.STDOUT)

    def generateScript(self):
        self.handleButton()
        if self.filename is not None:
            ofn = self.filenameField.text.get('1.0','end-1c')
            if ofn == "":
                ofn = "output.txt"
                msgbox.showinfo("Output Filename", "Output from the generated script will be piped to output.txt")
        else:
            ofn = self.filename
        filename = dialog.askstring("Script Filename", "Enter the filename for the generated script:")
        if filename is None:
            return # User clicked cancel
        if filename == "":
            filename = "script.sh"
            msgbox.showinfo("Script Filename", "Filename for the generated script will be script.sh")
        with open(filename, "w") as f:
            f.write("#!/bin/bash\n")
            f.write(self.resultText.get('1.0','end-1c'))
            f.write(" > ")
            f.write(ofn)
            f.close()
        msgbox.showinfo("Script Generated", "Your requested script has been generated.")

if __name__ == "__main__":

    root = tk.Tk()
    app = Argui(root)

    app.addField('Basic')
    app.addField('--insert-name', insert_name=True)
    app.addField('Custom Width', width=48)
    app.addField('Required', style='require')
    app.addField('Integer', style='integer')
    app.addField('Double', style='double')
    app.addField('Float', style='float')
    app.addField('String', style='string')
    app.addField('Regex', regex=Regex('^[a-zA-z0-9_]+$','Alphanumeric Input Only'))

    app.finishSetup()

    app.mainloop()
