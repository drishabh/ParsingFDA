##  Extracting drugs related to a adr in file called drug_ADR.txt
##  System requirements: Python3 or greater. won't work on 2.7 as urllib.request does not
##  exist in Python 2.7, which contains urllib2 as its counterpart.

##  Change the API key of each program when run in parallel
##  Description: Program to fetch all drug names (mostly brand names) along with thier substance name related to a particular ADR
##  Author: Rishabh Dalal
##  Version: 2.0

import urllib.request
from os.path import exists
import time
import os
import os.path
import copy

#https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct.exact=%22aspirin%22+AND+receivedate:[20040201+TO+20040301]&limit=100&skip=1600

##http = "https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct.exact=\"aspirin\"+AND+receivedate:[20040101+TO+20040201]&limit=100&skip=1600"

def firstStep(drugname):
    flag = False

    #Checking if the drug occurs in openFDA
    try:
        http = "https://api.fda.gov/drug/event.json?api_key=pseoQ9rTCIYAV9XwTczwXcJvn8LEQsenxlDGFplB&search=patient.reaction.reactionmeddrapt.exact=\"" + drugname.replace(" ", "%20") + "\""
        
        url = urllib.request.urlopen(http)
        data = url.read().decode("UTF-8")
    except:
        print("This reaction is not in openFDA")
        flag = True
        
    if not flag:   ##If it occurs
        for i in data.splitlines():
            ##Fetching total number of safety reports of that drug
            if "\"total\":" in i:
                line = i.split(":")
                total = line[1].strip()
                total = int(total)
                boolean = False
                print("Total safety reports for", drugname, "are", total)
                if total < 5000 and not boolean:
                    print("Going all in one go")
                    boolean = oneGo(drugname, total)

                if total < 36000 and not boolean:
                    print("Going yearly")
                    boolean = yearly(drugname)

                if total < 70000 and not boolean:
                    print("Going 6 months")
                    boolean = biyearly(drugname)
        
                if total < 90000 and not boolean:
                    print("Going three months")
                    boolean = qurteryearly(drugname)

                if not boolean:
                    print("Going month by month")
                    monthly(drugname)
                if not boolean:
                    print("It has failed. Look for another way to get its safety reports")
                return boolean
            

def oneGo(drugname, total):
    print("Going for all at once")
    print("Quering from the server\n")
    filename = str(drugname) + ".txt"
    file = open(filename, 'w')

    ##Looping using skip
    for skip in range(0, total, 100):
        http =  "https://api.fda.gov/drug/event.json?api_key=pseoQ9rTCIYAV9XwTczwXcJvn8LEQsenxlDGFplB&search=patient.reaction.reactionmeddrapt.exact=\"" + drugname.replace(" ", "%20") + "\"+AND+receivedate:[20040101+TO+20180101]&limit=100&skip="+str(skip)
        
        
        url = urllib.request.urlopen(http)
        data = url.read().decode("utf-8")
        
        file.write(data)
        file.write('\n')

    file.close()
    print(drugname, "DONE fetching safety reports")

    return True


def yearly(drugname):
    print("Going yearly")
    print("Quering from the server\n")

    first = [20040101, 20050102, 20060103, 20070104, 20080105, 20090106, 20100107, 20110108, 20120109, 20130110, 20140111, 20150112, 20160113, 20170114]

    second = [20050101, 20060102, 20070103, 20080104, 20090105, 20100106, 20110107, 20120108, 20130109, 20140110, 20150111, 20160112, 20170113, 20180114]
    netTotal = 0

    filename = str(drugname) + ".txt"
    file = open(filename, 'w')
    for r in range(len(first)):
        skip = 0
        while True:
            ##To break when we have fetched all the safety reports for a particular year or if a particular year
            ##does not have any safety reports
            try:
                http =  "https://api.fda.gov/drug/event.json?api_key=pseoQ9rTCIYAV9XwTczwXcJvn8LEQsenxlDGFplB&search=patient.reaction.reactionmeddrapt.exact=\"" + drugname.replace(" ", "%20") + "\"+AND+receivedate:[" + str(first[r]) + "+TO+" + str(second[r]) + "]&limit=100&skip="+str(skip)

                url = urllib.request.urlopen(http)
                data = url.read().decode("utf-8")
                if skip == 0:   ##Checking to see if each year has less than 5100 drugs or not
                    for i in data.splitlines():
                        if "\"total\":" in i:
                            line = i.split(":")
                            total = line[1].strip()
                            total = int(total)
                            netTotal += total
                            print("Net till now", netTotal)                 
                            break
                    if total > 5100:
                        ##returning False if it has more than 5100 drugs
                        print("This search won't work as total safety repots exceed 5100. The query is:", '\n', http)
                        file.close()
                        return False
                skip += 100             
                file.write(data)
                file.write('\n')

            except urllib.error.HTTPError:
                break
        

    print(drugname,"DONE fetching safety reports")
    print("Total written for", drugname, ":", netTotal)
    file.close()
    return True

