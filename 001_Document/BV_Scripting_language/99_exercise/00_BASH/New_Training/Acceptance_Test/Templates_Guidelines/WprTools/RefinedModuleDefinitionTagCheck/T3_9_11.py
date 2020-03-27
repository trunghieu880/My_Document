import sys
import getopt
import os
import re

ASR_VER_REGEX = r'\d\.\d\.\d'
ASR_VER_SRC_REGEX = r'[\w \.]*(\d[\-\.]\d[\-\.]\d)[\w \.]*\.[xX][sS][dD]'
ASR_PATH = r'xsi:schemaLocation="http://autosar.org/'
REFINED_REGEX = r'(<REFINED\-MODULE\-DEF\-REF DEST=' + \
				r'\"((ECUC\-MODULE\-DEF)|(MODULE\-DEF))">)' + \
				r'([\w\/]*)(<\/REFINED\-MODULE\-DEF\-REF>)'

family = ''
msn = ''


def check_T3_9(path):
	src_ver = ''
	asr_version = re.search(ASR_VER_REGEX, path).group(0)
	print 'Device Variant folder : ' + asr_version
	fd = open(path);
	for line in fd:
		if line.find(ASR_PATH) != -1:
			match = re.search(ASR_VER_SRC_REGEX, line)
			if match != None:
				print "PDF Autosar version : " + match.group(0)
				src_ver = match.group(1)
			break
	src_ver = src_ver.replace(r'-', r'.')
	if asr_version == src_ver:
		print '\n[3.09] VERIFIED OK\n'
	else:
		print '\n[3.09] VERIFIED NG\n'
	fd.close()
	pass

def check_T3_11(path):
	isExist = False
	fd = open(path);
	for line in fd:
		match = re.search(REFINED_REGEX, line)
		if match != None:
			isExist = True
			src_ver = match.group(0)
			print "Refined Tag Founded:"
			print match.group(1)
			print '\t' + match.group(5)
			print match.group(6)
			print '\n[3.11] VERIFIED OK'
			break
	if isExist == False:
		print '\n[3.11] VERIFIED NG'
	pass

def print_instruction():
	print '\n'
	print '=========================================================================='
	print '                   HELP TO LAUNCH T3_9'
	print '=========================================================================='
	print 'Usage:'
	print 'python T3_9.py -m[--msn]=<MODULE_SHORT_NAME> -f[--family]=<PRODUCT_FAMILY>'
	print 'e.g. python T3_9.py -m=mcu -f=F1x\n'
	print 'MODULE_SHORT_NAME - Module Short Name to be verified e.g. port, can, mcu, ...'
	print 'PRODUCT_FAMILY - Product family e.g. F1x, P1x-E, P1x-C...'
	print '==========================================================================='
	pass

try:
	opts, args = getopt.getopt(sys.argv[1:], 'm:f:', ['msn', 'family'])
except getopt.GetoptError:
	_, err, _ = sys.exc_info()
	print str(err)
	sys.exit(2)
# opts, args = getopt.getopt(sys.argv[1:], 'm:f:', ['msn', 'family'])

# print opts
# print args

k = ''
v = ''

for k, v in opts:
	if k in ('-m', '--msn'):
		msn = v.replace(r'=', '')
	elif k in ('-f', '--family'):
		family = v.replace(r'=', '')
	else:
		assert False, 'Unhandled option'

if k == '' or v == '':
	print 'Missing options'
	print_instruction()
	sys.exit(2)
	pass

# print '###' + msn + '###' + family

doc_path = 'U:\\external\\X1X\\' + family + '\\modules\\' + msn + '\\definition\\'

# print doc_path

for path, dirs, files in os.walk(doc_path):
	for f in files:
		if f.find(r'.arxml') != -1:
			print 'PDF : ' + f
			check_T3_9(path + '\\' + f)
			check_T3_11(path + '\\' + f)
