#! /usr/bin/perl

use strict;
use File::Copy;
use Cwd;
use File::Basename;
use Term::ReadKey;

# Assumes you are currently in <name>-students directory, and that you have already run degrade.pl

my $profId='tbartens'; # <-------------- Please update with your GIT userid!

my $assignment = basename(getcwd());
if (! $assignment =~/_students$/) {
	die "Please run from <assignemnt>_students directory";
}
$assignment =~ s/_students$//; # Remove _students from assignment name

if ($assignment eq '') {
	die "Please run from <assignemnt>_students directory";
}

if (!-d 'sdoc') {
	die "Please download from myCourses and run degrade.pl before running gitStudents";
}

if (!-d 'submissions') {
	die "Please download from myCourses and run degrade.pl before running gitStudents";
}

open(STU,"<students.txt") || die "Unable to open students.txt file";
# students.txt file contains student name with underscores for blanks, followed by git userid

printf "Please enter the git password for $profId ---->";
ReadMode 'noecho';
my $profPwd = <STDIN>;
ReadMode 'original';
chomp($profPwd);
printf("\nThank you\n");


while(<STU>) {
	chomp();
	my ($student,$gitId) = $_=~ /^(\S+)\s+(\S+)\s*$/;
	if ($student eq '') {
		warn "Blank student name in students.txt ignored";
		next;
	}
	if (!-r "sdoc/$student/submission.txt") {
		warn "No student submission on myCourses for student $student assignment $assignment";
		next;
	}
	if ($gitId eq '') {
		warn "Student $student has a blank gitHub userid... skipping this student";
		next;
	}
	$gitId=~s/_/ /g; # Translate underscores to blanks to allow team names with blanks
	my $sdir="submissions/${assignment}-${gitId}";
	# Archive previous clones
	if (-d $sdir) {
		my $rev=1;
		while( -d "${sdir}_ver_$rev") { $rev++; }
		move($sdir,"${sdir}_ver_$rev");
	}
	
	# Next, extract the SHA1 hash code from the submission.txt file in sdoc...
	my $SHA1 = `grep \'<p>\' sdoc/${student}/submission.txt`;
	chomp($SHA1);
	$SHA1 =~ s/^.*\<p\>//;
	$SHA1 =~ s/\<\/p\>.*$//;
	printf "Student $student SHA1=$SHA1\n";
	
	
	# Now actually do the git clone
	#Actually, lets do a git fetch instead of git clone.
	# See https://stackoverflow.com/questions/14872486/retrieve-specific-commit-from-a-remote-git-repository/14872590
	
	system('cd submissions; git clone -v https://'.$profId.':'.$profPwd.'@github.com/Binghamton-CS140-B1-Fall-2018/'."${assignment}-${gitId}.git");
	system('cd $sdir; git reset --hard $SHA1');
	
}
	
		

close(STU);
printf "All students processing complete\n";