def biyearly(drugname):
    print("Going bi-yearly")
    netTotal = 0
    print("Quering from the server\n")
    
    
    first = [20040101, 20040602, 20050103, 20050604, 20060105, 20060606, 20070107, 20070608, 20080109, 20080610, 20090111, 20090612, 20100113, 20100614, 20110115, 20110616, 20120117, 20120618, 20130119, 20130620, 20140121, 20140622, 20150123, 20150624, 20160125, 20160626, 20170127, 20170628]
    second = [20040601, 20050102, 20050603, 20060104, 20060605, 20070106, 20070607, 20080108, 20080609, 20090110, 20090611, 20100112, 20100613, 20110114, 20110615, 20120116, 20120617, 20130118, 20130619, 20140120, 20140621, 20150122, 20150623, 20160124, 20160625, 20170126, 20170627, 20180128]
    filename = str(drugname) + ".txt"
    file = open(filename, 'w')


    for r in range(len(first)):
        skip = 0
        while True:
            try:
                http =  "https://api.fda.gov/drug/event.json?api_key=pseoQ9rTCIYAV9XwTczwXcJvn8LEQsenxlDGFplB&search=patient.reaction.reactionmeddrapt.exact=\"" + drugname.replace(" ", "%20") + "\"+AND+receivedate:[" + str(first[r]) + "+TO+" + str(second[r]) + "]&limit=100&skip="+str(skip)
                    
                url = urllib.request.urlopen(http)
                data = url.read().decode("utf-8")
                
                if skip == 0:
                    for i in data.splitlines():
                        if "\"total\":" in i:
                            line = i.split(":")
                            total = line[1].strip()
                            total = int(total)
                            netTotal += total
                            print("Net till now", netTotal)                 
                            break
                    if total > 5100:
                        print("This search won't work as total safety repots exceed 5100. The query is:", '\n', http)
                        file.close()
                        return False
                skip += 100
                
                
                file.write(data)
                file.write('\n')

            except urllib.error.HTTPError:
                break


    print(drugname,"DONE fetching safety reports")
    print("Total written for", drugname, ":", netTotal)
    file.close()
    return True


def qurteryearly(drugname):

    print("Going quarter-yearly")
    netTotal = 0
    print("Quering from the server\n")

    
    first = [20040101, 20040402, 20040703, 20041004, 20050105, 20050406, 20050707, 20051008, 20060109, 20060410, 20060711, 20061012, 20070113, 20070414, 20070715, 20071016, 20080117, 20080418, 20080719, 20081020, 20090121, 20090422, 20090723, 20091024, 20100125, 20100426, 20100727, 20101028, 20110129, 20110502, 20110703, 20111004, 20120105, 20120506, 20120707, 20121008, 20130109, 20130510, 20130711, 20131012, 20140113, 20140514, 20140715, 20141016, 20150117, 20150518, 20150719, 20151020, 20160121, 20160522, 20160723, 20161024, 20170125, 20170526, 20170727, 20171028]


    second = [20040401, 20040702, 20041003, 20050104, 20050405, 20050706, 20051007, 20060108, 20060409, 20060710, 20061011, 20070112, 20070413, 20070714, 20071015, 20080116, 20080417, 20080718, 20081019, 20090120, 20090421, 20090722, 20091023, 20100124, 20100425, 20100726, 20101027, 20110128, 20110501, 20110702, 20111003, 20120104, 20120505, 20120706, 20121007, 20130108, 20130509, 20130710, 20131011, 20140112, 20140513, 20140714, 20141015, 20150116, 20150517, 20150718, 20151019, 20160120, 20160521, 20160722, 20161023, 20170124, 20170525, 20170726, 20171027, 20180128]

    filename = str(drugname) + ".txt"
    file = open(filename, 'w')
    
    for r in range(len(first)):
        skip = 0
        while True:
            try:
                http =  "https://api.fda.gov/drug/event.json?api_key=pseoQ9rTCIYAV9XwTczwXcJvn8LEQsenxlDGFplB&search=patient.reaction.reactionmeddrapt.exact=\"" + drugname.replace(" ", "%20") + "\"+AND+receivedate:[" + str(first[r]) + "+TO+" + str(second[r]) + "]&limit=100&skip="+str(skip)
                    
                url = urllib.request.urlopen(http)
                data = url.read().decode("utf-8")
                
                if skip == 0:
                    for i in data.splitlines():
                        if "\"total\":" in i:
                            line = i.split(":")
                            total = line[1].strip()
                            total = int(total)
                            netTotal += total
                            print("Net till now", netTotal)             
                            break
                    if total > 5100:
                        print("This search won't work as total safety repots exceed 5100. The query is:", '\n', http)
                        file.close()
                        return False
                skip += 100
                
                
                file.write(data)
                file.write('\n')

            except urllib.error.HTTPError:
                break


    print(drugname,"DONE fetching safety reports")
    print("Total written for", drugname, ":", netTotal)
    file.close()
    return True


