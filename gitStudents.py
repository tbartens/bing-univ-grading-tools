#! /usr/bin/python3

# Run after degrade.py is run
# 
# This script does the following:
#
#	A. Get's the next student from your students.txt file.
#
#	B. Looks at sdoc/<student name>/submission.txt and extracts the hash code the
#	student pasted into his submission. If it can't find it, it skips this student.
#
#	C. Runs a git clone command using your userid, the students repository name (the
#	repository prefix is taken from the current directory name, with _students
#	removed, and -<student gitHub id> added) and using the hash code to get the
#	correct level. You will be prompted for your git password for each student. (I
#	tried to automate this, but couldn't get it to work. Suggestions?) The
#	repository is put in the "submissions" sub-directory.

import logging
import getpass
import os
import re
from pathlib import Path
import subprocess
import sys

from html.parser import HTMLParser
import datetime
	
class MyHTMLParser(HTMLParser):

	def __init__(self):
		super(MyHTMLParser,self).__init__()
		self.hashcode=""
	
	def handle_starttag(self,tag,attrs): pass
		# if (tag.equals("p") return
		# print("Encounterred a start tag:", tag)
		#for attr in attrs :
		#	print("  attribute:", attr)
		
	def handle_endtag(self, tag): pass
		# print("Encountered an end tag :", tag)
			
	def handle_data(self, data):
		# Got some arbitrary data
		if (data) :
			flds=data.split()
			for fld in flds :
				if re.match("[0-9,A-F,a-f]{40}",fld) :
					self.hashcode=fld

logging.basicConfig(filename='gitStudents_log.txt',format='%(asctime)-15s %(levelname)s %(message)s',level=20)

# PROF_ID='tbartens'; # <-------------- Please update with your GIT userid!
# PROF_PWD=getpass.getpass(prompt=f'Enter the password for GIT userid {PROF_ID} : ');
CLASS_NAME='CS220-2024S'; # Current organization to work on
pwd=os.getcwd();
rep=os.path.basename(pwd)
# If there is a command line argument, use the first command line argument as the rep instead of the directory name
if (len(sys.argv) > 1) :
	rep=sys.argv[1];
# print ("Current directory is :",pwd," repository is ",rep);
logging.info("Working in directory: %s assignment: %s",pwd,rep);
logging.debug("git class: %s",CLASS_NAME);

if (not Path("students.txt").exists()) :
	logging.error("No students.txt file in the current directory.");\
	print("No students.txt file in the current directory... quitting.")
	exit(1)
	
if (not Path("students").is_dir()) :
	logging.error("No students subdirectory in the current directory.");
	print("Please run degrade.py before running gitStudents.py");
	exit(1);
	
repara=re.compile("\<p\>(.*)\<\/p\>")
respan=re.compile("\<span [^\>]*\>(.*)\<\/span\>")
# Example: HW01 Object Oriented C-Jan 30, 2023 700 PM.html
rehtmlfn=re.compile(".*\-([A-Z][a-z]{2}) (\d+), (\d+) (\d+) ([AP]M).html");
rehtmlfn_x=re.compile(".*\-([A-Z][a-z]{2}) (\d+), (\d+) (\d+) ([AP]M)\((\d+)\).html");

