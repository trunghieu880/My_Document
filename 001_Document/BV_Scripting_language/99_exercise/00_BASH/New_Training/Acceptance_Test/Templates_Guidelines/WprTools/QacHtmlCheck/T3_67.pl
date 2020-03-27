#!/bin/perl -s

use strict;

#T3_67.pl -msn=<MSN> -family=<Family> -f=<filename> -iheader -checkdup -path 

if( !$::msn || !$::family || !$::f){
	print "T3_67.pl -msn=<MSN> -family=<Family> -f=<filename> -iheader -checkdup -path=<QAC output folder>";
	print "\t<MSN>: Module, Ex adc\n";
	print "\t<Family>: P1x-C, P1x-E, F1x\n";
	print "\tfilename: QAC output file, Ex Adc.c.txt or Adc.c.html\n";
	print "\tiheader: Ignore header file in checking MSG without START,END\n";
	print "\tcheckdup: Remove duplicate NG point\n";
	print "\t<QAC output folder>: QAC output folder path (optional)\n";	
	exit;
}

#Get required options
my $file = $::f;
my $module = lc($::msn);

#Get optional option
my $g_ignore_header = $::iheader;

#Global variables
# START information
my @g_all_start_msg;
my @g_all_start_num;
my @g_all_start_src_num;
my @g_all_end_num;
my @g_all_start_end_msg_ng; #Number of NG in checking START, END without MSG

# Unjustified message
my @g_unjustified_line;
my @g_unjustified_msg;

#Common pattern
my $g_pat_start = "[sS][tT][aA][rR][tT][\t ]*Msg[\t ]*";
my $g_pat_end = "[eE][nN][dD][\t ]*Msg[\t ]*";
my $g_pat_msg = "[mM][sS][gG][\t ]*";
my $g_pat_tool_msg = "";

#config values
my $g_family;
if( $::family =~ /P1[a-zA-Z]-E/){
	$g_family = "P1x-E";
}elsif ( $::family =~ /P1[a-zA-Z]-C/){
	$g_family = "P1x-C";
}elsif ( $::family =~ /F1[a-zA-Z]/){
	$g_family = "F1x";
}elsif ( $::family =~ /P1[a-zA-Z]/){
	$g_family = "P1x";
}

#
my $g_checkdup = $::checkdup;

#html or txt
my $g_html = 0;

##
if( $file =~ /.c.html/ ){
	$g_pat_tool_msg = ":[\t ]*[mM][sS][gG][\t ]*";
	$g_html = 1;
}elsif ( $file =~ /.c.txt/ ){
	$g_pat_tool_msg = "^[mM][sS][gG][\t ]*";
}else{
	print "\tInvalid QAC output file\n";
	exit;
}

my $g_get_start = 1;
#
my $qac_folder;
if($::path eq "")
{
	#U:\internal\X1X\P1x-E\modules\spi\test_static\qac\4.0.3
	$qac_folder = "U:\\internal\\X1X\\$g_family\\modules\\$module\\test_static\\qac";
}else{
	$qac_folder = $::path;
}
#print "DBG1\tQAC output folder:$qac_folder\n";

my $cmd = "dir /s /b $qac_folder\\*$file";
print "CMD: $cmd\n";
my @all_file = `$cmd`;

my $num_file = 0;
foreach my $file (@all_file){
	chomp($file);
	$file =~ s/\//\\/g;	
	#print "DBG1\t $file\n";
	print "*******************************\n";
	print "Query file $file\n";
	
	
	&ProcessQACFile($file, $g_get_start);
	print "\n";
	
	if( $g_get_start){	
		$g_get_start = 0;	#only get at the first time
	}
	#
	$num_file++;
}

#Query all QAC files
print "*******************************\n";
print "Query file all $num_file QAC file $file\n";

#Report result of checking START,END without MSG
my $idx = 0;
my $size = @g_all_start_msg;
my $found_size = @g_all_start_end_msg_ng;
if($found_size > $size)
{
	#Error handling
	print "TOOL BUGGGGGGGGGGGGGG\n";
	exit;
}

while( $idx < $size)
{
	my $start_line = $g_all_start_msg[$idx];
	my $start_num = $g_all_start_num[$idx];
	my $pattern = $start_line;
	$pattern =~ /\d+:\d+/;
	$pattern = $&;
	#
	if($g_all_start_end_msg_ng[$idx] == $num_file ) #START,END without MSG NG occurs all QAC files
	{
		if( $g_html){
			my $src_num = $g_all_start_src_num[$idx];
			print "NG\tSTART,END without MSG (a redundant justification)> Line: $src_num, Msg\($pattern\)\n";
		}else{
			print "NG\tSTART,END without MSG (a redundant justification)> Msg\($pattern\), log line: $start_num\n";
		}
	}elsif ($g_all_start_end_msg_ng[$idx] > $num_file )
	{
		#Error handling
		print "TOOL BUGGGGGGGGGGGGGG\n";
		exit;
	}
	#
	$idx++;
}