def monthly(drugname):
    
    print("Going monthly")
    netTotal = 0
    print("Quering from the server\n")

    first = [20040101, 20040202, 20040303, 20040404, 20040505, 20040606, 20040707, 20040808, 20040909, 20041010, 20041111, 20050112, 20050213, 20050314, 20050415, 20050516, 20050617, 20050718, 20050819, 20050920, 20051021, 20051122, 20060123, 20060224, 20060325, 20060426, 20060527, 20060628, 20060729, 20060902, 20061003, 20061104, 20070105, 20070206, 20070307, 20070408, 20070509, 20070610, 20070711, 20070812, 20070913, 20071014, 20071115, 20080116, 20080217, 20080318, 20080419, 20080520, 20080621, 20080722, 20080823, 20080924, 20081025, 20081126, 20090127, 20090302, 20090403, 20090504, 20090605, 20090706, 20090807, 20090908, 20091009, 20091110, 20100111, 20100212, 20100313, 20100414, 20100515, 20100616, 20100717, 20100818, 20100919, 20101020, 20101121, 20110122, 20110223, 20110324, 20110425, 20110526, 20110627, 20110728, 20110902, 20111003, 20111104, 20120105, 20120206, 20120307, 20120408, 20120509, 20120610, 20120711, 20120812, 20120913, 20121014, 20121115, 20130116, 20130217, 20130318, 20130419, 20130520, 20130621, 20130722, 20130823, 20130924, 20131025, 20131126, 20140127 , 20140302, 20140403, 20140504, 20140605, 20140706, 20140807, 20140908, 20141009, 20141110, 20150111, 20150212, 20150313, 20150414, 20150515, 20150616, 20150717, 20150818, 20150919, 20151020, 20151121, 20160122, 20160223, 20160324, 20160425, 20160526, 20160627, 20160728, 20160902, 20161003, 20161104, 20170105, 20170206, 20170307, 20170408, 20170509, 20170610, 20170711, 20170812, 20170913, 20171014, 20171115, 20180116]



    second = [20040201, 20040302, 20040403, 20040504, 20040605, 20040706, 20040807, 20040908, 20041009, 20041110, 20050111, 20050212, 20050313, 20050414, 20050515, 20050616, 20050717, 20050818, 20050919, 20051020, 20051121, 20060122, 20060223, 20060324, 20060425, 20060526, 20060627, 20060728, 20060901, 20061002, 20061103, 20070104, 20070205, 20070306, 20070407, 20070508, 20070609, 20070710, 20070811, 20070912, 20071013, 20071114, 20080115, 20080216, 20080317, 20080418, 20080519, 20080620, 20080721, 20080822, 20080923, 20081024, 20081125, 20090126, 20090301, 20090402, 20090503, 20090604, 20090705, 20090806, 20090907, 20091008, 20091109, 20100110, 20100211, 20100312, 20100413, 20100514, 20100615, 20100716, 20100817, 20100918, 20101019, 20101120, 20110121, 20110222, 20110323, 20110424, 20110525, 20110626, 20110727, 20110901, 20111002, 20111103, 20120104, 20120205, 20120306, 20120407, 20120508, 20120609, 20120710, 20120811, 20120912, 20121013, 20121114, 20130115, 20130216, 20130317, 20130418, 20130519, 20130620, 20130721, 20130822, 20130923, 20131024, 20131125, 20140126, 20140301, 20140402, 20140503, 20140604, 20140705, 20140806, 20140907, 20141008, 20141109, 20150110, 20150211, 20150312, 20150413, 20150514, 20150615, 20150716, 20150817, 20150918, 20151019, 20151120, 20160121, 20160222, 20160323, 20160424, 20160525, 20160626, 20160727, 20160901, 20161002, 20161103, 20170104, 20170205, 20170306, 20170407, 20170508, 20170609, 20170710, 20170811, 20170912, 20171013, 20171114, 20180115, 20180216]
    filename = str(drugname) + ".txt"
    file = open(filename, 'w')

    for r in range(len(first)):
        skip = 0
        while True:
            try:
                http =  "https://api.fda.gov/drug/event.json?api_key=pseoQ9rTCIYAV9XwTczwXcJvn8LEQsenxlDGFplB&search=patient.reaction.reactionmeddrapt.exact=\"" + drugname.replace(" ", "%20") + "\"+AND+receivedate:[" + str(first[r]) + "+TO+" + str(second[r]) + "]&limit=100&skip="+str(skip)
                    
                url = urllib.request.urlopen(http)
                data = url.read().decode("utf-8")
                
                if skip == 0:
                    for i in data.splitlines():
                        if "\"total\":" in i:
                            line = i.split(":")
                            total = line[1].strip()
                            total = int(total)
                            netTotal += total
                            print("Net till now", netTotal)                 
                            break
                    if total > 5100:
                        print("This search won't work as total safety repots exceed 5100. The query is:", '\n', http)
                        file.close()
                        return False
                skip += 100
                
                
                file.write(data)
                file.write('\n')

            except urllib.error.HTTPError:
                break


    print(drugname,"DONE fetching safety reports")
    print("Total written for", drugname, ":", netTotal)
    file.close()
    return True

