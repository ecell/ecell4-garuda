import glob
import re

import http.client

conn = http.client.HTTPConnection('rest.kegg.jp')

for i in glob.glob("./*.txt"):
    content = open(i).read()
    kegg_org_codes = re.findall('[a-x]{3}', content)
    for orgcode in kegg_org_codes:
        conn.request("GET", "/list/pathway/" + orgcode)
        response = conn.getresponse()
        if response.status == 200:
            for i in response.readlines():
                pathid = i.decode('utf-8').split("\t")[0]
                pathid = pathid.split(":")[1]
                print("Downloading " + pathid)
                newconn = http.client.HTTPConnection('rest.kegg.jp')
                newconn.request("GET", "/get/" + pathid + "/kgml")
                re = newconn.getresponse()
                handle = open("..\\Output\\"+pathid+".xml", "w")
                handle.write(re.read().decode('utf-8'))
                handle.close()
                print("finishded downloading for organism " + orgcode)
        else:
            print("Your organism code is not in KEGG")