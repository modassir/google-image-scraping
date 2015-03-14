import requests
from lxml import html

#Change the proxy address here...
proxies ={
    "http":"http://10.3.100.207:8080",
    "https":"http://10.3.100.207:8080",
    "ftp":"http://10.3.100.207:8080",
    }

headers={
	"Connection":"keep-alive",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:27.0) Gecko/20100101 Firefox/34.0"
        }


var=raw_input("Please Enter the Search Query for which you want to download 100 images from Google: ")
size=raw_input("Enter l for Large Size Image, m for Medium, i for icon size and n for no preference: ")
var_list=var.split(" ")
var_str='+'.join(var_list)
if (size=="n"):
	url_main="https://www.google.com/search?tbm=isch&q="+var_str
else:
	url_main="https://www.google.com/search?tbm=isch&q="+var_str+"&tbs=isz:"+size
req=requests.get(url_main, proxies = proxies,headers=headers,verify=False)
r_content=req.content
tree=html.fromstring(r_content)
temp_links=tree.xpath('//a[@class="rg_l"]/@href')

print "List of temp links has been compiled in a single list"

for i in xrange(0,100):
	try:
		temp_links_str=temp_links[i]
		split_temp_links=temp_links_str.split("/")
		if (split_temp_links[0]=="https:"):
			url=temp_links[i]
		elif (split_temp_links[0]=="http:"):
			url=temp_links[i]
		else:
			url="https://www.google.com"+temp_links[i]
		req=requests.get(url, proxies = proxies,headers=headers,verify=False)
		req_content=req.content
		tree=html.fromstring(req_content)
		img_links=tree.xpath('//meta[@itemprop="image"]/@content')
		img_links_str=img_links[0]
		temp_img_links=img_links_str.split("/")
		if (temp_img_links[0]=="https:"):
			url2=img_links[0]
		elif (temp_img_links[0]=="http:"):
			url2=img_links[0]
		else:
			url2="https://www.google.com"+img_links[0]
		req2=requests.get(url2, proxies = proxies,headers=headers,verify=False)
		req2_content=req2.content
		string=req2.url
		ext_list=string.split(".")
		ext=ext_list[-1]
		if (len(ext)==3):
			fh=open("Images/"+var+"_"+str(i+1)+"."+ext,"wb+")
			fh.write(req2_content)
			fh.close()
			print "Got Image",i+1,"of 100"
		else:
			print "Skipping file",i+1,"of 100 because it is invalid"
	except:
		print "Encountered an error skipping",i+1,"of 100"
