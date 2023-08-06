from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from hashlib import sha1
def cachecheck(fun):
	def mod(*args,**kwargs):
		cname = sha1((str(args)+str(kwargs)).encode()).hexdigest()+".cache"
		try:
			text = open(cname,encoding='utf-8').read()
		except Exception:
			text = fun(*args,**kwargs)
			open(cname,"w",encoding='utf-8').write(text)
		return text
	return mod
def cleaner(regrex,text):
	return re.sub(re.compile(regrex),"",text)
@cachecheck
def reader(url):
	return urlopen(url).read().decode("utf-8")
def url2text(url,tag=None,regrex=None):
	soup = BeautifulSoup(reader(url),features="lxml")
	if tag!=None:
		text = ""
		for i in soup.find_all(tag):
			text+=i.text+"\n"#text in tag
	else:
		for script in soup(['style', 'script', 'head', 'title', 'meta', '[document]']):
			script.extract()    # remove unwanted tags
		text = soup.get_text()#extract text
					#Remove spaces, multi-headlines into a line, remove blank lines
	text= '\n'.join(chnk for chnk in (phrase.strip() for line in (line.strip() for line in text.splitlines()) for phrase in line.split("  ")) if chnk)
	if regrex!=None:
		return cleaner(regrex,text)
	else: 
		return text