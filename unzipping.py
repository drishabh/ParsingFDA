import zipfile
import os.path
import os
import time
import copy
import urllib.request, urllib.parse, urllib.error


def downloadingFiles(url, filename):
	#Downlading the file from given url and saves it in the same directory with name filename

	print("downloading with urllib")
	urllib.request.urlretrieve(url, filename)


def gettingDownloadFileWebAdd():
        ##Getting the web adddress of the to be downloaded files from openFDA website

	f = urllib.request.urlopen("https://api.fda.gov/download.json")
	data = f.read().decode("utf-8")
	string = "https://download.open.fda.gov/drug/event/"
	for line in data.splitlines():
		if string in line:
			line = line.strip().split("\"")
			line = line[3].strip()
			print("URL", line)
			filename = line.split("/")
			filename = filename[-1].strip()
			print("Filename", line)
			downloadingFiles(line, filename)

def unzipping(path_to_zip_file, directory_to_extract_to):
	#Unzipping a zipped file

	zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
	zip_ref.extractall(directory_to_extract_to)
	zip_ref.close() 
            
def dumpingData(path_to_file, table, db_name, delimiter):
	#Dumping any delimited file in mySQL    

	connection = MySQLdb.Connect(host='chas-wrt219a-01', user='root', passwd='s+uden+', db=db_name)
	cursor = connection.cursor()
	query = "LOAD DATA INFILE '" + path_to_file + "' INTO TABLE " + table + " FIELDS TERMINATED BY '" + delimiter + "'"
	cursor.execute(query)
	connection.commit()

