print '                           ~Author Aboubacar Diawara....Student at Stevens Institute of Technology~'
print '                                                                     Prof. Eins. Richard '
print
print
print
print '                                    A short program reading and printing each line of a GEDCOM file. '
print '       Printing the level number and  the tag of each line that has a valid tag for our project, or prints "Invalid tag" '


key_words = ['INDI','NAME','SEX','BIRT','DEAT','FAMC','FAMS','FAM','MARR','HUSB','WIFE','CHIL','DIV','DATE','HEAD','TRLR','NOTE']

#opening or reading file

text_file = open('My-Family-26-Sep-2016-267.ged','r')
inp = text_file

print " Printing each line of gedcom file followed by its level number and its tag "

#Looping through each line
for line in inp:
    line = line.strip()
    print " line is: ", line
    
    # getting level number
    
    level_number = int(line[:1])
    #level_number = line[:1]
    
    print " Level number is:  ", level_number   
    
    #spliting the line into individual word
    line_words = line.split()
    
    # get the first element since that is the tag of line
    line_tag = line_words[1].strip() 

    # check if Tag is among the keywords
    if line_tag in key_words:
        
        print " Tag is:  ", line_tag ,"\n"
    
    else:
        
        print "invalid tag \n"



