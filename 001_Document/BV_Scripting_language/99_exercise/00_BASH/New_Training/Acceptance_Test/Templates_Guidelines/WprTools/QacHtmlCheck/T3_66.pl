#!/usr/bin/perl -s
# @filename:     T3_66.pl
# @author:       Anh Trinh
# @release date: 21-Aug-2017
# @description:  Tool for check QAC lastest source code
#                 Revert QAC report to original source

# @Notes: 
# 1. Need show different between files (DONE)
# 2. Delete all source files in QAC folder before gen (DONE)
################################################################################
# MAIN PROGRAM 
################################################################################
use strict;
use File::Basename;
use Text::Wrap;
use Win32::OLE qw(in with);
# use Win32::OLE::Const 'Microsoft Word';
# use Win32::OLE::Const 'Microsoft Excel';
use URI::Escape;
use HTML::Entities;
use File::Compare;
use Text::Diff;

my $g_msn = $::msn;
my $g_family = $::family;
my $g_cmd = "call cls";
my $g_all = $::all;
my $g_total=0;

if ((!$g_msn && !$g_all) || !$g_family) {
    goto HELP;
}

(my $file_title = basename($0)) =~ s/\.[^.]+$//;

print "Please don't care 'File Not Found' message!!!\n";

if($g_msn) {
    &RetrieveQACConfig($g_msn);
}elsif($g_all) {
    # my $qac_dir = "U:\\internal\\X1X\\$g_family\\modules\\$g_msn\\test_static\\qac\\$g_ar\\$g_cfg\\output\\";
    my $folder = "U:\\external\\X1X\\$g_family\\modules";
    my $cmd = "dir /b $folder";
    my $ls_result = `$cmd`; 
    my @all_msn = split(/[\r|\n]/, $ls_result);

    # check for module
    foreach my $l_msn (in @all_msn) {
        print "--------------------->\tModule: $l_msn\t<--------------------\n";
        &RetrieveQACConfig($l_msn);
        # print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
    }
}

# close $G_LOG;

# Summary report
# print "\n+++++++++++++++++++++++++++++ SUMMARY ++++++++++++++++++++++++++++++++\n";
# if ($g_total == 0) {
#   print "\t\t\tNo violation found\n";
# }
# else {
#   print "\t\t\tTotal: $g_total NG found\n";
# }
# print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"; 
# End of main
print "DONE!!!\n";
print "\n==================================================================\n";
exit;

################################################################################
# SUBROUTINES DEFINITIONS
################################################################################


#===============================================================================
# Sub routine for retrieve all QAC config 
#
sub RetrieveQACConfig{
  my($module) = @_;
  my $module_lc = lc($module);
  my $module_uc = uc($module);
  # my $cfg_lc = lc($g_cfg);
  my $QAC_DIR = "U:\\internal\\X1X\\$g_family\\modules\\$module_lc\\test_static\\qac\\";
  my $DRIVER_SRC = "U:\\external\\X1X\\common_platform\\modules\\$module_lc\\src\\";
  my $MCU_DRIVER_SRC = "U:\\external\\X1X\\$g_family\\modules\\$module_lc\\src\\";

  print "\n==================================================================\n";
  print "Module: ", $module_uc, "\n";
  print "==================================================================\n";
  my $cmd = "dir /b $QAC_DIR";
  my $ls_result = `$cmd`; 
  my @all_ar_ver = split(/[\r|\n]/, $ls_result);
  # Retrieve all Autosar version
  foreach my $ar_ver (in @all_ar_ver) {
    print "+ [AR", $ar_ver, "]:\n";
    $cmd = "dir /b /ad $QAC_DIR\\$ar_ver\\"; # list only folder
    # print $cmd;
    $ls_result = `$cmd`;
    my @all_cfg = split(/[\r|\n]/, $ls_result);
    # print @all_cfg;
    # Retrieve all QAC config
    foreach my $cfg (in @all_cfg) {
      print ">>>>", $cfg, "\n";
      my $qac_dir = "$QAC_DIR\\$ar_ver\\$cfg\\output\\";
      &RetrieveQACReport($qac_dir);
      &CompareSource($module_lc, $qac_dir);
    }
  }

}