def create_df_file(filename):
	#Creating a $ dilimed text file from .json file

	myDict = {"drugcharacterization":[], "medicinalproduct":[], "drugbatchnumb":[], "drugauthorizationnumb":[],   "drugstructuredosagenumb":[], "drugstructuredosageunit":[], "drugseparatedosagenumb":[], "drugintervaldosageunitnumb":[], "drugintervaldosagedefinition":[], "drugcumulativedosagenumb":[], "drugcumulativedosageunit":[], "drugdosagetext":[], "drugdosageform":[], "drugadministrationroute":[], "drugindication":[], "drugstartdateformat":[], "drugstartdate":[], "drugenddateformat":[], "drugenddate":[], "drugtreatmentduration":[], "drugtreatmentdurationunit":[], "actiondrug":[], "drugrecurradministration":[], "drugadditional":[], "activesubstancename":[], "drugrecuraction":[], "patientonsetage":None, "patientonsetageunit":None, "patientagegroup":None, "patientweight":None, "patientsex":None, "reportercountry":None, "qualification":None, "literaturereference":None,"reactionmeddraversionpt":[], "reactionmeddrapt":[], "reactionoutcome":[], "receivertype":None, "receiverorganization":None, "duplicatesource":None, "duplicatenumb":None, "safetyreportversion":None, "safetyreportid":None, "primarysourcecountry":None, "occurcountry":None, "tranmissiondateformat":None, "transmissiondate":None, "reporttype":None, "serious":None, "seriousnessdeath":None, "seriousnesslifethreatening":None, "seriousnesshospitalization":None, "seriousnessdisabling":None, "seriousnesscongenitalanomali":None, "seriousnessother":None, "receivedateformat":None, "receivedate":None, "receiptdateformat":None, "receiptdate":None, "transmissiondateformat":None, "fulfillexpeditecriteria":None, "companynumb":None, "authoritynumb":None, "duplicate":None, "sendertype":None, "senderorganization":None, "narrativeincludeclinical":None}
	duplicate_myDict = copy.deepcopy(myDict)
	dataList = ["safetyreportid", "primarysourcecountry", "occurcountry", "tranmissiondateformat", "transmissiondate", "reporttype", "serious", "seriousnessdeath", "seriousnesslifethreatening", "seriousnesshospitalization", "seriousnessdisabling", "seriousnesscongenitalanomali", "seriousnessother", "receivedateformat", "receivedate", "receiptdateformat", "receiptdate", "transmissiondateformat", "fulfillexpeditecriteria", "companynumb", "authoritynumb", "duplicate", "sendertype", "senderorganization", "narrativeincludeclinical", "patientonsetage", "patientonsetageunit", "patientagegroup", "patientweight", "patientsex", "reportercountry", "qualification", "literaturereference", "receivertype", "receiverorganization", "duplicatesource", "duplicatenumb", "safetyreportversion"]

	junkHash = {"reaction":None, "results":None, "patient":None, "drug":None, "sender":None, "primarysource":None, "receiver":None, "reportduplicate":None, "activesubstance":None, "summary":None, "drugrecurrence":None}
	
	drugDict = {"drugcharacterization":None, "medicinalproduct":None, "drugbatchnumb":None, "drugauthorizationnumb":None,   "drugstructuredosagenumb":None, "drugstructuredosageunit":None, "drugseparatedosagenumb":None, "drugintervaldosageunitnumb":None, "drugintervaldosagedefinition":None, "drugcumulativedosagenumb":None, "drugcumulativedosageunit":None, "drugdosagetext":None, "drugdosageform":None, "drugadministrationroute":None, "drugindication":None, "drugstartdateformat":None, "drugstartdate":None, "drugenddateformat":None, "drugenddate":None, "drugtreatmentduration":None, "drugtreatmentdurationunit":None, "actiondrug":None, "drugrecurradministration":None, "drugadditional":None, "activesubstancename":None, "drugrecuraction":None}

	drugList = ["drugcharacterization", "medicinalproduct", "drugbatchnumb", "drugauthorizationnumb", "drugstructuredosagenumb", "drugstructuredosageunit", "drugseparatedosagenumb", "drugintervaldosageunitnumb", "drugintervaldosagedefinition", "drugcumulativedosagenumb", "drugcumulativedosageunit", "drugdosagetext", "drugdosageform", "drugadministrationroute", "drugindication", "drugstartdateformat", "drugstartdate", "drugenddateformat", "drugenddate", "drugtreatmentduration", "drugtreatmentdurationunit", "actiondrug", "drugrecurradministration", "drugadditional", "activesubstancename", "drugrecuraction"]

	reactionDict = {"reactionmeddraversionpt":None, "reactionmeddrapt":None, "reactionoutcome":None}

	reactionList = ["reactionmeddraversionpt", "reactionmeddrapt", "reactionoutcome"]
	start = time.time()

	file = open(filename, 'r')
	file1 = open("drugList.txt", 'w')
	file2 = open("reactionList.txt", 'w')
	file3 = open("dataList.txt", 'w')

	stack = []

	for i in drugList:
		file1.write(i)
		file1.write("$")
	file1.write("\n")

	for i in reactionList:
		file2.write(i)
		file2.write("$")
	file2.write("\n")

	for i in dataList:
		file3.write(i)
		file3.write("$")
	file3.write("\n")

	count = 0
	safetyreport = 0
	drugCount = 0
	for line in file:
		
		line = line.strip().replace(",", "")
		
		if line in "{[":
			stack.append(line)
			
		elif line in "}]":
			stack.pop()
			
		else:
			line = line.strip()
			line = line.split(":")

			for word in line:
				word = word.strip().lower()
				if word in "{[":
					stack.append(word)
				elif word in "]}":
					stack.pop()
					
			requiredWord = line[0][1:-1]
			if not requiredWord in junkHash:
				if requiredWord in myDict:
					output = ""
					j = j=line[1].strip().replace("\"", "")
					myDict[requiredWord] = j 
					
					
			
			if requiredWord == "drug":
				drugCountPrevious = drugCount
				drugCount = 0
				stack2 = ["["]
				while len(stack2) != 0:
					
					line = file.readline()
										
					line = line.strip().replace(",", "")
		
					if line in "{[":
						stack2.append(line)
				
					elif line in "}]":
						stack2.pop()
						if line == "]":
							stack.pop()
			
					else:
						line = line.strip()
						line = line.split(":")
		
						for word in line:
							word = word.strip().lower()
							if word in "[{":								
								stack2.append(word)
							elif word in "}]":
								stack2.pop()
								

						requiredWord = line[0][1:-1]
						
						if requiredWord in myDict:
							output = ""
							j =line[1].strip().replace("\"", "")
							myDict[requiredWord].append(j)
							
							if requiredWord == "medicinalproduct":
								drugCount += 1
					
					##Adding None to columns that otherwisde were empty so that we can correlate which column of
					##one row matches with which column of another row

					if len(stack2) != 0 and stack2[-1] == "[":
						for i in drugDict.keys():
							if len(myDict[i]) != drugCount:
								myDict[i].append(None)

			
			elif requiredWord == "reaction":
				stack3 = ["["]
				while len(stack3) != 0:
					line = file.readline()
					line = line.strip().replace(",", "")
		
					if line in "{[":
						stack3.append(line)
				
					elif line in "}]":
						stack3.pop()	
						if line == "]":
							stack.pop()
						
		
					else:
						line = line.strip()
						line = line.split(":")
		
						for word in line:
							word = word.strip().lower()
							if word in "[{":
								stack3.append(word)
								
							elif word in "}]":
								stack3.pop()
								
						requiredWord = line[0][1:-1]
						
						##Adding None to columns that otherwisde were empty so that we can 
						##correlate which column of one row matches with which column of another row
						if requiredWord in myDict:
							output = ""
							j =line[1].strip().replace("\"", "")
							myDict[requiredWord].append(j)
							
		
		if len(stack) == 0 or stack[-1] == "[":
			print("Printing safetyreport number:", safetyreport)
			if myDict["safetyreportid"]:
				safetyreport += 1
				for i in range(len(myDict["actiondrug"])):
						file1.write(myDict["safetyreportid"])
						file1.write("$")
					
						for j in drugList:
							#print("DRUG", myDict[j], ":", myDict[j][i])
							file1.write(str(myDict[j][i]))					
							file1.write("$")
						file1.write('\n')

	
				for i in range(len(myDict["reactionoutcome"])):
						file2.write(myDict["safetyreportid"])
						file2.write("$")
	
						for j in reactionList:
							#print("REACTION", myDict[j], ":", myDict[j][i])
							file2.write(str(myDict[j][i]))
							file2.write("$")
						file2.write('\n')
			
				for j in dataList:
					#print("DATA", myDict[j], ":", j)
					file3.write(str(myDict[j]))
					file3.write("$")
				file3.write('\n')
			myDict = copy.deepcopy(duplicate_myDict)			

	file.close()
	file1.close()
	file2.close()
	
	end = time.time()
	print("Total time taken for", safetyreport, "safetyreports:", end-start)



def main():
	gettingDownloadFileWebAdd()

	tempFileName = "junkFiles"
	newpath = str(os.getcwd()) + "/" + tempFileName
	if not os.path.exists(newpath):
		os.makedirs(newpath)

	directoryList = os.listdir('.')  ### '.' indicates the current directory
	for dirItem in directoryList:
		if not os.path.isdir(dirItem) and dirItem[-2:] != "py":
			path_to_zipped_file = str(os.getcwd()) + "/" + dirItem	            
			unzipping(path_to_zipped_file, newpath)

	os.chdir(newpath)   ### Go into subdirectory of all extracted files

	directoryList = os.listdir('.')

	for dirItem in directoryList:
		if dirItem[-5:] == ".json":
			print("INSIDE")
			create_df_file(dirItem)    ###Create the $ delimited file
##		        dumpingData(path_of_file)           ###3 diff files in diff tables

main()
