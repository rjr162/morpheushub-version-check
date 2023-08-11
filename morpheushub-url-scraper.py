  GNU nano 6.2                                                                                      site-scraper.py                                                                                                
#!/usr/bin/python3

from bs4 import BeautifulSoup
import re
import requests

## VAR VALUES TO BE SET
username = "<your morpheushub.com username>"
password = "<your morpheushub.com password"
morphversion = "<morphehus major.minor version to check, such as 6.0.>"

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

s = requests.Session()

URL = "https://morpheushub.com/login/authenticate"
data = {
        "username":username,
        "password":password
       }

page = s.post(URL, data=data)


URL = "https://morpheushub.com/download"
page = s.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
versions = soup.find("select", {"id": "downloadVersion"}).find_all("option", recursive=False)
for e in versions:
    if e.contents[0].startswith(morphversion):
        URL = "https://morpheushub.com/download/article?branchId=1&versionId=" + e['value']
        page = s.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        pattern = re.compile(r'%s' % (e.contents[0]))
        results = soup.find_all(text=pattern)
        for e in results:
            if ("downloads.morpheusdata.com/files/morpheus-appliance_" in e or "downloads.morpheusdata.com/files/morpheus-appliance-supplemental_" in e ) \
            and e.endswith(".deb"):
                print(e)

