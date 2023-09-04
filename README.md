# Bartenstein's TA Grading Tools

Tools that I find useful for grading at Binghamton University.

The following are a set of tools I have been using to grade students Computer Science assignments at Binghamton University. These are designed to be run in a UNIX environment, and work with the Brightspace infrastructure, in coordination with GitHub Classroom. Most of these tools are written in Python or Perl, and should run almost anywhere.

The basic process is to:

  1. Create a download zip file for the assignment from Brightspace.
  2. Run the degrade.py script to extract student information from the assignment zip file.
  3. If this is a GitHub Classroom assignment, run gitStudents.py to clone the students repositories and reset them to the correct level.
  4. Run eachStudent.py to build and test student executables in their repositories.
  5. Grade each student's results and input the grade and feedback in Brightspace.

More detail on each of these steps are included below.

Suggestions, comments, updates, corrections, improvements, alternatives, etc. are always welcome and invited.

## Create an Assignment Zip file

To create an Assignment zip file, in Brightspace:

1. In the "Assignments" tab, select the assignment. If you are grading a single section, select "View By: Sections", and then select your section.
2. Scroll to the bottom and make sure all students are displayed. Then scroll to the top and select the first box (to the left of "Last Name") to select all students, and then click on the "Download" icon.  
3. This will create a zip file and cause a popup to appear. In the popup, select the "Download" button.
4. This will download the *Assignment_Name*.zip file to your Downloads directory. (Brightspace figures out the *Assignment_Name*, and it **will** have embedded blanks in the name! Sorry.)
5. Move the assignment zip file from your Downloads directory to the subdirectory where you want to work on the assignment.

Now you are ready to run the degrade.py script in that directory.

## degrade.py - Extract student submissions from Assignment Zip file

The degrade.py script takes a single parameter: the prefix of the file name to work on. For example, if the download file is named "HW01 First Homework ... .zip", then you would invoke `degrade.py HW01`.

degrade.py will...

- Read the first *Assignment_name*.zip file in the current directory

- Extract student submission info from the zip file and put it in ./students/*student_name*/submission_info.txt. The *student_name* is defined by Brightspace, and is typically the student's last name, followed by an underscore (_), followed by the student's first name.

- Extract any submitted files from the student and put them in ./students/*student_name*/ If there are any .zip files, unzip these files in ./students/*student_name*

- If the student has made multiple submissions, degrade.py will keep all submissions, but make the latest submission the active one in the ./students/*student_name* directory. (We've had problems in the past with this not working, but I think it's fixed now. If not, let me know!)

- Details (with time/date stamp) are appended to degrade_log.txt file in the current directory.

Note, to make an update, rename or delete the original zip file before downloading a new zip file, and then rerun degrade.py.

If the students submitted files or zip files, you are now ready to grade the results. If the assignment was a GitHub Classroom assignment, more processing is required.

## gitStudents.py - Clone student repositories from GitHub Classroom

The gitStudents.py script is a python script which clones repositories for a list of students from a GitHub Classroom Organization.

Warning - The GitHub organization is hardCoded in the gitStudents.py script in the `CLASS_NAME` variable. Before you use this script, please make sure the `CLASS_NAME` variable is correct.
  
The gitStudents.py script assumes there is a file in the current directory called **students.txt**. This file consists of multiple lines, where each line contains two words:

1. the name of the student, following the conventions used by degrade.py (*last_name*_*first_name*)

2. the Git Userid of the student.

The gitStudents.py script takes a single, optional command line parameter that specifies the assignment's repository prefix (like hw01 or lab01). If no prefix is specified, then gitStudents.py assumes that the base name of the current directory is that prefix. This prefix will be saved as the *assignment*.

gitStudents.pl will:

1. Loop through students.txt, and for each line, save the *student_name* and *gitID* from that line. Then, for each line,

2. If there is already a ./students/*student_name*/*assignment*-*gitId* directory, move it to an archive (./students/*student_name*/*assignment*-*gitId*\_ver\_*nnn*, where *nnn* is a number starting at zero and counting up.)

