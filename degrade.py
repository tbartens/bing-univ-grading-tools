#! /usr/bin/python3

# In grade center, right click on arrow next to assignment name and choose "Assignment File Download"
# 		Scroll to the bottom of the page and select "Show All"
# 		Then at the top of the page select the button next to the "Name" header to select all students
#		Then click the "submit" button
# 		Then click the "Download assignments now" hyperlink, and move the resulting file to the assignment directory
# Run degrade.py in the assignment directory
# 
# degrade.py will...
# 	Read the first gradebook_*.zip file in the current directory
# 	Extract student submission info from the zip file and put it in ./sdoc/<student_name>/submission.txt
#  Extract any submitted files from the student and put them in ./submissions/<student_name>/
#     If there are any .zip files, unzip these files in ./submissions/<student_name>
#
#  Details (with time/date stamp) are appended to degrade_log.txt file in the current directory
#	The gradebook_*.zip file that has been processed will be deleted

import glob
import re
import zipfile
from pathlib import Path
import os
import logging
logging.basicConfig(filename='degrade_log.txt',format='%(asctime)s %(message)s')

zfiles=glob.glob('gradebook_*.zip');
if (len(zfiles)==0) :
	print("There are no gradebook_*.zip files in the current directory... quitting");
	logging.warning("There are no gradebook_*.zip files in the current directory... quitting")
	exit(1)
	
zfile=zfiles[0]	
# print("Working on gradebook zip file: ",zfile);

# my ($sid,$sname,$sdate)=$gbfile=~/^gradebook_(\d+\.\d+)_(.*)_(.*)\.zip$/;
gbinfo=re.match("gradebook_(\d+\.\d+)_(.*)_(.*)\.zip",zfile)
sid=gbinfo[1]
sname=re.sub("20",' ',gbinfo[2])
sdatef=re.split('-',gbinfo[3])
sdate="%2d/%d %d @ %02d:%02d:%02d" % (int(sdatef[1]),int(sdatef[2]),int(sdatef[0]),int(sdatef[3]),int(sdatef[4]),int(sdatef[5]))
print("Working on gradebook zip file id: ",sid,"assignment:",sname)
logging.info("Working on gradebook file id: %s assignment: %s downloaded %s",sid,sname,sdate);

# Check to see if there are subdirectories of the current path for sdoc and submissions
if (not Path('./sdoc').is_dir()) : os.mkdir('./sdoc')
if (not Path('./submissions').is_dir()) : os.mkdir('./submissions')

resubfile=re.compile(sname+"_(b\d{8})_attempt_(.*)\.txt")
reothfile=re.compile(sname+"_(b\d{8})_attempt_([0-9\-]+)_(.*)")
student='unknown'
nextract=0
nothers=0
with zipfile.ZipFile(zfile) as zobj :
	for zname in zobj.namelist() :
		zsubm = resubfile.fullmatch(zname)
		# zsubm = re.fullmatch(sname+"_(b/d{8})_attempt_(\d{4}\-\d{2}\-\d{2}\-\d{2}\-\d{2}\-\d{2})\.txt",zname)
		if zsubm :
			bnum=zsubm[1]
			subdate=zsubm[2]
			student=bnum
			# print("  Found submission file for bnum:",bnum,"subdate:",subdate)
			# Read this file to get user name
			with zobj.open(zname) as sfile:
				for line in sfile :
					nlm=re.fullmatch("Name\: (.*) \(b\d{8}\)\s*",str(line,'utf-8'))
					if nlm :
						student=re.sub(" ","_",nlm[1])
						if (not Path('./sdoc/'+student).is_dir()) : os.mkdir('./sdoc/'+student)
						zobj.extract(zname,path="./sdoc/"+student)
						os.rename('./sdoc/'+student+'/'+zname,'./sdoc/'+student+'/submission.txt')
						print("  Working on student:",student)
						logging.info("  Extracted submission.txt for student %s (%s)",student,bnum)
						nextract=nextract+1
						break
					else :
						print("      Name not found in submission file, found:",line)			
						logging.warning("Name not found in submmission file, found: %s",line)
		else :
			zothm = reothfile.fullmatch(zname)
			if zothm :
				bnum=zothm[1]
				subdate=zothm[2]
				othfile=zothm[3]
				if (not Path('./submissions/'+student).is_dir()) : os.mkdir('./submissions/'+student)
				zobj.extract(zname,path="./submissions/"+student)
				os.rename('./submissions/'+student+'/'+zname,'./submissions/'+student+'/'+othfile)
				print("  Downloaded file",othfile,"into submissions/"+student)
				nothers=nothers+1
				if (othfile.endswith('.zip')) :
					with ZipFile('submissions/'+student+'/'+othfile,'r') as subZip :
						logging.info("  Extracting all files from student zip file %s into ./submissions/%s",othfile,student)
						subZip.extractall(path='submissions/'+student)
			else :
				print("    Unrecognized Non-Submission file:",zname)
				
os.remove(zfile)	
if (len(zfiles)>1) : print("More zfiles are available... run degrade.py again")
logging.info("Extracted info for %d students, including %d submitted files",nextract,nothers)
