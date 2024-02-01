#! /usr/bin/python3

# For each line in students_todo.txt...
#   Parse the line into blank delimited tokens
#   Replace @n in the command arguments with the nth token from student_todo.txt
#   Prompt... Run the command?
#			'q' - Quit immediately... do not run the command
#			Any other response... run the command
#   Prompt the user...
#			'r' - repeat processing for this student
#			'q' - Quit immediately... do not treat this student as processed
#			Any other response... mark the student as complete... get the next student 

import sys
import subprocess

def getNextStudent() :
	f=open("students_todo.txt","r");
	line=f.readline()
	f.close()
	if (line) :
		fields=line.split()
		return fields
	sys.exit("students_todo.txt file empty");

def studentComplete(sname) :
	with open("students_todo.txt", 'r+') as f: # open file in read / write mode
		firstLine = f.readline() # read the first line
		fldsf=firstLine.split()
		if (fldsf[0] != sname) :
			print("Error... First line of students_todo.txt file does not match the student we just finished with");
			sys.exit("Problem with students_todo.txt");
		data = f.read() # read the rest
		f.seek(0) # set the cursor to the top of the file
		f.write(data) # write the data back
		f.truncate() # set the file size to the current size
		with open("students_done.txt",'a') as of:
			of.write(firstLine);
	print("Student",sname,"marked as complete")
       
cmdList=sys.argv
cmdList.pop(0) # Remove this script invocation
rawCmdLine=' '.join(cmdList)
while(1) :
	flds=getNextStudent()
	cmd=rawCmdLine
	for i in range(len(flds)) :
		token='@'+str(i)
		cmd=cmd.replace(token,flds[i])
	r1=input("Run command: " + cmd + " ==> ")
	if (r1 == "q") : break
	# print("Running:",cmd)
	subprocess.run(cmd,shell=True)
	r2=input("next ==> ")
	if (r2 == "q") : break
	if (r2 == "r") : continue
	studentComplete(flds[0]);
	