3. Look in students/*student_name*/*.html to find the git Commit Hash submitted by the student. If there are multiple html files, looks for the html file with the latest submission time/date (which is contained in the file name.) The hash code is the first string of 40 hexadecimal digits found in the file, after parsing the html and ignoring formatting html.

4. Executes a `git clone` command to clone the students repository into ./students/*student_name*. This will create a new ./students/*student_name*/*assignment*-*gitId* clone of the student's repository.

5. Runs `git reset` using the student's hash code to reset the repository to the level indicated by the student's hash code.

Details (with time/date stamp) are appended to the gitStudents_log.txt file in the current directory.

If there are errors and gitStudents.py needs to be re-run, there is no problem. Just edit the students.txt file to run only the students that need to be re-run. (I often copy the full student list to all_students.txt before editing students.txt, just so I have the full list.)

Warning - gitStudents.py assumes you have an established your gitHub credentials using a credential manager. If not, you will be prompted for you git userid and password, or the passphrase twice for each student.

## massPush.py - Push a file into multiple student repositories

The massPush.py script should **only** be used when there is an error in the original repository, and you need to push a new version out to all students. This is inherently dangerous and should be avoided if possible because students need to do a `git pull` on all their clones after you run massPush.py.

Warning mashPush.py assumes a file in the current directory called ***students.csv***, which is a comma separated file, where each line contains a student name, student id, student gitHub id

Warning - The GitHub organization is hardCoded in the massPush.py script. Before you use this script, please edit the `CLASS_NAME` variable.

Warning - massPush.py assumes you have an SSH link with gitHub established. If that SSH link has a passphrase, you will be prompted for the passphrase twice for each student.

massPush.py assumes that the modified file (or files) you want to push are in the current directory, and that you have specified the name(s) of the file(s) as command line argument(s).

massPush.py will...

1. For each line in students.csv....

2. clone the students current version of the repository

3. Replace the file(s) specified on the command line in the student's repository with the version of that/those file(s) in the current directory.

4. Do a git commit with the comment "Professor improving instructions", followed by a git push

5. Remove the student's cloned repository

Warning - massPush.py assumes you have an established your gitHub credentials using a credential manager. If not, you will be prompted for you git userid and password, or the passphrase twice for each student.

Note... It would be good to add logging to this script.
Note... It would be good to generate an email to the students, telling them to do a pull.

## eachStudent.py - Perform the same command on a list of students

The eachStudent.py script allows you to run a command with some tokens replaced to personalize that command for a list of students.

The eachStudent.py needs a file called **students_todo.txt** which contains a line for each student. Each line has the one or more blank delimited tokens to be used to personalize the command to run. Most often, I copy the students.txt (or all_students.txt) file used for gitStudents.py into students_todo.txt.

When you run eachStudent.py, the command line arguments become the command to run for each student. If the command line arguments contain a blank delimited word of the form @*n*, where *n* is a number, then eachStudent.py will replace that token with a word from the first line of students_todo.txt. The *n* indicates which token, starting from 0, should be used.

The eachStudent.py script will:

1. If students_todo.txt is not empty, parse the first line of students_todo.txt and save each blank delimited word.

2. Replace any @*n* tokens in the command read from the command line with the associated token read from the first line of students_todo.txt to create a personalized command.

3. Print the personalized command for that student to the terminal, and put up a prompt.  A null response (just enter) will continue. Any non-null response will quit eachStudent.py

4. Run the personalized command.

5. When the personalized command finishes, put up another prompt. If the response is "r", rerun for the current student. If the response is any other non-blank entry, quit the eachStudent.py script (the students_todo.txt file has not been changed, so the same student will be rerun on the next execution of eachStudent.py.) A blank response will remove this student from the "students_todo.txt" file, and write that student's line at the end of the "students_done.txt" file. Then loop back to step 1 to work on the next student.

The eachStudent.py command is designed to allow grading to occur on a list of students with interruptions. Quit the script in the middle of the list, and then re-invoke eachStudent.py to continue from where you left off. If you need to specify both a student name and a gitHub userid, put them both in students_todo.txt and they will both be available to personalize the command being run.

## sortStudents.pl - Sort by last name

A simple filter to take a list of student names (with blanks replaced by underscores) from stdin, sort by last name, and write the sorted list out to stdout.
