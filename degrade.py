#! /usr/bin/python3

# In Brightspace,  select the assignment name to see the list of submissions. Scroll to the bottom of the page
# 	and make sure that all students are displayed. Then click on the select checkbox at the top of the list to select
#    all submissions, and click on "Download". This starts to create a download file.
#    When the download file has been created, select the "Download" button to copy that onto your computer, in
#    the "Downloads" folder.
#
#    Move the resulting file, whose name will start with the assignment name, to your directory for this assignment.
#
#    Run degrade.py in the assignment directory, specifying the assignment name as a parameter.
# 
# degrade.py will...
# 	Read the <assignment_name>*.zip file in the current directory
# 	Extract student submission info from the zip file and put it in ./sdoc/<student_name>/submission.txt
#  Extract any submitted files from the student and put them in ./submissions/<student_name>/
#     If there are any .zip or .tar files, unzip these files in ./submissions/<student_name>
#
#  Details (with time/date stamp) are appended to degrade_log.txt file in the current directory

import sys
import glob
import re
import zipfile
import tarfile
from pathlib import Path
import os
import logging
import os.path
from os import path

logging.basicConfig(filename='degrade_log.txt',format='%(asctime)s %(message)s',level=20)

if (len(sys.argv) < 2) :
	print("Please invoke as ",sys.argv[0]," <assignment_name>");
	exit(1);
	
assignment = sys.argv[1];
assignment = assignment.replace("_"," ");
print("Working on assignment: ", assignment);



zfiles=glob.glob(assignment+'*.zip');
# print("assignment:",assignment);
# print("zfiles:",zfiles);
if (len(zfiles)==0) :
	print("There are no ",assignment,"*.zip files in the current directory... quitting");
	logging.warning("There are no %s*.zip files in the current directory... quitting",assignment)
	exit(1)
	
zfile=zfiles[-1]
if (len(zfiles)>1) :
	print("The current directory contains multiple assignment files. Working on the last in the list: ",zfile);
	logging.warning("There are multiple assignment files in the current directory... selected: %s",zfile);

# my ($sid,$sname,$sdate)=$gbfile=~/^gradebook_(\d+\.\d+)_(.*)_(.*)\.zip$/;
isgroup=False
gbinfo=re.match("("+assignment+".*) Download (\S\S\S \d+, \d+) (\d+ [AP]M).zip",zfile)
if not gbinfo:
	print("Trying group submission format");
	# gbinfo=re.match("("+assignment+".*) Download (\S\S\S \d+, \d+) (\d+ [AP]M)\(Group Submission Folder\).zip",zfile)
	gbinfo=re.match("("+assignment+".*) Download (\S\S\S \d+, \d+) (\d+ [AP]M) \(Group Submission Folder\)\.zip",zfile)
	isgroup=True
if gbinfo: 
	aname=gbinfo[1]
	adate=gbinfo[2]
	atime=gbinfo[3]
	print("Working on Brightspace assignment: ",aname," downloaded on", adate,"at",atime)
	logging.info("Working on Brightspace assignemnt: %s downloaded on %s at %s",aname,adate,atime);

	# Check to see if there is a subdirectory of the current path for students
	if (not Path('./students').is_dir()) : os.mkdir('./students')

	with zipfile.ZipFile(zfile) as zobj :
		for zname in zobj.namelist() :
			if (zname=="index.html") : continue
			fileInfo=re.match("(.*)/(.*)",zname);
			studentDir=fileInfo[1];
			file=fileInfo[2];
			if isgroup :
				#print("Working on group submission:",studentDir)
				studentInfo=re.match("(\d{4,6})-\d{4,6} - .* (\d+) - (.*) - (.*)",studentDir);
				if studentInfo :
					sid=studentInfo[1];
					sfullname=studentInfo[3]; # Submitters full name
					sname=re.split(" ",sfullname);
					sdir='students/group_'+studentInfo[2];
					sSubmit=studentInfo[4];
					#print("Extracted from",studentDir," - sid=",sid,"sfullname=",sfullname,"sdir=",sdir);
				else :
					logging.warning("Unable to extract group information from: %s",studentDir);
					print("Unable to extract group information from:",studentDir);
					continue;
			else :
				studentInfo=re.match("(\d{4,6})-\d{4,6} - (.*) - (.*)",studentDir);
				if studentInfo :
					sid=studentInfo[1]
					sfullname=studentInfo[2];
					sname=re.split(" ",sfullname);
					sdir='students/'+sname[-1]+'_'+sname[0]
					sSubmit=studentInfo[3];
				else : 
					logging.warning("Unable to extract sudent information out of %s",studentDir)
					print("Unable to extract student information out of",studentDir);
					continue;

			if (not Path(sdir).is_dir()) : os.mkdir(sdir)
			
			target=sdir+'/'+file;
			subFile=open(sdir+'/submission_info.txt',"a");
			if (path.exists(target)) :
				# GOT THIS WRONG!!! the current submission is NEWER than the one we've already got. Change sdir to prev!
				#pdir=sdir+'/prev'
				#if (not Path(pdir).is_dir()) : os.mkdir(pdir)
				#pv=0;
				#target=pdir+'/'+file+'v'+str(pv)
				#while(path.exists(target)):
				#	pv=pv+1;
				#	target=pdir+'/'+file+'v'+str(pv)
				#zobj.extract(zname,path=sdir)
				#os.rename(sdir+'/'+zname,target)
				#subFile.write("File %s presubmitted on %s moved to %s\n"%(file,sSubmit,target));
				#logging.info("Student %s pre-submitted %s on %s",sfullname,file,sSubmit);
				pdir=sdir+'/prev'
				if (not Path(pdir).is_dir()) : os.mkdir(pdir)
				pv=0;
				ptarget=pdir+'/'+file+'_v'+str(pv)
				while(path.exists(ptarget)):
					pv=pv+1;
					ptarget=pdir+'/'+file+'_v'+str(pv)
				os.rename(sdir+'/'+file,ptarget)
				subFile.write("Earlier submission: file %s moved to %s\n"%(file,ptarget));
				logging.info("Student %s early version of file %s moved to %s",sfullname,file,ptarget);
			# else :
			# Extract the file into the student directory
			zobj.extract(zname,path=sdir)
			os.rename(sdir+'/'+zname,target)
			subFile.write("File %s submitted on %s\n"%(file,sSubmit));
			logging.info("Student %s submitted %s on %s",sfullname,file,sSubmit);
			# unzip and/or untar the student submission if required...
			if (file.endswith('.zip')) :
				with zipfile.ZipFile(target,'r') as subZip :
					logging.info("  Extracting all files from student zip file %s into %s",file,sdir)
					subZip.extractall(path=sdir)
			elif (file.endswith('.tar.gz') or file.endswith('.tar')) :
				try :
					with tarfile.open(target, 'r',errorlevel=2) as subTar :
						logging.info("  Extracting all files from student tar file %s into %s",file,sdir);
						subTar.extractall(sdir);
				except: 
						logging.info("  Extract of files from student tar file %s failed.",file);
			# Also handle RAR files?
			os.rmdir(sdir+'/'+studentDir);
			subFile.close();
			
	logging.info("Extract of file %s complete",zfile);
	print("Extract of file",zfile,"complete");
else :
	logging.warning("Unable to extract information out of file name: %s ",zfile);
	print("Unable to extract information out of file name:",zfile);
		
exit(0)
