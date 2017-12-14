import re
import os

def parse():

    with open("cacm.all","r") as cacm:
        newpath = r'./Collection' 
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        documents_pattern = re.compile("^.I[ ][0-9]{1,4}[\n]$")
        sections_pattern = re.compile("^.[A-Z]?[\n]$")
        interesting_sections = re.compile("^.[KWT]?[\n]$") #these are the interesting sections we need
        collection = open('I0','w') #serves only to be closed, for the loop

        for line in cacm:
            if documents_pattern.match(line) is not None:
                #this is to find the documents headers and create the files
                title = re.sub('[.\n]', '', line)
                collection.close() #closes the opened document
                filepath = os.path.join(newpath,title)
                collection = open(filepath,'w')
            elif sections_pattern.match(line) is not None:
                #this lets us know in which sections we are placed
                line_section = line
            elif interesting_sections.match(line_section):
                #when we are placed in one of our interesting sections KWT, we write in the document
                line = re.sub('\n', ' ', line)
                collection.write(line)
        collection.close()      

a = parse()