sub ProcessQACFile {
	my($qac_file, $get_start) = @_;
		
	#Get all MSG
	my @all_msg_line;
	my @all_msg_num;
	my @all_src_num;
	my @all_justify;

	open( MYFILE, $qac_file );
	my $line = <MYFILE>;
	my $num = 0;
	while( $line ne "")
	{
		$num++;
		if(($line =~ /$g_pat_msg\([0-9]:[0-9]+\)/) 
		&& ($line !~ /Message[\t ]*:/) ) #execlude /* Message       : Msg(4:0303)*/
		{
			if( $g_html ){
				my $src_num = $line;
				if( $src_num =~ /^[\t ]*[0-9]+:/){
					$src_num =~ /[0-9]+:/;
					$src_num = $&;
				}else{
					$src_num = "";
				}			
				push @all_src_num, $src_num;
				#print "DBG2\tsrc num: $src_num, log num:$num,:$line";		
			}else{
				#print "DBG2\tlog num: $num:$line";		
			}
			push @all_msg_line, $line;
			push @all_msg_num, $num;		
		}elsif ($line =~ /Message[\t ]*:[\t ]*\([0-9]:[0-9]+\)/)
		{
			$line =~/[0-9]:[0-9]+/;
			$line =$&;
			#print "DBG7\tjustify=$line\n";
			push @all_justify,$line;
		}elsif ($line =~ /Message[\t ]*:[\t ]*Msg\([0-9]:[0-9]+\)/)	
		#/* Message       : Msg(4:0303) [I] Cast between a pointer to volatile         */
		{
			$line =~/[0-9]:[0-9]+/;
			$line =$&;
			#print "DBG7\tjustify=$line\n";
			push @all_justify,$line;
		}
		$line = <MYFILE>;
	}
	close (MYFILE);

	#Get all START msg
	my @all_start_msg;
	my @all_start_num;
	my @all_start_src_num;
	my @all_end_num;

	my $idx = 0;
	my $size = @all_msg_line;
	while( $idx < $size)
	{
		$line = $all_msg_line[$idx];
		$num = $all_msg_num[$idx];
		#print "DBG3\tidx=$idx,$num:$line";
		
		#/* START Msg(4:0310)-1  */
		#/* QAC Warning START Msg(2:3211)-1 */
		#/* QAC Warning: START Msg(2:2824)-1 */
		#/* MISRA Violation: START Msg(4:0491)-9 */
		#/* MISRA Violation: START Msg(4:2842)- 5 */
		#/*MISRA Violation : START Msg(4:4454)-11 */
		if( ($line =~ /\/\*\s*$g_pat_start\(\d+:\d+\)-\d+\s*\*/) 
		||
		($line =~ /\/\*\s*[qQ][aA][cC]\s*\w+\s*[:]*\s*$g_pat_start\(\d+:\d+\)-\d+\s*\*\//) 
		||
		($line =~ /\/\*\s*[mM][iI][sS][rR][aA]\s*\w+\s*[:]*\s*$g_pat_start\(\d+:\d+\)-\s*\d+\s*\*\//)
		){
			#print "DBG3\tidx=$idx,$num:$line";
			push @all_start_msg, $line;
			push @all_start_num, $num;
			push @all_end_num,0;
			if($get_start){
				push @g_all_start_msg, $line;
				push @g_all_start_num, $num;
				push @g_all_end_num,0;
			}
			if( $g_html ){
				my $src_num = $all_src_num[$idx];
				push @all_start_src_num, $src_num;
				if($get_start){
					push @g_all_start_src_num, $src_num;
				}
			}
		}
		$idx++;
	}

	#Check START END for first log
	#if( $get_start ){
		print "-----Check START without END or invalid END------\n";
		$idx = 0;
		$size = @all_start_msg;
		while( $idx < $size)
		{
			my $start_line = $all_start_msg[$idx];
			my $start_num = $all_start_num[$idx];
			my $pattern = $start_line;
			$pattern =~ /[0-9]:[0-9]+/;
			$pattern = $&;
			#print "DBG4\t $start_num:$pattern\n";
			#
			my $seek_idx = 0;
			my $seek_size = @all_msg_line;
			my $found = 0;
			while( $seek_idx < $seek_size &&
				   $found == 0)
			{
				if( $all_msg_num[$seek_idx] == $start_num)
				{
					$found = 1;
					#print "DBG4\t seek_idx=$seek_idx, num = $all_msg_num[$seek_idx]";
				}
				$seek_idx++;
			}
			#
			$all_end_num[$idx] = 0;
			#print "DBG4\t ************\n";
			while( $seek_idx < $seek_size)
			{
				$line = $all_msg_line[$seek_idx];
				my $end_num = $all_msg_num[$seek_idx];
				#print "DBG4\tSEEK\t end_num=$end_num:$line";

				if($line =~ /$g_pat_start\($pattern\)-[0-9]*/) #Found the next same START
				{
					$seek_idx = $seek_size; #
				}elsif( $line =~ /$g_pat_end\($pattern\)-[0-9]*/) #Found END
				{
					$all_end_num[$idx] = $end_num;
					#print "DBG4\t Found START,END line:$start_num,$end_num:$start_line";
					$seek_idx = $seek_size;
				}
				$seek_idx++;
			}
			
			if( $all_end_num[$idx] == 0 && $get_start)
			{
				#print "DBG4\t Not Found START,END line:$start_num:$start_line";
				if( $g_html){
					my $src_num = $all_start_src_num[$idx];
					print "NG\t START without END> Line: $src_num, Msg\($pattern\)\n";
				}else{
					print "NG\t START without END> Msg\($pattern\), log line: $start_num\n";
				}		
			}
			
			$g_all_end_num[$idx] = $all_end_num[$idx];
			#
			$idx++;
		}
		print "------------------------------\n";
	#}	

	#Check START,MSG,END
	$idx = 0;
	$size = @all_start_msg;
	my @all_start_found;

	while( $idx < $size)
	{
		push @all_start_found, 0;
		if($get_start){
			push @g_all_start_end_msg_ng, 0;	#Assump no NG at the first log
		}
		
		my $start_line = $all_start_msg[$idx];
		my $start_num = $all_start_num[$idx];
		my $pattern = $start_line;
		$pattern =~ /[0-9]:[0-9]+/;
		$pattern = $&;
		#
		my $seek_idx = 0;
		my $seek_size = @all_msg_line;
		my $found = 0;
		while( $seek_idx < $seek_size &&
			   $found == 0)
		{
			if( $all_msg_num[$seek_idx] == $start_num)
			{
				$found = 1;
			}
			$seek_idx++;
		}
		#
		my $end_num = $all_end_num[$idx];
		#print "DBG5\t DEGGGGGGstart=$start_num,end=$end_num\n";
		$found = 0;
		my $num = 0;
		while($seek_idx < $seek_size && $found == 0
			&& $num < $end_num)
		{
			$line = $all_msg_line[$seek_idx];
			$num = $all_msg_num[$seek_idx];
			if( $line =~ /$g_pat_tool_msg\($pattern\)/)
			{
				$all_start_found[$idx] = 1;
				#print "DBG5\tFound Msg ($num),$start_num,$end_num:$start_line";
				$found  = 1;
			}
			$seek_idx++;
		}
		if($all_start_found[$idx] == 0 )
		{
			if( $g_html){
				my $src_num = $all_start_src_num[$idx];
				#print "DBG5\tSTART,END without MSG,pattern:\($pattern\), source line: $src_num, log line:$start_num\n";
			}else{
				#print "DBG5\tSTART,END without MSG,pattern:\($pattern\),log line:$start_num\n";
			}
			$g_all_start_end_msg_ng[$idx]++;			
		}
		
		#
		$idx++;
	}

	#Chek MSG without START,END 
	$idx = 0;
	$size = @all_msg_line;
	while($idx < $size)
	{
		my $msg_line = $all_msg_line[$idx];
		my $msg_num = $all_msg_num[$idx];
		if($msg_line =~ /$g_pat_tool_msg\([0-9]:[0-9]+\)/)
		{
			if($g_html &&
			   $msg_line =~ /\w+.h\([0-9]+,[0-9]+\)/ && 
			   $g_ignore_header ){
			   #ignore header file
			}else{
			
				#print "DBG6\t$msg_num:$msg_line";
				my $pattern = $msg_line;
				$pattern =~ /[0-9]:[0-9]*/;
				$pattern = $&;
				
				#Seek START and END
				my $found_start = 0;
				my $found_end = 0;
				
				#Seek START
				my $seek_idx = $idx-1;
				my $seek_start = 0;
				my $seek_end = 0;
				while($seek_idx > 0 && 
					$seek_start ==0 && 
					$seek_end == 0)
				{
					$line = $all_msg_line[$seek_idx];
					$num = $all_msg_num[$seek_idx];
					if($line =~ /$g_pat_end\($pattern\)/)
					{
						$seek_end = 1;
					}elsif ($line =~ /$g_pat_start\($pattern\)/)
					{
						$seek_start = 1;
					}
					$seek_idx--;
				}
				$found_start = $seek_start;
				
				#Seek END 
				$seek_idx = $idx+1;
				my $seek_start=0;
				my $seek_end=0;
				my $seek_size=@all_msg_line;
				while($seek_idx < $seek_size && 
					$seek_start ==0 && 
					$seek_end == 0)
				{
					$line = $all_msg_line[$seek_idx];
					$num = $all_msg_num[$seek_idx];
					if($line =~ /$g_pat_end\($pattern\)/)
					{
						$seek_end = 1;
					}elsif ($line =~ /$g_pat_start\($pattern\)/)
					{
						$seek_start = 1;
					}
					$seek_idx++;
				}
				
				$found_end = $seek_end;
				
				if($found_start == 0  && $found_end == 0 )
				{
					#print "DBG6\tMSG without START or END,line:$msg_num:$msg_line";
					if( $g_html ){
						my $src_info = $msg_line;
						$src_info =~ /\w+.[hc]\([0-9]+,[0-9]+\)/;
						$src_info = $&;
						my $src_file = $src_info;
						$src_file =~ /\w+.[hc]/;
						$src_file = $&;
						my $src_num = $src_info;				
						$src_num =~ /\([0-9]+,[0-9]+\)/;
						$src_num = $&;
						$src_num =~ /[0-9]+/;
						$src_num = $&;
						
						if($g_checkdup)
						{
							my $unjustified_count = @g_unjustified_line;
							my $unjustifed_idx=0;
							my $unjustifed_add=0;
							while( $unjustifed_idx < $unjustified_count && $unjustifed_add == 0)
							{
								if( $src_num eq $g_unjustified_line[$unjustifed_idx] &&
								$pattern eq $g_unjustified_msg[$unjustifed_idx] )
								{
									$unjustifed_add = 1; #Found violation was seen before
								}
								$unjustifed_idx++;
							}							
								
							if( !$unjustifed_add)
							{
								push @g_unjustified_line, $src_num;
								push @g_unjustified_msg, $pattern;
								print "NG\tMSG without START,END (unjustification)> log line: $msg_num, File: $src_file > Line: $src_num, Msg\($pattern\)\n"
							}
						}else{
							print "NG\tMSG without START,END (unjustification)> log line: $msg_num, File: $src_file > Line: $src_num, Msg\($pattern\)\n";				
						}						
					}else {
						print "NG\tMSG without START,END (unjustification)> Msg\($pattern\), log line: $msg_num\n";					
					}			
				}	
			}
		}
		$idx++;
	}

	#Check consistent
	$idx = 0;
	$size = @all_start_msg;
	while($idx < $size)
	{
		my $msg_line = $all_start_msg[$idx];
		my $msg_num = $all_msg_num[$idx];
		#
		my $seek_size = @all_justify;
		my $seek_idx = 0;
		my $found = 0;
		
		#print "DBG8\t$msg_line";
		while($seek_idx < $seek_size &&  $found == 0)
		{
			my $justify = $all_justify[$seek_idx];
			#print "\t Justified: $justify\n";
			#print "\t Msg line: $msg_line\n";
			if($msg_line =~ /$justify/)
			{
				$found = 1;
			}
			$seek_idx++;
		}
		if($found == 0){
			print "NG\tThe justified id is not described at the top of file> Log line:$msg_num, justified id: $msg_line";
		}
		#
		$idx++;
	}

	my $seek_size = @all_justify;
	my $seek_idx = 0;
	$size = @all_start_msg;
	while($seek_idx < $seek_size)
	{
		my $justify = $all_justify[$seek_idx];
		$idx = 0;
		my $found = 0;
		while($idx < $size && $found == 0)
		{
			my $msg_line = $all_start_msg[$idx];
			#print "DBG8\t$msg_line";
			if($msg_line =~ /$justify/)
			{
				$found = 1;
			}
			$idx++;
		}
		if($found == 0){
			print "NG\tRedundant justified id at the top of file> Justified id: $justify\n";
		}
		$seek_idx++;
	}
}