with open("students.txt","r") as students:
	for line in students :
		std_flds=line.split()
		student=std_flds[0]
		print("  Working on student : ",student);
		# print("Student name is ", std_flds[0], " git ID is ", std_flds[1]);
		sdir="students/"+student
		if (not Path(sdir).exists()) :
			logging.error("No student submission for student %s",student);
			continue
		
		if (len(std_flds)<2) :
			logging.error("No git userid in students.txt for user %s",student);
			continue;
			
		student_git_id=re.sub(" ","_",std_flds[1]) # git replaces blanks in team names with underscores
		student_rep=rep+"-"+student_git_id;
		gitDir="students/"+student+"/"+student_rep;	
		# print ("Working on cloning: ",gitDir);
		# Rename older versions of the gitDir if it is there
		if (Path(gitDir).is_dir()) :
			rev=1;
			while(Path("students/"+student+"/rev_"+ str(rev)+student+rep).is_dir()) : rev=rev+1
			os.rename(gitDir,"students/"+student+"/rev_"+str(rev)+student+rep);
			
		# Next, read through the html file looking for the hashcode
		student_hashcode="";
		hashdate=datetime.datetime(datetime.MINYEAR,1,1,0,0);
		hashSub=-1
		for sfile in os.listdir(sdir):
			if (sfile.endswith(".html")) :
				# Pull time/date info out of file name
				# Example: HW01 Object Oriented C-Jan 30, 2023 700 PM.html
				# Or: Lab 03 Square Roots Using the Newton Raphson Method-Feb 7, 2023 1115 AM(1).html for two submissions @ same time
				submission=0;
				fnfields=rehtmlfn.match(sfile)
				if not fnfields :
					fnfields=rehtmlfn_x.match(sfile)
					if not fnfields :
						print("Unable to extract time/date out of file name:",sfile)
						sys.exit("No time date stamp in html file.");
					submission=int(fnfields[6])
				month_name=fnfields[1]
				month_number = datetime.datetime.strptime(month_name, '%b').month
				dom=int(fnfields[2])
				year=int(fnfields[3])
				hr=int(int(fnfields[4])/100)
				min=int(fnfields[4])%100
				ampm=fnfields[5]
				if (ampm=="PM" and hr !=12):  hr=hr+12;
				# print("Extracted from file name:",month_name,month_number,dom,year,hr,min,ampm)
				fdate=datetime.datetime(year,month_number,dom,hr,min)
				# print("File date/time:",fdate.ctime(),"current hash date is",hashdate.ctime());
				if (fdate>hashdate or (fdate==hashdate and submission>hashSub)) :
					hashdate=fdate
					hashSub=submission
					parser = MyHTMLParser()
					# Next, read through html file, feeding to the parser
					with open(sdir+"/"+sfile,"r") as slines :		
						for sline in slines :
							parser.feed(sline);
					student_hashcode=parser.hashcode
					if (not student_hashcode) :
						logging.error("No hash code found for student %s please check this submission manually.",student);
				#else : 
					#print("Submission on",fdate.ctime(),"ignored because it was older than the hash code submitted on",hashdate.ctime());
		try:	
			# git clone -v https://'.$PROF_ID.':'.$profPwd.'@github.com/'.$gitClass.'/'."${assignment}-${gitId}.git"
			# https://github.com/CS-220-2022S/lab01-AAboys23.git
			# "git", "clone", "-v", f'https://{PROF_ID}:{PROF_PWD}@github.com/{CLASS_NAME}/{student_rep}.git'
			p = subprocess.run(["git", "clone", "-v",f'https://github.com/{CLASS_NAME}/{student_rep}.git'],cwd = "students/"+student, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			logging.info("Cloned %s for student %s",student_rep,student)
		except subprocess.CalledProcessError as cloneError:
			logging.error("Unable to clone %s for student %s Return code=%d",student_rep,student,cloneError.returncode);
			# print("Error running clone command: ",cloneError.cmd);
			print("===Clone error - return code: ",cloneError.returncode);
			if (cloneError.stdout) : print("  clone output: ",cloneError.stdout.decode());
			continue
		if (student_hashcode) :
			try :
				# git reset --hard $SHA1
				p = subprocess.run(["git", "reset", "--hard", student_hashcode],cwd = gitDir, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
				logging.info("Reset %s for student %s using hash %s submitted on %s",student_rep,student,student_hashcode,hashdate.ctime());
			except subprocess.CalledProcessError as resetError:
				logging.error("Unable to reset %s for student %s Return code=%d using hash=%s",student_rep,student,resetError.returncode,student_hashcode);
				# print("Error running reset command: ",resetError.cmd);
				print("===Reset error - return code: ",resetError.returncode);
				if (resetError.stdout) : print("  reset output: ",resetError.stdout.decode());
				continue
		
	logging.info("All students processed.")
	print("All students processed.")
