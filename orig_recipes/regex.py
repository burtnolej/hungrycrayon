#!/usr/bin/python

import re

# is the string of the pattern word word,word
#m = re.match(r"(\w+) (\w+), (\w+)", "Isaac Newton, physicist")
#print m.group(0)

# match only works from start of string
#m = re.search("c","abcdef")

#pat1 = re.compile('foo.trailingString')
#mat1 = pat1.match(mystring)

'''
character class / special chars
[abc],[a-c] will match any of the chars a,b & c
[^5] any char but 5
[\]] match a ]
[\d] matches any decimal same as [0-9]
[\D] complement of above so any non-decimals same as [^0-9]
[\s] whitespace
[\S] non white space
[\w] any alphanumeric same as [a-zA-Z0-9_]
repeats
ca*t will match ct,cat,caat,caaat etc
ca+t will match cat, caat etc but not ct
ca?t will match ct cat only
a/{1,3}b will match a/b, a//b. a///b but not ab or a////b
'''

#p = re.compile('[a-z]+')
#print  p.findall('**tempo** tempo')
#print m.span()
#iterator = p.finditer('**tempo**tempa')
#for match in iterator:
#    print match.group(), match.span()

#paragraph = 'this is a sentence\n with carriage returns in it and \n lines as well wool'

#for match in re.finditer(r'[a-z]+','**tempo**tempa'):
#print paragraph
#for match in re.finditer(r'w[a-z]*l',paragraph):
#    print match.group(), match.span()

# find any , between " " like "fdfsdf,ddf"
#s = "dfgdfg,dfgfgdfg,,dfgdfgfg,\"sffsdf,sdfsdf\""
#p = re.compile('["][^"]*["]|[^,]*')
#y = p.findall(s)

# substitute
#cpy_mangle = re.sub("\"","",fields[3])
    
# find words between words/tags
#s = "<tag start> is sdsd </tag>"
#p = re.compile("start(\w+)end")
#p = re.compile("start (.*?) end")

#op = re.compile("<tag[^>]*> (.*?) </tag>")
#<TAG\b[^>]*>(.*?)</TAG>

#print len(p.findall(s))

# find complete words that 
m = re.compile(r"__\w+")
s = "nottag __tag1 nottag __tag2"
print m.findall(s)
