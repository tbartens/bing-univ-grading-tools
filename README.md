# bing-univ-grading-tools
Tools that I find useful for grading at Binghamton University

The following are a set of tools I have been using to grade students Computer Science assignments at Binghamton University. These are designed to be run in a UNIX environment, and work with myCourses infrastructure, in coordination with GitHub Classroom. Most of these tools are written in either Python or Perl, and should run almost anywhere.

The list of tools follows:

## degrade.py - Extract student submissions from a myCourse Assignment Download File

To create an Assignment Download file, in myCourses, under "Full Grade Center", right click on the arrow next to the assignment name and choose "Assignment File Download". Scroll to the bottom of the resulting page, and select "Show All", then clock on the button next to the "Name" header at the top of the page to select all students, and click on the "Submit" button. Then click on the "Download Assignments now" hyperlink. This will create a gradebook_.... .zip file in your Downloads directory.  Move from your Downloads directory to the subdirectory where you want to work on the assignment, and run the degrade.py script in that directory.

degrade.py will...

- Read the first gradebook_\*.zip file in the current directory

- Extract student submission info from the zip file and put it in ./sdoc/<student_name>/submission.txt

- Extract any submitted files from the student and put them in ./submissions/<student_name>/ If there are any .zip files, unzip these files in ./submissions/<student_name>

- Details (with time/date stamp) are appended to degrade_log.txt file in the current directory

- The gradebook_\*.zip file that has been processed will be deleted
