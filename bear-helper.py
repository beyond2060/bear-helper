# -----------------------------------------------------------------------------
# 🍯 Bear Helper: An easy-to-customize macOS menubar helper for the Bear app
#    Written by James Johnson, June 2024
#    https://www.beyond2060.com/bear-helper/
# -----------------------------------------------------------------------------

import rumps
#rumps.debug_mode(True)
from datetime import datetime
from AppKit import NSPasteboard, NSStringPboardType
import re
import webbrowser
import urllib.parse

# JOURNAL TEMPLATE ------------------------------------------------------------

journal_template = """
## 🌟 Daily highlight
*What one thing can I do today that will make it a great day?*


## ⏰ Schedule
### Morning:

### Afternoon:

### Evening:


## 🤔 Reflection
*What went well today? What can I improve?*


## 📅 Plan for tomorrow
*Top priorities for tomorrow.*


--- 


"""

# PROJECT TEMPLATE ------------------------------------------------------------

project_template = """
## What am I doing?


## Why?


## Results


## Conclusion


---
## Details

"""

# CODE ------------------------------------------------------------------------

today = datetime.today()
formatted_date = today.strftime("%d %B %Y")

class BearHelper(rumps.App):

    # ABOUT -------------------------------------------------------------------

    @rumps.clicked("About Bear Helper")
    def about(self, _):
        webbrowser.open('https://www.beyond2060.com/bear-helper/')

    # NEW JOURNAL ENTRY -------------------------------------------------------
        
    @rumps.clicked("New journal entry")
    def journal(self, _):

        dayOfWeek = today.strftime( "%A\n")

        title = formatted_date
        body  =  dayOfWeek + journal_template
        tags  = "00 📗 journal/%Y/%m"

        newNote(title, body, tags)

    # NEW PROJECT -------------------------------------------------------------

    @rumps.clicked("New project note")
    def project(self, _):

        title = "Project: TITLE" 
        body  =  f"**Date: {formatted_date}**\n" + project_template 
        tags  = "03 💥 projects"

        newNote(title, body, tags)

    # NEW FROM PERPLEXITY -----------------------------------------------------

    @rumps.clicked("New note from Perplexity.ai")
    def perplexity(self, _):
        pb = NSPasteboard.generalPasteboard()
        pbstring = pb.stringForType_(NSStringPboardType)
        
        # Do a regex search and replace on the clipboard contents
        # Replace [NUMBER] with "[^NUMBER]
        body = re.sub(r"\[(\d+)\]", r"[^\1]", pbstring)
        
        # If a line starts with [^NUMBER] then replace it with [^NUMBER]:
        body = re.sub(r"^\[\^(\d+)\]", r"[^\1]:", body, flags=re.MULTILINE)
        body = urllib.parse.quote(f"Date: {formatted_date}\n\n" + body)

        title = "TITLE"
        tags = "perplexity.ai"

        newNote(title, body, tags)

    # -------------------------------------------------------------------------

def newNote(title, body, tags):
    title_encoded = urllib.parse.quote(title)
    body_encoded  = urllib.parse.quote(body)
    tags_encoded  = urllib.parse.quote(tags)

    xcallback = f"bear://x-callback-url/create?title={title_encoded}&text={body_encoded}&tags={tags_encoded}&clipboard=no&open_note=yes&new_window=yes&float=yes&edit=yes"
    webbrowser.open(xcallback)

if __name__ == "__main__":
    BearHelper("🍯").run()