# bing-univ-grading-tools
Tools that I find useful for grading at Binghamton University

The following are a set of tools I have been using to grade students Computer Science assignments at Binghamton University. These are designed to be run in a UNIX environment, and work with myCourses infrastructure, in coordination with GitHub Classroom. Most of these tools are written in either Python or Perl, and should run almost anywhere.

The list of tools follows:

## degrade.py - Extract student submissions from myCourse Assignment Download

To create an Assignment Download file, in myCourses, under "Full Grade Center", right click on the arrow next to the assignment name and choose "Assignment File Download". Scroll to the bottom of the resulting page, and select "Show All", then clock on the button next to the "Name" header at the top of the page to select all students, and click on the "Submit" button. Then click on the "Download Assignments now" hyperlink. This will create a gradebook_.... .zip file in your Downloads directory.  Move from your Downloads directory to the subdirectory where you want to work on the assignment, and run the degrade.py script in that directory.

degrade.py will...

- Read the first gradebook_\*.zip file in the current directory

- Extract student submission info from the zip file and put it in ./sdoc/<student_name>/submission.txt

- Extract any submitted files from the student and put them in ./submissions/<student_name>/ If there are any .zip files, unzip these files in ./submissions/<student_name>

- Details (with time/date stamp) are appended to degrade_log.txt file in the current directory

- The gradebook_\*.zip file that has been processed will be deleted

## gitStudents.pl - Clone student repositories from GitHub Classroom

A perl script which clones repositories for a list of students from a GitHub Classroom Organization. Note: Needs to be re-written in Python.

Warning - The Git userid for the professor is hard-coded in the script. Please edit the script before using it to change this value.

Warning - the name of the assignment is taken from the current directory name.  gitStudents.pl assumes the current directory name is <name>_students, where <name> is the repository prefix.
  
Warning - the gitStudents.pl script assumes there is a file in the current directory called **students.txt**. This file consists of multiple lines, where each line contains 1) the name of the student (with blanks replaced by underscores), followed by white-space, followed by 2) the Git Userid of the student.

Warning - The gitStudents.pl script assumes that there are both sdoc and submissions subdirectories of the current directory, and that the sdoc directory has subdirectories for each student with a file called "submission.txt" in it. This is the infrastructure produced by the degrade.pl script!  Furthermore, the submission.txt files should have the hash code associated with the student submitted directory.

gitStudents.pl will...

- Prompt for the professor's GIT password (and read it in no-echo mode)

- Loop through students.txt, and for each line...

- If there is already a ./submissions/<assignment>-<gitId> directory, move it to an archive (./submissions/<assignment-<gitId>_ver_<nnn>)

- Look in sdoc/<student>/submission.txt to find the git Commit Hash submitted by the student
  
- clone the student repository, and reset it to the version represented by the git Commit Hash in ./submissions/<assignment>-<gitid>
  
## massPush.py - Push a file into multiple student repositories
 
Warning mashPush.py assumes a file in the current directory called ***students.csv***, which is a comma separated file, where each line contains a student name, student id, student gitHub id

Warning - The GitHub organization is hardCoded in the massPush.py script. Before you use this script, please edit the CLASS_NAME variable.

Warning - massPush.py assumes you have an SSH link with gitHub established. If that SSH link has a passphrase, you will be prompted for the passphrase twice for each student.

massPush.py assumes that the modified file (or files) you want to push are in the current directory, and that you have specified the names of the file(s) as command line argument(s).

massPush.py will...

- For each line in students.csv....

- clone the students current version of the repository

- Replace the file specified on the command line in the student's repository with the version of that file in the current directory

- Do a git commit with the comment "Professor improving instructions", followed by a git push

- Remove the student's cloned repository

Note... It would be good to add logging to this script.
Note... It would be good to generate an email to the students, telling them to do a pull.

## allX.pl - Perform the same command on a list of students

Warning - Assumes a file called ***students.txt*** which contains a line for each student, where each line has the list of parameters associated with that student.

Command line argument: The name of a command to run for each student.

allX.pl will...

- For each student in students.txt...

- Print the command to be executed for that student, and put up a prompt.  A null response (just enter) will continue. Any non-null response will quit allX.pl

- Invoke the command for that student.

- When the command for that student finishes, put up another prompt. If the response is "r", rerun for the current student. If the response is any other non-blank entry, quit the allX.pl script (the same student will be rerun on the next execution of allX.pl.) A blank response will remove this student from the "students.txt" file, and put her at the end of the "finished_students.txt" file.

The allX.pl command is designed to allow grading to occur on a list of students in chunks. Quit the script in the middle of the list, and then re-invoke allX.pl to continue from where you left off. If you need to specify both a student name and a gitHub userid, put them both in students.txt and they will both be passed as separate paramters to the command being run.

## sortStudents.pl - Sort by last name

A simple filter to take a list of student names (with blnaks replaced by underscores) from stdin, sort by last name, and write the sorted list out to stdout.

## getBmail.py - Extract email userid's from myCourses Users View

First, browse myCourses Users, select show all, right click to view source and save html. Feed the result into this script, which will write a CSV that contains bnumber, name, and bmail.


 
 
