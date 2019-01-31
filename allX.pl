#! /usr/bin/perl

use strict;

my $cmd=shift;

open(STU,"<students.txt") || die "Unable to open students.txt file";
my @stu=<STU>;
close(STU);
my $st=shift(@stu);
while($st) {
	chomp($st);
	printf "Run %s on student %s? ====>",$cmd,$st;
	my $answer=<>;
	chomp($answer);
	last if ($answer ne "");
	system($cmd." ".$st); 
	printf "Next ===>";	
	my $panswer=<>;
	chomp($panswer);
	next if ($panswer eq 'r'); # Repeat same student?
	last if ($panswer ne "");	
	open(DON,">> finished_students.txt");
	printf DON "%s\n",$st;
	close(DON);
	open(STU,">students.txt");
	print STU @stu;
	close(STU);
	$st=shift(@stu);
}
