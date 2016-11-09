import sys 
import pandas as pd 
from datetime import datetime
from datetime import timedelta

#Dictionary of the family
fam ={}
#Dictionary of the individual
indi ={}

#getting todays date 
today = datetime.now()
end_date1 =  today - timedelta(days=30)
end_date2 =  today + timedelta(days=30)

date_type = ''

print "Please enter file path only"

ged_file = raw_input ("Please Enter the file path:")

#Usng try and except to print error message if file not found

try:
    open_file = open ( ged_file )

except:
    print "File not found"
    raise SystemExit

for line in open_file:
        line = line.rstrip().lstrip()
        #spliting line into individual words
        words = line.split()
        
        #pushing individual data
        if words[0] == '0' and len(words) == 3 and words[2] == 'INDI':
            id_type = words[1]
            id_tag = words[2]
            indi[id_type] = {}
        
        elif words[0] == '1' and len(words) >3 and words[1] == 'NAME':
            indi[id_type][words[1]] = ' '.join(words[2:])
        
        elif words[0] == '1' and len(words) ==3 and words[1] == 'SEX':
            indi[id_type][words[1]] = ' '.join(words[2:])
        
        elif words[0] == '1' and len(words) == 2 and words[1] == 'BIRT':
            ex1 = next(open_file).rstrip().lstrip()
            term1 = ex1.split()
            indi[id_type]['BIRT'] = ' '.join(term1[2:])
            
        elif words[0] == '1' and len(words) == 3 and words[1] == 'DEAT':
            ex2 = next(open_file).rstrip().lstrip()
            term2 = ex2.split()
            indi[id_type]['DEAT'] = ' '.join(term2[2:])
    
        elif words[0] == '1' and len(words) == 3 and words[1] == 'FAMS':
            indi[id_type][words[1]] = ' '.join(words[2:])
        
        elif words[0] == '1' and len(words) == 3 and words[1] == 'FAMC':
            indi[id_type][words[1]] = ' '.join(words[2:])
 
        #pushing family data
        if words[0] == '0' and len(words) == 3 and words[2] == 'FAM':
            id_type1 = words[1]
            id_tag1 = words[2]
            fam[id_type1] = {}
            fam[id_type1]['CHIL'] = []
        
        elif words[0] == '1' and len(words) == 3 and words[1] == 'HUSB':
            fam[id_type1][words[1]] = ' '.join(words[2:])
            
        elif words[0] == '1' and len(words) == 3 and words[1] == 'WIFE':
            fam[id_type1][words[1]] = ' '.join(words[2:])
            
        elif words[0] == '1' and len(words) == 3 and words[1] == 'CHIL':
            fam[id_type1][words[1]] += [' '.join(words[2:])]
        
        elif words[0] == '1' and len(words) == 2 and words[1] == 'MARR':
            ex3 = next(open_file).rstrip().lstrip()
            term3 = ex3.split()
            fam[id_type1]['MARR'] = ' '.join(term3[2:])
        
        elif words[0] == '1' and len(words) == 2 and words[1] == 'DIV':
            ex4 = next(open_file).rstrip().lstrip()
            term4 = ex4.split()
            fam[id_type1]['DIV'] = ' '.join(term4[2:])
print "\n"

print"===================================== INDIVIDUAL INFORMATION ==================================================="
#Printing detailed individual inforamtion in non-tabular form
for k in sorted(indi.keys()):
    print "Unique ID of Individual:-", k
    print "Name of the Individual:-", indi[k]["NAME"]
    if indi[k].has_key('BIRT'):
        print "Birthdate of the Individual:-", indi[k]["BIRT"]
    if indi[k].has_key('SEX'):
        print "SEX of the Individual:-", indi[k]["SEX"]
    if indi[k].has_key('DEAT'):
        print "DEATH of the Individual:-", indi[k]["DEAT"]
    print "\n"

print"===================================== INDIVIDUAL INFORMATION ( tabular form ) =================================="

#printing individual data in tabular form.
print "\n"                  
person = pd.DataFrame(indi).T
person.fillna(0, inplace=True)
print(person)

print"===================================== FAMILY INFORMATION ========================================================"

#Printing detailed family inforamtion in non-tabular form
for f in sorted(fam.keys()):
    print "Unique ID of the family:-", f
    if fam[f].has_key('HUSB'):
        print "Husband in the family is:- " + indi[fam[f]['HUSB']]['NAME']
    if fam[f].has_key('WIFE'):
        print "Wife in the family is:- " + indi[fam[f]['WIFE']]['NAME']
    #looping thourgh family data to print name of all childrens realted to each family 
    for c in fam[f]['CHIL']:
        print "Children in the family:-" + indi[c]['NAME']
    print "\n"

print"===================================== FAMILY INFORMATION ( tabular form ) ======================================="
#printing family data in tabular form
Family = pd.DataFrame(fam).T
Family.fillna(0, inplace=True)
print(Family)
print "\n"

