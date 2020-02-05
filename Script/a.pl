#!/bin/perl

my $temp_path = "/c/Users/hieu.nguyen-trung/Desktop/Material/MYOUTPUT";

for my $file (`find $temp_path`){
    chomp($file);
    my $f_name = `basename $file`;
    chomp($f_name);
    if ("$f_name" eq "sed_ex_3"){
        printf("%s\n", $file);
        printf("%d\n", length($file));
    }

}
