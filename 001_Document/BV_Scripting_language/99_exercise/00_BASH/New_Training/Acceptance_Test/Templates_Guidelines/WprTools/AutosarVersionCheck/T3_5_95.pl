#!/bin/perl -s
#T3_5_95.pl -m=<msn> -family=<Family>
#example T3_5_95.pl -m=mcu -family=F1x

if(!$m || !$family)
{
	print "T3_5_95.pl -m=<msn> -family=<Family> \n";
	print "\t<msn> Module Name, Ex: adc\n";
	print "\t<Family>, Ex:F1x , P1x \n";
	exit;
}


$variant = $family;
$module = ucfirst(lc($m));
$version_check;

$file;
$line;
$pattern = "[0-9]-[0-9]-[0-9]";
print "------------------------------------------Check 3.5----------------------------------\n";
$dir = 'U:\external\X1X\common_platform\generic\stubs';
$cmd = "where /R $dir *$module*.arxml";
#$dir = 'U:\external\X1X/common_platform/generic/stubs/';
#$cmd = "find $dir  -name *$module*.arxml";
#print "$cmd/n";
@search_log = `$cmd`;
foreach $log (@search_log)
{
	$file = $log;
	if ($log =~ /[0-9].[0-9].[0-9]/)
	{
		$version_check = $&;
	}
	if ($version_check eq "4.0.3")
	{
		$version = "4-0-3";
	}
	elsif ($version_check eq "4.2.2")
	{
		$version = "4-2-2";
	}
	else
	{
		$version = "3-2-2";
	}	
	if ($module ne "")
	{
		open (FILE, $file);
		while ($line = <FILE>)
		{
			if ($line =~ /AUTOSAR_$pattern.xsd/)
			{
				$line =~ /[0-9]-[0-9]-[0-9]/;
				$found_pattern = $&;
				print "File: $file, Version = $found_pattern \n";
				if ($found_pattern eq $version)
				{
					print "Recommend Adjustion: OK\n";
				}
				else
				{
					print "Recommend Adjustion: NG \n";
				}
			}
		}
		close(FILE);
	}
}
$dir = "U:\\external\\X1X\\".$variant."\\common_family\\config\\";
$cmd = "where /R $dir *$module*.arxml";

#$dir = 'U:/external/X1X/F1x/common_family/config/';
#$dir = "U:/external/X1X/".$variant."/common_family/config/";
#$cmd = "find $dir  -name *$module*.arxml";
#print "$cmd/n";
@search_log = `$cmd`;
foreach $log (@search_log)
{
	$file = $log;
	if ($log =~ /[0-9].[0-9].[0-9]/)
	{
		$version_check = $&;
	}
	if ($version_check eq "4.0.3")
	{
		$version = "4-0-3";
	}
	elsif ($version_check eq "4.2.2")
	{
		$version = "4-2-2";
	}
	else
	{
		$version = "3-2-2";
	}	
	if ($module ne "")
	{
		open (FILE, $file);
		while ($line = <FILE>)
		{
			if ($line =~ /AUTOSAR_$pattern.xsd/)
			{
				$line =~ /[0-9]-[0-9]-[0-9]/;
				$found_pattern = $&;
				print "File: $file, Version = $found_pattern \n";
				if ($found_pattern eq $version)
				{
					print "Recommend Adjustion: OK\n";
				}
				else
				{
					print "Recommend Adjustion: NG \n";
				}
			}
		}
		close(FILE);
	}
}

# $temp_module = $module;
# $module = uc($module);
# $dir = 'U:/external/X1X/common_platform/generic/stubs/';
# $cmd = "find $dir  -name *$module*.arxml";
# #print "$cmd/n";
# @search_log = `$cmd`;
# foreach $log (@search_log)
# {
	# $file = $log;
	# if ($log =~ /[0-9].[0-9].[0-9]/)
	# {
		# $version_check = $&;
	# }
	# if ($version_check eq "4.0.3")
	# {
		# $version = "4-0-3";
	# }
	# elsif ($version_check eq "4.2.2")
	# {
		# $version = "4-2-2";
	# }
	# else
	# {
		# $version = "3-2-2";
	# }	
	# if ($module ne "")
	# {
		# open (FILE, $file);
		# while ($line = <FILE>)
		# {
			# if ($line =~ /AUTOSAR_$pattern.xsd/)
			# {
				# $line =~ /[0-9]-[0-9]-[0-9]/;
				# $found_pattern = $&;
				# print "File: $file, Version = $found_pattern \n";
				# if ($found_pattern eq $version)
				# {
					# print "Recommend Adjustion: OK\n";
				# }
				# else
				# {
					# print "Recommend Adjustion: NG \n";
				# }
			# }
		# }
		# close(FILE);
	# }
