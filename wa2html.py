#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

exportFile = open('index.html', 'w')
msgText = ''
msgFrom = ''
msgTime = ''

# Line Regex
reTimestamp = '([0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+): '
pPict = re.compile(reTimestamp + '(.*): (.*) <‎bijgevoegd>')
pNewMsg = re.compile(reTimestamp + '(.*): (.*)')
pNote = re.compile(reTimestamp + '(.*)')
pMsgLine = re.compile('(.*)')
pAdmin = re.compile('Sander|Rüdiger')

def startExport():
    exportFile.write("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Marieke group</title>
<link rel="stylesheet" type="text/css" href="whatsapp.css">
<link rel="stylesheet" href="magnific-popup.css">
<script src="https://code.jquery.com/jquery-1.12.4.js"></script>
<script src="jquery.magnific-popup.min.js" async></script>
</head>
<body>
<div class="speech-wrapper">
    """)

def finishExport():
    exportFile.write("""
</div>
</body>
<script>
    $(document).ready(function() {
        $('.image-link').magnificPopup({type:'image'});
    });
</script>
</html>""")
    exportFile.close()

def appendMsg(txt):
    global msgText
    msgText = msgText + '<br/>' + txt

def writeBalloon(date, who, msg):
    if pAdmin.match(who):
        alt = ''
    else:
        alt = 'alt'
    exportFile.write("""
        <div class="bubble {3}">
        <div class="txt">
        <p class="name">{1}</p>
        <p class="message">{2}</p>
        <span class="timestamp">{0}</span>
        </div>
        <div class="bubble-arrow {3}"></div>
        </div>
    """.format(date, who, msg, alt))

startExport()
with open('_chat.txt') as chat:
    content = chat.readlines()
for x in content:
    mPict = pPict.match(x)
    mNewMsg = pNewMsg.match(x)
    mNote = pNote.match(x)
    mMsgLine = pMsgLine.match(x)

    if (mPict or mNewMsg) and msgText:
        writeBalloon(msgTime, msgFrom, msgText)

    if mPict:
        msgTime = mNewMsg.group(1)
        msgFrom = mNewMsg.group(2)
        msgText = '<a href="{0}" class="image-link"><img src="{0}" height="25%" width="25%"/></a><br/>'.format(mPict.group(3))
    elif mNewMsg:
        msgTime = mNewMsg.group(1)
        msgFrom = mNewMsg.group(2)
        msgText = mNewMsg.group(3)
    elif mNote:
        print 'Skipped note: ' + x
    elif mMsgLine:
        appendMsg(mMsgLine.group(1))
    else:
        print 'oeps: ' + x
finishExport()
