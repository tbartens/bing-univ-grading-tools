#! /usr/bin/python3
import os
import sys
import subprocess
import csv
from argparse import ArgumentParser
from html.parser import HTMLParser

CLASS_NAME = "Binghamton-CS220-Spring-2019"  # GitHub Classroom Name
STUDENT_INFO_FILE = "students.csv" # Student info file : student name, student_id, student_github_id

NAME_IDX = 0
COMMENT_IDX = 9

def get_student_info():
  name_to_info_mapping = {}
  with open(STUDENT_INFO_FILE, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in (csv_reader):
      last_name = row[0]
      first_name = row[1]
      student_id = row[2]
      github_username = row[3]
      student_name=first_name.join("_").join(last_name);

      name_to_info_mapping[student_name] = [student_id, github_username]

  return name_to_info_mapping

#make a directory names after the assignment
#for each student, go through clone their repositories
def main():
  students_wo_githubs = []

  name_to_info_mapping = get_student_info()

  parser = ArgumentParser()
  parser.add_argument("assn_name", type=str, nargs=1)
  parser.add_argument("update_files", type=str, nargs= '+')

  # students_of_interest = []
  args = parser.parse_args()

  assn_name = args.assn_name
  update_files = args.update_files

  num_repos_updated = 0

  # for student_name in name_to_info_mapping:
  for student_name in name_to_info_mapping.keys() :
    bID = name_to_info_mapping[student_name][0]
    gitusername = name_to_info_mapping[student_name][1]
    userdir=sys.argv[1] + "-" + gitusername.replace("\n", "")
    if(name_to_info_mapping[student_name][1] != ""):
        # git@github.com:Binghamton-CS220-Spring-2019/HW-01.git
        retVal = os.system(f'git clone git@github.com:{CLASS_NAME}/{userdir}.git')
        #if the repo doesn't exist, continue
        if(retVal != 0):
        	continue
        for file in update_files:
        	os.system(f'cp {file} {sys.argv[1]}-{gitusername.strip()}')

        p = subprocess.run(["git", "add", "-A"], cwd = userdir)
        p = subprocess.run(["git", "commit", "-m" ,"Professor improving instructions"], cwd = userdir)
        p = subprocess.run(["git", "push"], cwd = userdir)
 
        num_repos_updated += 1
        
        os.system("rm -rf " + sys.argv[1] + "-" + gitusername.replace("\n", ""))
    else:
      students_wo_githubs.append(student_name)

  print(f'Successfully updated repos of {num_repos_updated} students out of a possible {len(name_to_info_mapping.keys())}.')
  print(f'{len(students_wo_githubs)} have no github username on file.')
  print(students_wo_githubs)

main()