# }

# $dir = "U:/external/X1X/".$variant."/common_family/config/";
# $cmd = "find $dir  -name *$module*.arxml";
# #print "$cmd/n";
# @search_log = `$cmd`;
# foreach $log (@search_log)
# {
	# $file = $log;
	# if ($log =~ /[0-9].[0-9].[0-9]/)
	# {
		# $version_check = $&;
	# }
	# if ($version_check eq "4.0.3")
	# {
		# $version = "4-0-3";
	# }
	# elsif ($version_check eq "4.2.2")
	# {
		# $version = "4-2-2";
	# }
	# else
	# {
		# $version = "3-2-2";
	# }	
	# if ($module ne "")
	# {
		# open (FILE, $file);
		# while ($line = <FILE>)
		# {
			# if ($line =~ /AUTOSAR_$pattern.xsd/)
			# {
				# $line =~ /[0-9]-[0-9]-[0-9]/;
				# $found_pattern = $&;
				# print "File: $file, Version = $found_pattern \n";
				# if ($found_pattern eq $version)
				# {
					# print "Recommend Adjustion: OK\n";
				# }
				# else
				# {
					# print "Recommend Adjustion: NG \n";
				# }
			# }
		# }
		# close(FILE);
	# }
# }

print "------------------------------------------Check 3.95----------------------------------\n";

#$module = $temp_module;
$dir = "U:\\internal\\X1X\\".$variant."\\common_family\\config\\";
$cmd = "where /R $dir *$module*.arxml";
#$dir = "U:/internal/X1X/".$variant."/common_family/config/";
#$cmd = "find $dir  -name *$module*.arxml";
#print "$cmd/n";
@search_log = `$cmd`;
foreach $log (@search_log)
{
	$file = $log;
	if ($log =~ /[0-9].[0-9].[0-9]/)
	{
		$version_check = $&;
	}
	if ($version_check eq "4.0.3")
	{
		$version = "4-0-3";
	}
	elsif ($version_check eq "4.2.2")
	{
		$version = "4-2-2";
	}
	else
	{
		$version = "3-2-2";
	}	
	if ($module ne "")
	{
		open (FILE, $file);
		while ($line = <FILE>)
		{
			if ($line =~ /AUTOSAR_$pattern.xsd/)
			{
				$line =~ /[0-9]-[0-9]-[0-9]/;
				$found_pattern = $&;
				print "File: $file, Version = $found_pattern \n";
				if ($found_pattern eq $version)
				{
					print "Recommend Adjustion: OK\n";
				}
				else
				{
					print "Recommend Adjustion: NG \n";
				}
			}
		}
		close(FILE);
	}
}

# $module = uc($module);
# $cmd = "find $dir  -name *$module*.arxml";
# #print "$cmd/n";
# @search_log = `$cmd`;
# foreach $log (@search_log)
# {
	# $file = $log;
	# if ($log =~ /[0-9].[0-9].[0-9]/)
	# {
		# $version_check = $&;
	# }
	# if ($version_check eq "4.0.3")
	# {
		# $version = "4-0-3";
	# }
	# elsif ($version_check eq "4.2.2")
	# {
		# $version = "4-2-2";
	# }
	# else
	# {
		# $version = "3-2-2";
	# }	
	# if ($module ne "")
	# {
		# open (FILE, $file);
		# while ($line = <FILE>)
		# {
			# if ($line =~ /AUTOSAR_$pattern.xsd/)
			# {
				# $line =~ /[0-9]-[0-9]-[0-9]/;
				# $found_pattern = $&;
				# print "File: $file, Version = $found_pattern \n";
				# if ($found_pattern eq $version)
				# {
					# print "Recommend Adjustion: OK\n";
				# }
				# else
				# {
					# print "Recommend Adjustion: NG \n";
				# }
			# }
		# }
		# close(FILE);
	# }
# }