import nltk
import operator
import sys
import re


class pclassify:
    weights={}
    labels={}

    def __init__(self,fname):
        f=open(fname,'r')
        lline=f.readline().rstrip().split(' ')
	#print lline
        for l in lline:
            val=l.split('\t')
	    #print val
            self.labels[val[0]]=int(val[1])
            self.weights[val[0]]={}
        for l in f:
            param=l.split()
            self.weights[param[0]][param[1]]=float(param[2])
        f.close()
        #print self.labels

    def predict(self,features,fx):
        wi={}
        for l in self.labels:
            wi[l]=0.0
        for feature in fx:
            for l in self.labels:
                if self.weights[l].has_key(feature)==False:
                    continue
                wi[l]+=self.weights[l][feature]*fx[feature]
        zlabel=max(wi.iteritems(), key=operator.itemgetter(1))[0]
        return zlabel
    
    def classify(self,line):
        #fl=open(tfile,'r')
	#fl=sys.stdin
        #for line in fl:
        features=line.split()
        fx={}
        for feature in features:
       		if fx.has_key(feature)==False:
        		fx[feature]=1
        	else:
        		fx[feature]+=1
        zlabel=self.predict(features,fx)
       	return zlabel
        #fl.close()

#pits=pclassify('its.model')
#pyour=pclassify('your.model')
#ptheir=pclassify('their.model')
#pto=pclassify('to.model')
plose=pclassify('lose.model')



def gen_grams(line, org_line):  # lose, loose
	#print line
	mylist=line.split(' ')
	labels=['lose','loose']
	code=0
	bin_tags=[]
	#if mylist[-1]=='\n':
	del mylist[-1]
	n=len(mylist)
	pos=0
	#print mylist
	for i in range(0,n):
		result=''
		pattern1=re.compile("([^a-zA-Z\-]|^)(lose|loose|Lose|Loose)([^a-zA-Z\-]|$)")		
		#if ('lose/' in mylist[i]) or ('Lose/' in mylist[i]):
		if pattern1.search(mylist[i])!=None:
			#print mylist[i]
			if (i-1)>=0:
				wt=mylist[i-1].split('/')	
				result+='lw1:'+wt[0]+' lt1:'+wt[1]
			if (i-2)>=0:
				wt=mylist[i-2].split('/')	
				result+=' lw2:'+wt[0]+' lt2:'+wt[1]

			if (i+1)<n:
				wt=mylist[i+1].split('/')	
				result+=' rw1:'+wt[0]+' rt1:'+wt[1]
			if (i+2)<n:
				wt=mylist[i+2].split('/')
				#print wt	
				result+=' rw2:'+wt[0]+' rt2:'+wt[1]
			if (i+3)<n:
				wt=mylist[i+3].split('/')	
				result+=' rw3:'+wt[0]+' rt3:'+wt[1]
			#print result
			bin_tags.append(plose.classify(result))
			#print pits.classify(result)


	#org_line=org_line.replace("it's",'its')
	#org_line=org_line.replace("It's",'Its')
	org_line=re.sub("([^a-zA-Z\-])lose([^a-zA-Z\-])","\\1l##se\\2",org_line)
	org_line=re.sub("([^a-zA-Z\-])loose([^a-zA-Z\-])","\\1l##se\\2",org_line)
	org_line=re.sub("^lose([^a-zA-Z\-])","l##se\\1",org_line)
	org_line=re.sub("([^a-zA-Z\-])lose$","\\1l##se",org_line)
	org_line=re.sub("^loose([^a-zA-Z\-])","l##se\\1",org_line)
	org_line=re.sub("([^a-zA-Z\-])loose$","\\1l##se",org_line)

	#org_line=org_line.replace("It's",'Its')
	org_line=re.sub("([^a-zA-Z\-])Lose([^a-zA-Z\-])","\\1L##se\\2",org_line)
	org_line=re.sub("([^a-zA-Z\-])Loose([^a-zA-Z\-])","\\1L##se\\2",org_line)
	org_line=re.sub("^Lose([^a-zA-Z\-])","L##se\\1",org_line)
	org_line=re.sub("([^a-zA-Z\-])Lose$","\\1L##se",org_line)
	org_line=re.sub("^Loose([^a-zA-Z\-])","L##se\\1",org_line)
	org_line=re.sub("([^a-zA-Z\-])Loose$","\\1L##se",org_line)

	beg=0
	for i in range(0,len(bin_tags)):
		#print bin_tags[i]
		j=org_line.find('l##se',beg,len(org_line))
		k=org_line.find('L##se',beg,len(org_line))
		if(j==-1 and k==-1):
			break
		elif j==-1:
			j=k
		elif k==-1:
			k=j
		elif k<j:
			j=k

		str1=org_line[0:j]
		str2=org_line[j+5:]
		if org_line[j]=='L':
			if str(bin_tags[i])==str(0):
				org_line=str1+'Lose'+str2
				beg=beg+j+4
			else:
				org_line=str1+"Loose"+str2
				beg=beg+j+5
		if org_line[j]=='l':
			if str(bin_tags[i])==str(0):
				org_line=str1+'lose'+str2
				beg=beg+j+4
			else:
				org_line=str1+"loose"+str2
				beg=beg+j+5
				
	return org_line



class res_homophone:
	txt=''
	org_txt=''

	def assign_txt(self,text):
		self.org_txt=text

	def pos_tag(self,sentence):	
		text=nltk.word_tokenize(sentence)
		ptxt=nltk.pos_tag(text)
		otxt=''
		for word in ptxt:
			otxt=otxt+word[0]+'/'+word[1]+' '
		return otxt



	def analyse_line(self,labels):
		beg=0
		n=len(self.org_txt)
		ntxt=''
		for i in range(0,n):
			if self.org_txt[i] in ['.','?','!',';']:
				txt=self.org_txt[beg:i]
				#print txt
				beg=i+1
				if ('lose' in txt) or ('Lose' in txt) or ("loose" in txt) or ("Loose" in txt):
					ptxt=self.pos_tag(txt)
					ntxt=ntxt+gen_grams(ptxt, txt)+self.org_txt[i]
				else:
					ntxt=ntxt+txt+self.org_txt[i]
		
				#print ntxt
		#print '\n\n'
		if self.org_txt[i] not in ['.','?','!',';']:
			txt=self.org_txt[beg:i]
				#print txt
			beg=i+1
			if ('lose' in txt) or ('Lose' in txt) or ("loose" in txt) or ("Loose" in txt):
				ptxt=self.pos_tag(txt)
				ntxt=ntxt+gen_grams(ptxt, txt)+self.org_txt[i]
			else:
				ntxt=ntxt+txt+self.org_txt[i]

			if(ntxt[len(ntxt)-1]=='\n'):
				ntxt=ntxt[:-1]

		print ntxt


robj=res_homophone()

for text in sys.stdin:
	robj.assign_txt(text)
	labels=['lose','Lose',"loose","Loose"]
	robj.analyse_line(labels)
#text="It's time to find out if their prepared to loose this match. If your sure, go ahead. If your not sure, then it might be to late to do anything about it. Its you're choice. "
#text="It's time to find out if their prepared to loose this match. If your sure, go ahead. If your not sure, then it might be to late to do anything about it. Its you're choice. Its awesome. I hope its awesome. It's better if its there. I hope its fine. I think its ok. The dodo bird is known for its inability to fly. This frog is too small for its aquarium."
#text="Its Its"
#robj.assign_txt(text)
#labels=['its','Its',"it's","It's"]
#robj.analyse_line(labels)
