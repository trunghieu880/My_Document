import os
import sys
import mmap
import re
import collections
from fnmatch import fnmatch
	
# List all UUIDs in all modules
list_UUID = [] #list_all (module, file_name, UUID)
list_file = [] #list_file (module, file_name)
list_file_duplicate = [] #list_file (module, file_name)
list_UUID_only = [] # only contain UUID
list_duplicate_UUID = [] # cotain information about duplicate UUID (module, file_name, duplicate UUID)
list_deviceFamily = [] # list of device family (Ex: Common, P1L-C, F1K...)
pattern = 'UUID="'
# type_check = 'PDF'
# family = 'P1x-C'
# ArVersion = '4.0.3'
# module_link = "U:\\external\\X1X\\" + family + "\\modules\\"
# module_list = os.listdir(module_link)

def get_DeviceFamily():
	tempt_list_deviceFamily = []
	for i in range(len(module_list)):
		module = module_list[i]
		PDF_module_link = module_link + module + "\\definition\\" + ArVersion
		deviceFamily = os.listdir(PDF_module_link)
		for j in range(len(deviceFamily)):
			tempt_list_deviceFamily.append(deviceFamily[j])
	list_deviceFamily = [item for item, count in collections.Counter(tempt_list_deviceFamily).items() if count > 1]
	return list_deviceFamily
	
# list_deviceFamily = get_DeviceFamily()
	
def print_instruction():
	print '\n'
	print '=========================================================================='
	print '                   HELP TO LAUNCH Check_UUID'
	print '=========================================================================='
	print 'Usage:'
	print 'python Check_UUID.py <family> <ArVersion> <type_check>'
	print '<family>		Product family e.g. F1x, P1x-E, P1x-C...'
	print '<ArVersion> 	4.0.3 or 4.2.2'
	print '<type_check> PDF or BSWMDT'
	print '==========================================================================='
	pass

# search_DeviceFamily in full PDF name 	
def search_DeviceFamily(PDF_name_full):
	# deviceFamilyName = ""
	for i in range(len(list_deviceFamily)):
		checkFamilyName = list_deviceFamily[i]
		if (PDF_name_full.find(checkFamilyName) != -1):
			deviceFamilyName = checkFamilyName
	return deviceFamilyName

def search_DuplicateDeviceFamily(list_PDFname): #list_PDFname (module, file name)
	list_deviceFamilyName = []
	list_PDFwithDupDevFam = []
	for i in range(len(list_PDFname)):
		list_deviceFamilyName.append(search_DeviceFamily(list_PDFname[i][1]))
	#Find list_DuplicateDeviceFamily
	list_DuplicateDeviceFamily = [item for item, count in collections.Counter(list_deviceFamilyName).items() if count > 1]
	#Search DuplicateDeviceFamily in list_PDFname 
	for j in range(len(list_deviceFamilyName)):
		for k in range(len(list_DuplicateDeviceFamily)):
			if list_deviceFamilyName[j] == list_DuplicateDeviceFamily[k]:
				list_PDFwithDupDevFam.append(list_PDFname[j])
	return list_PDFwithDupDevFam
		
# Main Script
if len(sys.argv) == 4:
	if ((str(sys.argv[2]) != "4.0.3") and (str(sys.argv[2]) != "4.2.2")) or ((str(sys.argv[3]) != "PDF") and (str(sys.argv[3]) != "BSWMDT")):
		print str(sys.argv[2])
		print str(sys.argv[3])
		print "Wrong parameter for ARVersion or type check \n"
		print_instruction()
		sys.exit(2)
		pass
else:
	print_instruction()
	sys.exit(2)
	pass
	
family = str(sys.argv[1])
ArVersion = str(sys.argv[2])
type_check = str(sys.argv[3])
module_link = "U:\\external\\X1X\\" + family + "\\modules\\"
module_list = os.listdir(module_link)
list_deviceFamily = get_DeviceFamily()

for i in range(len(module_list)):
	module = module_list[i]
	if type_check == 'PDF':
		PDF_module_link = module_link + module + "\\definition\\" + ArVersion
		for root, dirs, files in os.walk(PDF_module_link):
			for file in files:
				if file.endswith(".arxml"):
					path = os.path.join(root,file)
					list_file.append((module, path))
	else:
		path = module_link + module + "\\generator\\R" + ArVersion.replace(".","") + "_" + module.upper() + "_" + family + "_BSWMDT.arxml"
		list_file.append((module, path))
		
for j in range(len(list_file)):
	f = open(list_file[j][1], 'r+b')
	mf = mmap.mmap(f.fileno(), 0)
	mf.seek(0)
	index = [m.start() for m in re.finditer(pattern, mf)]
	for x in range(0, len(index)):
		if mf[index[x] + 6] == "E":
			UUID = mf[index[x]: (index[x] + 48)]
		else:
			UUID = mf[index[x]: (index[x] + 43)]
		list_UUID.append((list_file[j][0], list_file[j][1], UUID))
		list_UUID_only.append(UUID)
	mf.close()
	f.close()

# Check duplicate in list UUIDs
list_duplicate_UUID_only = [item for item, count in collections.Counter(list_UUID_only).items() if count > 1]

# Check all list_duplicate_UUID_only to find duplicate UUID with different module
for i in range(len(list_duplicate_UUID_only)):
	list_file_duplicate_tempt = []
	Duplicate_Result = "OK"
	for j in range(len(list_UUID)):
		if (list_duplicate_UUID_only[i] == list_UUID[j][2]):
			list_file_duplicate_tempt.append((list_UUID[j][0], list_UUID[j][1]))
	# check duplicate with type_check is "PDF" or "BSWMDT"
	if type_check == "PDF":
		list_file_duplicate = search_DuplicateDeviceFamily(list_file_duplicate_tempt)
	else:
		list_file_duplicate = list_file_duplicate_tempt
	
	# Find NG duplicate
	if len(list_file_duplicate) > 0:
		for k in range(len(list_file_duplicate) - 1):
			if (list_file_duplicate[k][0] != list_file_duplicate[k+1][0]):
			# if (list_file_duplicate[k][0] != list_file_duplicate[k+1][0]) or (list_file_duplicate[k][1] == list_file_duplicate[k+1][1]):
				Duplicate_Result = "NG"
	
	if (Duplicate_Result == "NG"):
		if len(list_file_duplicate) > 0:
			list_duplicate_UUID.append((list_file_duplicate, list_duplicate_UUID_only[i]))
			
# print files duplicate UUIDs
if len(list_duplicate_UUID) > 0:
	for i in range(len(list_duplicate_UUID)):
		print list_duplicate_UUID[i][1] + "duplicate at files"
		for j in range(len(list_duplicate_UUID[i][0])):
			print (list_duplicate_UUID[i][0])[j][1]
		print "\n"
else:
	print "NO FOUND DUPLICATE UUID \n"
	