#===================================== Start-US22-Unique ID ============================================================ 
#Programmer - Aboubacar Diawara
# All family and individual ids are stored by program 

IndiID = []
Namelist1 = []
FamID = []
famlist1 = []
for individual_id in indi:
    individual = indi[individual_id]
    IndiID.append(individual_id)
Namelist1 = set (IndiID)
print "US22: Number of duplicate Individual IDs:-",len(IndiID)-len(Namelist1),"\n" 
for family_id in fam:
    family = fam[family_id]
    FamID.append(family_id)   
famlist1 = set (FamID)
print "US22: Number of duplicate Family IDs:-",len(FamID)-len(famlist1),"\n"
#===================================== Start-US22-Unique ID ============================================================


#===================================== Start-US01-Dates before current date ==============================================
#Programmer - Aboubacar Diawara
for individual_id in indi:
    individual = indi[individual_id]
    
    if individual.has_key('BIRT'):
        Bdate = datetime.strptime(indi[individual_id]["BIRT"],"%d %b %Y") 
        if Bdate > today:
            print "Error US01:-Birthdate ",Bdate,"is after current date \n"
    
    if individual.has_key('DEAT'):
        Ddate = datetime.strptime(indi[individual_id]["DEAT"],"%d %b %Y")
        if Ddate > today:
            print "Error US01:- Deathdate ",Ddate,"is after current date \n"

for family_id in fam:
    family = fam[family_id]

    husbandID = ""
    wifeID = ""
    weddingDate = ""
    divorceDate = ""
    if family.has_key('HUSB'): husbandID = family['HUSB']
    if family.has_key('WIFE'): wifeID = family['WIFE']
    if family.has_key('MARR'): weddingDate = family['MARR']
    if family.has_key('DIV'): divorceDate = family['DIV']
    
    if weddingDate:
        WD =datetime.strptime(weddingDate,"%d %b %Y")
        if WD > today:
            print "Error US01:- Weddingdate ",WD,"is after current date \n" 
    
    if divorceDate:
        DD =datetime.strptime(weddingDate,"%d %b %Y")
        if DD > today:
            print "Error US01:- Weddingdate ",DD,"is after current date \n" 

#===================================== END-US01-Dates before current date ===============================================
for individual_id in indi:
    individual = indi[individual_id]
    
#===================================== Start-US03-Birth Before Death ====================================================    
#Programmer - Pinkal Ganjawala
    if individual.has_key('BIRT') and individual.has_key('DEAT'):
        Bdate = datetime.strptime(indi[individual_id]["BIRT"],"%d %b %Y")
        Ddate = datetime.strptime(indi[individual_id]["DEAT"],"%d %b %Y")       
        if Bdate > Ddate:
            print "Anomaly:US03:- ID:-",individual_id,"Name",individual["NAME"],"Born after the death \n" 
            
#===================================== END-US03-Birth Before Death ======================================================

#===================================== US36 Start - List recent death ===================================================     
#Programmer - Pinkal Ganjawala   
    if individual.has_key('DEAT'):       
       Deathdate = datetime.strptime(indi[individual_id]["DEAT"],"%d %b %Y")
       if Deathdate >= end_date1 and Deathdate <= today:
           print "US36- ID:-",individual_id,",Name:-",individual["NAME"], "is died within last 30 days, Death date :-",Deathdate,"\n"
           
#======================================US36 End - List recent death ===================================================== 

#======================================== US35 Start-List recent birth ================================================== 
#Programmer - Aboubacar Diawara
#Birth is normal thing hence we are not considering it as an anomaly or an error
   
    if individual.has_key('BIRT'):       
       Birthdate = datetime.strptime(indi[individual_id]["BIRT"],"%d %b %Y")
       if Birthdate >= end_date1 and Birthdate <= today:
           print "US35 - ID:-",individual_id,",Name:-",individual["NAME"], "is born within last 30 days and has birthdate :-",Birthdate,"\n" 
#===================================== US35 End-List recent birth  ======================================================

#======================================== US38 Start-list upcoming birthday =============================================
#Programmer - Pinkal Ganjawala
    if individual.has_key('BIRT'):       
       Birthdate = datetime.strptime(indi[individual_id]["BIRT"],"%d %b %Y").replace(year =today.year)       
       if Birthdate >= today and Birthdate <= end_date2:
           print "US38 - ID:-",individual_id,",Name:-",individual["NAME"], "has birthday within next 30 days \n"
           
#======================================== US38 End-list upcoming birthday ===============================================

#======================================== US27 Start- Include individual ages ===========================================
#Programmer - Pinkal Gajawala
for individual_id in indi:
    individual = indi[individual_id]        
    if individual.has_key('BIRT'):       
        indi[individual_id]['AGE']  = today.year - (datetime.strptime(indi[individual_id]["BIRT"],"%d %b %Y")).year              
