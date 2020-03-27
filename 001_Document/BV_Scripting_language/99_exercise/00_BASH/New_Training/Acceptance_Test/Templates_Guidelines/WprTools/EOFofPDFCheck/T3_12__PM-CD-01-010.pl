#!/usr/bin/perl -s
# @filename:     PM-CD-01-010.pl
# @author:       Anh Trinh
# @release date: 05-Jul-2017
# @description:  Checking if there is 'EOF' at the head of the last line in 
# Parameter Definition File



################################################################################
# MAIN PROGRAM 
################################################################################
use strict;
use File::Basename;
use Text::Wrap;
use Win32::OLE qw(in with);
# use Win32::OLE::Const 'Microsoft Word';
# use Win32::OLE::Const 'Microsoft Excel';

my $g_msn = $::msn;
my $g_family = $::family;
my $g_cmd = "call cls";
my $g_all = $::all;
my $G_LOG;
my $g_debug=$::debug;
my $g_total=0;

if ((!$g_msn && !$g_all) || !$g_family) {
    goto HELP;
}

(my $file_title = basename($0)) =~ s/\.[^.]+$//;

# Select log direction is to log file or terminal
open ($G_LOG, ">", $file_title."_log.csv") or die "$!";
$G_LOG->autoflush(1);
if ($g_debug) {
  select $G_LOG;
} else {
  select STDOUT;
}


# print "Module,\tPerameter Definition Files\n";

if($g_msn) {
    &RetrievePDF($g_msn);
}elsif($g_all) {
    my $folder = "U:\\external\\X1X\\$g_family\\modules";
    my $cmd = "dir /b $folder";
    my @all_msn = `$cmd`; 
    # my @all_msn = split(" ", $ls_result);

    foreach my $l_msn (in @all_msn) {
        print "module: $l_msn\n";
        chomp $l_msn;
        &RetrievePDF($l_msn);
    }
}

close $G_LOG;

# Summary report
print "\n+++++++++++++++++++++++++++++ SUMMARY ++++++++++++++++++++++++++++++++\n";
if ($g_total == 0) {
  print "\t\t\tNo violation found\n";
}
else {
  print "\t\t\tTotal: $g_total NG found\n";
}
print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"; 
# End of main
exit;

################################################################################
# SUBROUTINES DEFINITIONS
################################################################################


################################################################################
# Sub routine for retrieve all of PDFs of a module 
sub RetrievePDF{
    my($module) = @_;
    my $module_lc = lc($module);
    my $module_uc = uc($module);
    my $PDF_PATH = "U:\\external\\X1X\\$g_family\\modules\\$module_lc\\definition\\";
    
    if (!(-e $PDF_PATH)){ 
      print "ERROR\t Definition folder not found \n";
      return;
    }

    $g_cmd = "dir /s /b $PDF_PATH*.arxml";
    my @pdf_files_path = `$g_cmd`;
    # List PDF
    foreach my $file (in @pdf_files_path) {
      # print "$file \n";
      if (CheckEOF($file) == 0){
          # OK
      } else {
          # NG
          print "$module_uc,\t$file";
          $g_total++;
      }
    }
    
}
################################################################################
# Sub routine for checking EOF in PDF

sub CheckEOF{
    my($file) = @_;
    my $line;

    open (MYFILE, $file) || die "ERROR Unable to open: $!\n" ;
    # $line = <MYFILE>;
    my @lines_arr = <MYFILE>;
            
    close (MYFILE);

    my $last_line = pop(@lines_arr);
    if ($last_line =~ /.[\r|\n]$/) {
        # print "Found EOF\n";
        return 0;
    } else {
        # print "last_line:". $last_line;
        return 1;
    }
    return 0;
}


HELP:
print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n";
print "                             HOW TO RUN:\n";
print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n";
print "Usage:\n\n";
print "+ Step 1:\n";
print "\t". basename($0) . " -msn=<MSN> -all -family=<FAMILY_NAME>\n";
print "\t\t<MSN>         - [REQUIRED] Module short name. E.g. adc, dio, gpt,...\n";
print "\t\t-all          - [OPTIONAL] For retrieving all of modules\n";
print "\t\t<FAMILY_NAME> - [REQUIRED] Family name. E.g. F1x, P1x-C, P1x, ...\n";
print "\t\t-debug        - [OPTIONAL] If you want to show result to log file\n";
print "+ Step 2:\n";
print "\tCheck the result in log file if use -debug".$::file_title.".\n";
print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n";

END:
# End of File.
