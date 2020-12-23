import threading
import subprocess
import requests
import shutil
import os
import time
import gzip
import datetime
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import sys
import re
from common_variables import *

def xml_merge(notification=False):
	xmltvs = []
	if selfAddon.getSetting('xmltv1') != '':
		xmltvs.append(selfAddon.getSetting('xmltv1'))
		t1 = threading.Thread(name='xmltv1', target=download_and_extract , args=('1-',selfAddon.getSetting('xmltv1'),))
		t1.start()
		
	if selfAddon.getSetting('xmltv2') != '':
		xmltvs.append(selfAddon.getSetting('xmltv2'))
		t2 = threading.Thread(name='xmltv2', target=download_and_extract , args=('2-',selfAddon.getSetting('xmltv2'),))
		t2.start()

	if selfAddon.getSetting('xmltv3') != '':
		xmltvs.append(selfAddon.getSetting('xmltv3'))
		t3 = threading.Thread(name='xmltv3', target=download_and_extract , args=('3-',selfAddon.getSetting('xmltv3'),))
		t3.start()

	if selfAddon.getSetting('xmltv4') != '':
		xmltvs.append(selfAddon.getSetting('xmltv4'))
		t4 = threading.Thread(name='xmltv4', target=download_and_extract , args=('4-',selfAddon.getSetting('xmltv4'),))
		t4.start()	
		
	if selfAddon.getSetting('xmltv5') != '':
		xmltvs.append(selfAddon.getSetting('xmltv5'))
		t5 = threading.Thread(name='xmltv5', target=download_and_extract , args=('5-',selfAddon.getSetting('xmltv5'),))
		t5.start()	

	if selfAddon.getSetting('xmltv6') != '':
		xmltvs.append(selfAddon.getSetting('xmltv6'))
		t6 = threading.Thread(name='xmltv6', target=download_and_extract , args=('6-',selfAddon.getSetting('xmltv6'),))
		t6.start()
		
	if selfAddon.getSetting('xmltv7') != '':
		xmltvs.append(selfAddon.getSetting('xmltv7'))
		t7 = threading.Thread(name='xmltv7', target=download_and_extract , args=('7-',selfAddon.getSetting('xmltv7'),))
		t7.start()

	if selfAddon.getSetting('xmltv8') != '':
		xmltvs.append(selfAddon.getSetting('xmltv8'))
		t8 = threading.Thread(name='xmltv8', target=download_and_extract , args=('8-',selfAddon.getSetting('xmltv8'),))
		t8.start()

	if selfAddon.getSetting('xmltv9') != '':
		xmltvs.append(selfAddon.getSetting('xmltv9'))
		t9 = threading.Thread(name='xmltv9', target=download_and_extract , args=('9-',selfAddon.getSetting('xmltv9'),))
		t9.start()
		
	if selfAddon.getSetting('xmltv10') != '':
		xmltvs.append(selfAddon.getSetting('xmltv10'))
		t10 = threading.Thread(name='xmltv10', target=download_and_extract , args=('10-',selfAddon.getSetting('xmltv10'),))
		t10.start()
		
	if selfAddon.getSetting('xmltv11') != '':
		xmltvs.append(selfAddon.getSetting('xmltv11'))
		t11 = threading.Thread(name='xmltv11', target=download_and_extract , args=('11-',selfAddon.getSetting('xmltv11'),))
		t11.start()
						
	try:t1.join()
	except:pass
	try: t2.join()
	except:pass
	try: t3.join()
	except:pass
	try: t4.join()
	except:pass
	try: t5.join()
	except:pass
	try: t6.join()
	except:pass
	try: t7.join()
	except:pass
	try: t8.join()
	except:pass
	try: t9.join()
	except:pass
	try: t10.join()
	except:pass
	try: t11.join()
	except:pass
	
	print "Starting extraction process..."
	
	dirs, files = xbmcvfs.listdir(os.path.join(datapath,'download_folder'))
	for ficheiro in files:
		if ficheiro.endswith('.xz'):
			infn = os.path.join(datapath,'download_folder',ficheiro)
			task = subprocess.Popen(['xz', '-dc', infn], stdout=subprocess.PIPE)
			s = task.stdout.read()
			assert task.wait() == 0
			p = s.find('<?xml')
			if p == -1: p = 0
			outF = file(os.path.join(datapath,'download_folder',ficheiro.replace('.xz','')+'.xml'),'wb')
			outF.write(s[p:])
			outF.close()
			os.remove(os.path.join(datapath,datapath,'download_folder',ficheiro))
		elif not ficheiro.endswith('.xml'):
			inF = gzip.GzipFile(os.path.join(datapath,'download_folder',ficheiro), 'rb')
			s = inF.read()
			inF.close()
			p = s.find('<?xml')
			if p == -1: p = 0
			outF = file(os.path.join(datapath,'download_folder',ficheiro.replace('.gz','')+'.xml'),'wb')
			outF.write(s[p:])
			outF.close()
			os.remove(os.path.join(datapath,datapath,'download_folder',ficheiro))
		else:
			print ficheiro + " nao e um zip...skip"
	print "Extracting done"
	print "merging starts here...."
	dirs, xmltv_list = xbmcvfs.listdir(os.path.join(datapath,'download_folder'))
	out = os.path.join(selfAddon.getSetting('output_folder'),selfAddon.getSetting('file_name').replace('.xml','')+'.tmp')
	if xbmcvfs.exists(out): os.remove(out)
	i = 1
	for xmltv in xmltv_list:
		f = open(os.path.join(datapath,'download_folder',xmltv), "r")
		text = f.read()
		f.close()
		if i == 1:
			with open(out, "a") as myfile:
				myfile.write(re.sub(r"</tv[^>]*>","",text))
		else:
			with open(out, "a") as myfile:
				myfile.write(re.sub(r"<xml[^>]*>|</?tv[^>]*>","",text))
		os.remove(os.path.join(datapath,'download_folder',xmltv))
		i += 1
	o = open(out,"a")
	o.write('</tv>')
	o.close()
	print "Xmltvs have been merged"
	if notification:
		xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('PVR Tools', "EPG's Merged!", 1,os.path.join(addonfolder,"icon.png")))
	os.rename(out,out.replace('.tmp','.xml'))
	return
