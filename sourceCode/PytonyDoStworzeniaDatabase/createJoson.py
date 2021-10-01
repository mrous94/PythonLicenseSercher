

#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import re
import requests
import codecs
import os.path
import os
from html.parser import HTMLParser
import json


h = HTMLParser()
licenses = [x for x in os.listdir('.') if '.html' in x]

database = []

for license in licenses:
    with codecs.open(license, 'r', 'utf-8') as myfile:
        data = myfile.read()

    name = [h.unescape(x) for x in re.findall('<code property="spdx:name">(.*?)</code>', data)][0]
    shortname = [h.unescape(x) for x in re.findall('<code property="spdx:licenseId">(.*?)</code>', data)][0]

    result = re.findall('<div property="spdx:licenseText" class="license-text">(.*?)</div>', data, re.MULTILINE | re.DOTALL)
    license = ' '.join(re.sub('<[^<]+?>', '', h.unescape(result[0])).split())


    result = re.findall('<div property="spdx:standardLicenseHeader" class="license-text">(.*?)</div>', data, re.MULTILINE | re.DOTALL)
    header = ' '.join(re.sub('<[^<]+?>', '', h.unescape(result[0])).split())
    if 'There is no standard license header for the license' in header:
        header = ''

    database.append({
        'fullname': name,
        'shortname': shortname,
        'text': license,
        'header': header
    })




print (json.dumps(database))
#file = open("database.josn","w")
#print (json.dumps(database),file = file)
#file.close()