person = pd.DataFrame(indi).T
person.fillna(0, inplace=True)
print "US27:Individual Ages \n"
print(person.filter(['NAME','BIRT','AGE'])) 
print "\n"

#=============================================== US27 END - Include individual ages ======================================= 

for family_id in fam:
    family = fam[family_id]

    husbandID = ""
    wifeID = ""
    weddingDate = ""
    divorceDate = ""
    if family.has_key('HUSB'): husbandID = family['HUSB']
    if family.has_key('WIFE'): wifeID = family['WIFE']
    if family.has_key('MARR'): weddingDate = family['MARR']
    if family.has_key('DIV'): divorceDate = family['DIV']
      
#===================================== START-US02-Birth before marriage ==================================================
#Programmer - Aboubacar Diawara     
    if husbandID and wifeID and weddingDate:
        WD =datetime.strptime(weddingDate,"%d %b %Y")
        HB = datetime.strptime(indi[husbandID]['BIRT'],"%d %b %Y")
        WB = datetime.strptime(indi[wifeID]['BIRT'],"%d %b %Y")
        if HB > WD:
            print "Anomaly:US02:- ID",family_id,"Name",indi[husbandID]["NAME"],"Married beore Birth\n"
        if WB > WD:
            print "Anomaly:US02:- ID",family_id,"Name",indi[wifeID]["NAME"],"Married beore Birth \n"

#===================================== END-US02-Birth before Marriage ====================================================
#===================================== US10 Start- Marriage after 14 =======================================================
#Programmer - Aboubacar Diawara
    if husbandID and wifeID and weddingDate:
        Datedifference1 = (datetime.strptime(weddingDate,"%d %b %Y")).year - (datetime.strptime(indi[husbandID]["BIRT"],"%d %b %Y")).year
        Datedifference2 = (datetime.strptime(weddingDate,"%d %b %Y")).year - (datetime.strptime(indi[wifeID]["BIRT"],"%d %b %Y")).year
        if Datedifference1 < 14:
            print "US10: - ANOMALY (Fam " + family_id + "): The marriage of " + indi[husbandID]["NAME"] + " took place before he was 14 years old. \n"
        if Datedifference2 < 14:
            print "US10: - ANOMALY (Fam " + family_id + "): The marriage of " + indi[wifeID]["NAME"] + " took place before she was 14 years old.\n"
            
#===================================== US10 End - Marriage after 14 ========================================================
#===================================== START-US04-Marriage before divorce ================================================    
#programmer - Aboubacar Diawara   
    if weddingDate != "" and divorceDate != "":
        print "Couple is, Husband:-",indi[husbandID]["NAME"],"Wife:-",indi[wifeID]["NAME"]
        if weddingDate > divorceDate:
            print "Anomaly:US04 :-ID",family_id,"HUsband",indi[husbandID]["NAME"],"and ID",family_id,"Wife",indi[wifeID]["NAME"],"are divorced before Marriage \n"

#===================================== End-US04-Marriage before divorce ==================================================
#===================================== Start-US23-Unique name and birthdate ============================================== 
#Programmer - Pinkal Gajawala
Namelist =[]
Namelist1 =[]
Birthdate =[]
Birthdate1 =[]

for individual_id in indi:
    individual = indi[individual_id]
    Name = indi[individual_id]["NAME"].split()
    Namelist.append(Name[0])
    if individual.has_key('BIRT'):
        Bdate = datetime.strptime(indi[individual_id]["BIRT"],"%d %b %Y")
        Birthdate.append(Bdate)

Namelist1 = set (Namelist)
print "US23: Number of duplicate names:-",len(Namelist)-len(Namelist1),"\n"
Namelist.sort()
for i in range(0,len(Namelist)-1):
               if Namelist[i] == Namelist[i+1]:
                   print "Error:US23:-ID",individual_id,"Name",str(Namelist[i]) + " is duplicate \n" 

Birthdate1  = set (Birthdate)
print "US23: Number of duplicate Birthdates:-",len(Birthdate) - len(Birthdate1),"\n" 
Birthdate.sort()
for j in range(0,len(Birthdate)-1):
               if Birthdate[j] == Birthdate[j+1]:
                   print "Error:US23:-ID",individual_id,"Bithdate",str(Birthdate[j]) + " is duplicate" 
#===================================== END-US23-Unique name and birthdate ================================================ 
#===================================== US17 Start - Parents not marrying children =============================================
#Programmer - Pinkal Gajawala   
    for child_id in family['CHIL']:
         if husbandID:
            if husbandID == child_id:
                    print "US17 Error :- Wife",indi[wifeID]["NAME"], " married her child, ",indi[child_id]["NAME"]
            if wifeID:
                if wifeID == child_id:
                    print "US17 Error :- Husband",indi[husbandID]["NAME"], " married his child, ",indi[child_id]["NAME"]

#===================================== US17 End - Parents not marrying children ===============================================            

