import os
import glob
import subprocess
import re
import smtplib

import shutil

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#######################################################################################################################
#######################################################################################################################

def doopRemove(seq):
    ret = []
    for i in seq:
        if i not in ret:
            ret.append(i)
    return ret

def toString(seq):
    for i in seq:
        return i

def newline(seq):
    for i in seq:
        newseq = seq(i) + '\n'
        return newseq

def idopen(seq):
    for i in seq:
        return seq.insert(0, "<id>")

# [MAKE FILES] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [MAKE FILES] #
newFile1 = open('/home/alec/csc344/a1/main.c', 'r')
newFile2 = open('/home/alec/csc344/a2/CSC344_02.clj', 'r')
newFile3 = open('/home/alec/csc344/a3/Main.scala', 'r')
newFile4 = open('/home/alec/csc344/a4/prolog.pl', 'r')
newFile5 = open('/home/alec/csc344/a5/main.py', 'r')

# [POPULATE FILES] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [POPULATE FILES] #
contents1 = newFile1.read()
newFile1.close()
contents2 = newFile2.read()
newFile2.close()
contents3 = newFile3.read()
newFile3.close()
contents4 = newFile4.read()
newFile4.close()
contents5 = newFile5.read()
newFile5.close()

# [C REGEX] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [C REGEX] #
cregex = []
cfixed = []
# find functions:
cfuncs = re.findall("(int|char|void|struct) [a-z]\w+", contents1)
for i in cfuncs:
    cregex.append(i)
# find vars & pointers
cvptrs = re.findall("([a-z]\w+ =)", contents1)
for j in cvptrs:
    cregex.append(j[0:len(j)-2])
# remove duplicates
cfixed = doopRemove(cregex)

# [CLOJURE REGEX] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [CLOJURE REGEX] #

cljregex = []
cljfixed = []
# find functions:
cljfuncs = re.findall("(\(defn [a-z].* \[)", contents2)
for i in cljfuncs:
    cljregex.append(i[5:len(i)-2])
# remove duplicates
cljfixed = doopRemove(cljregex)
cljstring = ''
for i in cljfixed:
    cljstring = cljstring + i + '\n'

# [SCALA REGEX] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [SCALA REGEX] #

scalaregex = []
scalafixed = []
# find functions & case classes:
scalafuncs = re.findall("((def)|(class) \w+)", contents3)
for i in scalafuncs:
    j = i[0]
    scalaregex.append(j)
# find vars and vals:
scalavars = re.findall("(((val)|(var)) \w+)", contents3)
for i in scalavars:
    j = i[0]
    scalaregex.append(j)
# remove duplicates
scalafixed = doopRemove(scalaregex)
scalastring = ''
for i in scalafixed:
    scalastring = scalastring + i + '\n'

# [PROLOG REGEX] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [PROLOG REGEX] #

plregex = []
plfixed = []
#find capital-letter identifiers:
plvars = re.findall("([A-Z]\w+)", contents4)
for i in plvars:
    plregex.append(i)
#remove duplicates
plfixed = doopRemove(plregex)
plstring = ''
for i in plfixed:
    plstring = plstring + i + '\n'

# [PYTHON REGEX] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [PYTHON REGEX] #

pyregex = []
pyfixed = []
#find python vars & fns
pyvars = re.findall("((def \w+)|([a-z]\w+ =))", contents5)
for i in pyvars:
    j = i[0]
    pyregex.append(j[:len(j)-2])
pyfixed = doopRemove(pyregex)
pystring = ''
for i in pyfixed:
    pystring = str(pystring) + str(i) + '\n'

# [BUILD HTML PAGE] * * * * * * ** * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [BUILD HTML PAGE] #
f = open('index.html', 'w')

index = """<!doctype html>
<html>
  <body>
  <br>
    <a href = "a1/c.xml"> a1 -- C </a>
  <br>
  <br>
    <a href = "a2/clojure.xml"> a2 -- Clojure </a>
  <br>
  <br>
    <a href = "a3/scala.xml" >a3 -- Scala</a>
  <br>
  <br>
    <a href = "a4/prolog.xml"> a4 -- Prolog </a>
  <br>
  <br>
    <a href = "a5/python.xml"> a -- Python </a>
  </body>
</html>"""

f.write(index)
f.close()
os.system("mv index.html ../../csc344")

# * [BUILD XML FILES] * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# [C XML] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [C XML] #
# create c.xml
f = open('c.xml','w')
# get word count
cWordcount = sum(1 for x in open('/home/alec/csc344/a1/main.c'))
# encode xml
cxml1 = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="c.xsl"?>
<answer>
  <wc>