def create_df_file(filename, adr):
    ##Extracting the required infor from all the safety reports

    start = time.time()
    print("Getting all drug names along with substance names if they have any")
    file = open(filename, 'r')
    writeToFile = filename.replace(".txt", '') + "_ADR.txt"
    file2 = open(writeToFile, 'w')
    myDict = {}
    myReactionDict = {}
    count = 0
    safetyreport = 0
    drugCount = 0
    drugName = ""
    myList = []
    
    d = []
    for line in file:
        line = line.strip()
        flag = False
        if line == "\"patient\": {":
            mySet = set()
            flag = True
            patientStack = ["("]
            myReactionDict = {}

            while patientStack != []:
                line = file.readline().strip()

                if "[" in line or "{" in line:
                    patientStack.append("(")
                elif "]" in line or "}" in line:
                    patientStack.pop()


                if line == "\"reaction\": [":
                    
                    reactionStack = ["("]
                    
                    while len(reactionStack) != 0:
                        line = file.readline()
                        if "[" in line or "{" in line:
                            reactionStack.append("(")
                            patientStack.append("(")
                        elif "]" in line or "}" in line:
                            reactionStack.pop()
                            patientStack.pop()
                        line = line.strip().split(":")
                        requiredWord = line[0].strip()[1:-1]
                        if requiredWord == "reactionmeddrapt":
                            reaction = line[-1].strip()[1:-1]
                            reaction = reaction.lower()
                            myReactionDict[reaction] = None
                            
                            
                    
                if line == "\"drug\": [":
                    drugCount = 0
                    stack2 = ["["]
                    
                    while stack2 != []:
                        line = file.readline()
                        line = line.strip()
                
                        if "{" in line or "[" in line:
                            stack2.append("{")
                            patientStack.append("(")

                        if "}" in line or "]" in line:
                            stack2.pop()
                            patientStack.pop()
                        line = line.strip().split(":")
                        requiredWord = line[0][1:-1]
                        if len(line) > 1:
                        
                            if requiredWord == "medicinalproduct":
                                drugName = line[1].strip()
                                if drugName[-1] == ",":
                                    drugName = drugName[:-1]
                                drugName = drugName.strip()[1:-1]

                        
                            elif requiredWord == "substance_name":
                                while True:
                                    count += 1
                                    line = file.readline()
                                    
                                    line = line.strip()
                                    if line[-1] == ",":
                                        line = line[:-1].strip()
                                    
                                    if line == "]":
                                        stack2.pop()
                                        patientStack.pop()
                                        break

                                    line = line[1:-1]
                                    d.append(line)
                                
                        if len(stack2) == 1 and stack2[-1] == "[":
                            active = ""
                            for j in d:
                                active += j
                                active += "~"
                            active = active[:-1]
                            output = drugName + "$" + active + '\n'
                            myList.append(output)
                            d = []
        
        if flag:
            if adr in myReactionDict:
                for i in myList:
                    file2.write(i)

    file.close()
    end = time.time()
    print("DONE in time:", end-start, "seconds")
    
def main():
    file = open("adr.txt", 'r')
    resultFile = open("result.txt", 'w')
    for line in file:
        if line != '\n':
            adr = line.strip().lower()
            print("ADR:", adr)
            boolean = firstStep(adr)
            if boolean:
                    filename = adr + ".txt"
                    create_df_file(filename, adr)
                    result = adr + ":" + "DONE" + '\n'
                    resultFile.write(result)
                    os.remove(filename)
            else:
                result = adr + ":" + "FAILED" + '\n'
                resultFile.write(result)
            print()
    file.close()

main()

