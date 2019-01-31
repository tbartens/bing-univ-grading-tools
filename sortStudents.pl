#! /usr/bin/perl

use strict;

# stdin has student names, separated by _
# stdot prints these sorted by last name

my @orig=<>;
my @sorted=sort { compName($a,$b) } @orig;
foreach my $name (@sorted) {
	printf $name;
}

sub compName {
	my $a=shift;
	my $b=shift;
	my $a=lastName($a);
	my $b=lastName($b);
	return $a cmp $b;
}

sub lastName {
	my $n=shift;
	chomp($n);
	$n=~s/\s.*$//g; # Throw away everything from first white space to the end of the line
	my @ns=split('_',$n);
	my $ln=$ns[-1];
	if ($ln eq "III") { $ln=$ns[-2]; }
	if ($ns[-2] eq "St") { $ln=$ns[-2].'_'.$ns[-1]; } # Handle St_Pierre
	return $ln;
}
	