"""
cxml2 = """</wc>
"""
cxml3 = """</answer>
"""
# create c.xsl
g = open('c.xsl','w')
cxsl = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html> 
<body>
  <h2>C -- answer</h2>
  <a href="main.c">main.c</a>
  <table border="2">
    <tr bgcolor="#1c9dad">
      <th style="text-align:center">WC -- Identifiers</th>
    </tr>
    <xsl:for-each select ="answer">
    <tr>
      <tr><xsl:value-of select="wc"/></tr>
    </tr>
    </xsl:for-each>
    <xsl:for-each select="answer/id">
    <tr>
      <td><xsl:value-of select="current()"/></td>
    </tr>
    </xsl:for-each>
  </table>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
"""
# concatenation for xslt display
cbigboi1 = cxml1 + str(cWordcount) + cxml2
cbigboi2 = ''
cbigboi3 = cxml3
f.write(cbigboi1)
for i in cfixed:
    cbigboi2 = '  <id>' + i + '</id>' + '\n'
    f.write(cbigboi2)
f.write(cbigboi3)
g.write(cxsl)
f.close()
g.close()
# directory issue fixes
os.chdir("/home/alec/PycharmProjects/CSC344_micro05/venv")
os.system("mv c.xml c.xsl ../../../csc344/a1")

# [CLOJURE XML] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [CLOJURE XML] #

# create clj.xml
f = open('clj.xml', 'w')
# get word count
cljWordcount = sum(1 for x in open('/home/alec/csc344/a2/CSC344_02.clj'))
# encode xml
cljxml1 = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="clj.xsl"?>
<answer>
  <wc>
"""
cljxml2 = """</wc>
"""
cljxml3 = """</answer> 
"""
# create clj.xsl
g = open('clj.xsl', 'w')
cljxsl = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html> 
<body>
  <h2>Clojure -- answer</h2>
  <a href="CSC344_02.clj">CSC344_02.clj</a>
  <table border="2">
    <tr bgcolor="#1c9dad">
      <th style="text-align:center">WC -- Identifiers</th>
    </tr>
    <xsl:for-each select ="answer">
    <tr>
      <tr><xsl:value-of select="wc"/></tr>
    </tr>
    </xsl:for-each>
    <xsl:for-each select="answer/id">
    <tr>
      <td><xsl:value-of select="current()"/></td>
    </tr>
    </xsl:for-each>
  </table>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
"""
# concatenation for xslt display
cljbigboi1 = cljxml1 + str(cljWordcount) + cljxml2
cljbigboi2 = ''
cljbigboi3 = cljxml3
f.write(cljbigboi1)
for i in cljfixed:
    cljbigboi2 = '  <id>' + i + '</id>' + '\n'
    f.write(cljbigboi2)
f.write(cljbigboi3)
g.write(cljxsl)
f.close()
g.close()
# directory issue fixes
os.chdir("/home/alec/PycharmProjects/CSC344_micro05/venv")
os.system("mv clj.xml clj.xsl ../../../csc344/a2")

# [SCALA XML] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [SCALA XML] #

# create scala.xml
f = open('scala.xml', 'w')
# get word count
scalaWordcount = sum(1 for x in open('/home/alec/csc344/a3/Main.scala'))
# encode xml
scalaxml1 = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="scala.xsl"?>
<answer>
  <wc>
"""
scalaxml2 = """</wc>
"""
scalaxml3 = """</answer> 
"""
# create scala.xsl
g = open('scala.xsl', 'w')
scalaxsl = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html> 
<body>
  <h2>Scala -- answer</h2>
  <a href="Main.scala">Main.scala</a>
  <table border="2">
    <tr bgcolor="#1c9dad">
      <th style="text-align:center">WC -- Identifiers</th>
    </tr>
    <xsl:for-each select ="answer">
    <tr>
      <tr><xsl:value-of select="wc"/></tr>
    </tr>
    </xsl:for-each>
    <xsl:for-each select="answer/id">
    <tr>
      <td><xsl:value-of select="current()"/></td>
    </tr>
    </xsl:for-each>
  </table>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
"""
# concatenation for xslt display
scalabigboi1 = scalaxml1 + str(scalaWordcount) + scalaxml2
scalabigboi2 = ''
scalabigboi3 = scalaxml3
f.write(scalabigboi1)
for i in scalafixed:
    scalabigboi2 = '  <id>' + i + '</id>' + '\n'
    f.write(scalabigboi2)