#===============================================================================
# Sub routine for retrieve all qac report files of a config
#
sub RetrieveQACReport{
    my($qac_dir) = @_;

    # check valid stubs or gsa path
    if ( !(-e $qac_dir)){ 
      print "ERROR\t Directory not found \n";
      return;
    }

    # Remove previous reverted source (*.c)
    # $g_cmd = "dir /s /b $qac_dir*.c";
    # my @files_path = `$g_cmd`;
    unlink glob "$qac_dir*.c";
    # foreach my $file_path (in @files_path) {
    #   # print $file_path;
    # }

    # Retrieve all file report in cfg
    $g_cmd = "dir /s /b $qac_dir*.c.html";
    my @files_path = `$g_cmd`;
    # print @files_path; #DEBUG
    foreach my $file_path (in @files_path) {
      # print $file_path;
      &Report2Source($file_path);
    }

}

#===============================================================================
# Sub routine for revert QAC report to original source files 
#
sub Report2Source{
  my($rpt_file) = @_;
  chomp $rpt_file;
  # Create source output
  (my $src_file = $rpt_file) =~ s/\.[^.]+$//;
  # print "\tReverting... ",$src_file,"\n";
  unless(open (SOURCE_FILE, '>'.$src_file)) {
    # Cannot create source file
    die "\nERROR Unable to create $src_file\n";
  }
  # Open QAC report file
  open (REPORT_FILE, $rpt_file) || die "\nERROR Unable to open: $!\n" ;
  my $rpt_line = <REPORT_FILE>;
  my $src_line = <REPORT_FILE>; 
  while ($rpt_line) {
    if ($rpt_line =~ /^[ ]*[0-9]+:[\t]*/) {
      # Remove line number
      ($src_line = $rpt_line) =~ s/^[ ]*[0-9]+:[\t]*//;
      # HTML entities decode
      &decode_entities($src_line);
      print SOURCE_FILE $src_line;
    }
    $rpt_line = <REPORT_FILE>;
  }          
  close (REPORT_FILE);
  close (SOURCE_FILE);
}

#===============================================================================
# Sub routine for compare reverted qac report files with original source files 
#
sub CompareSource{
  my($module_lc, $qac_dir) = @_;
  my $DRIVER_SRC = "U:\\external\\X1X\\common_platform\\modules\\$module_lc\\src\\";
  my $MCU_DRIVER_SRC = "U:\\external\\X1X\\$g_family\\modules\\$module_lc\\src\\";
  my $src_dir;
  my $cmd = "";
  # print $module_lc, "\n";
  # print $qac_dir, "\n";
  if ($module_lc eq "mcu") {
    $src_dir = $MCU_DRIVER_SRC;
  } 
  else {
    $src_dir = $DRIVER_SRC;
  }
  $cmd = "dir /b $src_dir*.c"; # list only folder
  # print $cmd;
  my $ls_result = `$cmd`;
  my @all_src_files = split(/[\r|\n]/, $ls_result);
  # print "\t", @all_src;
  # Retrieve all source files and compare with reverted QAC report
  foreach my $src_file (in @all_src_files) {
    my $cmp_results = File::Compare::compare_text("$src_dir\\$src_file", "$qac_dir\\$src_file");
    if (-1 == $cmp_results) {
      print "\t-->[", $src_file, "] isn't run by QAC\n";
    }
    elsif (1 == $cmp_results) {
      # print "\t$qac_dir$src_file.html\n"; 
      print "\t-->[", $src_file, "] is not lastest\n";
      if ($::debug) {
        my $diff_result = diff "$src_dir\\$src_file", "$qac_dir\\$src_file", {STYLE => "Table", CONTEXT => 0}; 
        print $diff_result, "\n";
      }
    }
  }

  $cmd = "dir /b $qac_dir*.c"; # list only folder
  # print $cmd;
  $ls_result = `$cmd`;
  @all_src_files = split(/[\r|\n]/, $ls_result);
  # Check QAC gen without source
  foreach my $qac_file (in @all_src_files) {
    my $file_size = -s "$qac_dir\\$qac_file";
    # print $file_size, "\n";
    if (0 == $file_size) {
      print "\t-->[", $qac_file, "] is gen without source\n";
    }
  }
}

HELP:
print "\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n";
print "                             HOW TO RUN:\n";
print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n";
print "Usage:\n\n";
print basename($0) . " -msn=<MSN> -all -family=<FAMILY_NAME> -debug\n";
print " <MSN>             - [Required] Module short name. E.g. adc, dio, gpt,...\n";
print " all               - [Optional] For retrieving all of modules\n";
print " <FAMILY_NAME>     - [Required] Family name. E.g. F1x, P1x-C, P1x,...\n";
print " debug             - [Optional] Enable to show file differences\n";
print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n";

END:
# End of File.
