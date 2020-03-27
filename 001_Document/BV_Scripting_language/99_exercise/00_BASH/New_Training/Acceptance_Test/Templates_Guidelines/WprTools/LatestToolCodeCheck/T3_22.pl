#!/bin/perl -s
use Term::ANSIColor;

#T3_22.pl -m=<msn> -f=<family>
if( !$m or !$f)
{
	print "T3_22.pl -m=<msn> -f=<family>\n";
	print "\t<msn> module, Ex: adc \n";
	print "\t<family> family, Ex: F1x";
	exit;
}

$family = $f;
$module = $m;
$module = lc($module);
$module = ucfirst($module);

$ROOT = "..";
$checkRUCG = "find $ROOT/external/tools -name RUCG.exe";
@RUCGisAvailable = `$checkRUCG`;
if ($RUCGisAvailable[0])
{
	$RUCG = $ROOT."/external/tools/RUCG/RUCG.exe";
	#DLL path 
	$cmd = "find $ROOT/external -name $module*.dll";
	@all_dll = `$cmd`;
	$dll = $all_dll[0];
	chomp($dll);
	print "$dll\n";
	print("cp -f $dll tmp.dll\n");
	system("cp -f $dll tmp.dll\n");

	#
	$cmd = "$RUCG tmp.dll -F";
	@log =  `$cmd`;
	#
	system("rm -f tmp.dll\n");
}
else
{
	$TOOL = $ROOT."/external/X1X/common_platform/modules/".$module."/generator/".$module."_X1x.exe";
	print "Tool\t:$TOOL\n";

	$cmd = "$TOOL -F";
	@log =  `$cmd`;
}

$size = @log;
#print "DBG1t log size:$size\n";

#Search folder
#module: + U:\internal\X1X\P1x-E\modules\<msn>\generator
#module: + U:\internal\X1X\common_platform\modules\<msn>\generator
#generic: + U:\internal\X1X\common_platform\generic\generator
$generic_folder = $ROOT."/internal/X1X/common_platform/generic/generator";
$module = lc($module);
$module_folder_common = $ROOT."/internal/X1X/common_platform/modules/".$module."/generator";
$module_folder_family = $ROOT."/internal/X1X/".$family."/modules/".$module."/generator";

$idx = 0;
while ($idx < $size)
{
	$log_line = $log[$idx];
	if( $log_line =~ /[a-zA-Z0-9]*.p[lm][\t ]*[1-9].[0-9]*.[0-9]*/)
	{
		$file = $log_line;
		$version = $log_line;
		$file =~ /[a-zA-Z0-9]*.p[lm]/;
		$file = $&;
		print "$file\n";
		$version =~ /[1-9].[0-9]*.[0-9]*/;
		$version = $&;
		print "$version\n";
		
		#print "DBG1\tfile:$file\tversion:$version\n";
		
		#search file
		$found = 0;
		$file_found = "";
		#search in generic folder
		$cmd = "find $generic_folder -name $file";
		@search_log = `$cmd`;
		if( $search_log[0] =~ /$file/){
			$file_found = $search_log[0];
			chomp( $file_found);
			$found = 1;
			#print "DBG2\tFound $file in generic folder:$file_found\n";
		}
		
		$cmd = "find $module_folder_common -name $file";
		@search_log = `$cmd`;
		if ( $search_log[0] =~ /$file/){
			$file_found = $search_log[0];
			chomp( $file_found);
			$found = 1;
			#print "DBG2\tFound $file in generic folder:$file_found\n";
		}
		
		$cmd = "find $module_folder_family -name $file";
		@search_log = `$cmd`;
		if ( $search_log[0] =~ /$file/){
			$file_found = $search_log[0];
			chomp( $file_found);
			$found = 1;
			#print "DBG2\tFound $file in generic folder:$file_found\n";
		}
		
		if( $found == 0 ){
			print color ("red"), "NG\t cannot find $file report by GEN TOOL\n", color ("reset");
		}else{
			$last_version = "";
			open (MYFILE, $file_found);
			$line = <MYFILE>;
			while ( $line ne "")
			{
				if( $line =~ /#[\t ]*[0-9]+.[0-9]+.[0-9]+/)
				{
					#print "DBG3\t$line";
					$line =~ /[0-9]+.[0-9]+.[0-9]/; 
					$last_version = $&;
				}
				$line = <MYFILE>;
			}
			close(MYFILE);
			#
			if( $last_version eq ""){
				print color ("red"), "NG\tTool Code File $file doesn't have revision history\n", color ("reset");
			}else{
				if( $version !~ /$last_version/ ){
					print color ("red"), "NG\tThe Generation Tool is not build with Latest Tool Code Files:$file\t$version,latest:$last_version\n", color("reset");
				}else{
					print "OK\tThe Generation Tool is build with Latest Tool Code Files:$file\t$version,latest:$last_version\n";
				} 
			}
		}		
	}
	$idx++;
}
#