f.write(scalabigboi3)
g.write(scalaxsl)
f.close()
g.close()
# directory issue fixes
os.chdir("/home/alec/PycharmProjects/CSC344_micro05/venv")
os.system("mv scala.xml scala.xsl ../../../csc344/a3")

# [PROLOG XML] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [PROLOG XML] #

# create pl.xml
f = open('pl.xml', 'w')
# get word count
plWordcount = sum(1 for x in open('/home/alec/csc344/a4/prolog.pl'))
# encode xml
plxml1 = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="pl.xsl"?>
<answer>
  <wc>
"""
plxml2 = """</wc>
"""
plxml3 = """</answer>
"""
# create pl.xsl
g = open('pl.xsl', 'w')
plxsl = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html> 
<body>
  <h2>Prolog -- answer</h2>
  <a href="prolog.pl">prolog.pl</a>
  <table border="2">
    <tr bgcolor="#1c9dad">
      <th style="text-align:center">WC -- Identifiers</th>
    </tr>
    <xsl:for-each select ="answer">
    <tr>
      <tr><xsl:value-of select="wc"/></tr>
    </tr>
    </xsl:for-each>
    <xsl:for-each select="answer/id">
    <tr>
      <td><xsl:value-of select="current()"/></td>
    </tr>
    </xsl:for-each>
  </table>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
"""
# concatenation for xslt display
plbigboi1 = plxml1 + str(plWordcount) + plxml2
plbigboi2 = ''
plbigboi3 = plxml3
f.write(plbigboi1)
for i in plfixed:
    plbigboi2 = '  <id>' + i + '</id>' + '\n'
    f.write(plbigboi2)
f.write(plbigboi3)
g.write(plxsl)
f.close()
g.close()
# directory issue fixes
os.chdir("/home/alec/PycharmProjects/CSC344_micro05/venv")
os.system("mv pl.xml pl.xsl ../../../csc344/a4")

# [PYTHON XML] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [PYTHON XML] #

# create py.xml
f = open('py.xml', 'w')
# get word count
pyWordcount = sum(1 for x in open('/home/alec/csc344/a5/main.py'))
# encode xml
pyxml1 = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="py.xsl"?>
<answer>
  <wc>
"""
pyxml2 = """</wc>
"""
pyxml3 = """</answer> 
"""
# create py.xsl
g = open('py.xsl', 'w')
pyxsl = """<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html> 
<body>
  <h2>Python -- answer</h2>
  <a href="main.py">main.py</a>
  <table border="2">
    <tr bgcolor="#1c9dad">
      <th style="text-align:center">WC -- Identifiers</th>
    </tr>
    <xsl:for-each select ="answer">
    <tr>
      <tr><xsl:value-of select="wc"/></tr>
    </tr>
    </xsl:for-each>
    <xsl:for-each select="answer/id">
    <tr>
      <td><xsl:value-of select="current()"/></td>
    </tr>
    </xsl:for-each>
  </table>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
"""
# concatenation for xslt display
pybigboi1 = pyxml1 + str(pyWordcount) + pyxml2
pybigboi2 = ''
pybigboi3 = pyxml3
f.write(pybigboi1)
for i in pyfixed:
    pybigboi2 = '  <id>' + i + '</id>' + '\n'
    f.write(pybigboi2)
f.write(pybigboi3)
g.write(pyxsl)
f.close()
g.close()
# directory issue fixes
os.chdir("/home/alec/PycharmProjects/CSC344_micro05/venv")
os.system("mv py.xml py.xsl ../../../csc344/a5")

# [ZIP] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [ZIP] #

os.chdir("../../..")
os.system('zip -r 344pyzip.zip csc344')
os.system('mv 344pyzip.zip 344zip')

# [EMAIL] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [EMAIL] #

sender = "abg523@gmail.com"
receiver = "daniel.schlegel@oswego.edu"

mail = MIMEMultipart()
mail['From'] = sender
mail['To'] = receiver
mail['Subject'] = "CSC344 Assignment 5"
text = "text"

mail.attach(MIMEText(text))

thisFile = "344pyzip.zip"
thatFile = open("/home/alec/344zip/344pyzip.zip", "rb")

app = MIMEBase('application', "octet-stream")
app.set_payload(thatFile.read())
encoders.encode_base64(app)
app.add_header('Content-Disposition', 'attachment; thisFile = %s' % thisFile)

mail.attach(app)

print('password: ')
pswd = input()
get_served = smtplib.SMTP('smtp.gmail.com', 587)
get_served.starttls()
get_served.login(sender, pswd)
get_served.sendmail(sender, receiver, mail.as_string())
get_served.close()

# that's a lot of damage...
# [END] * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * [END] #
