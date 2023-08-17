#!/usr/bin/env perl
use strict;
use Getopt::Long;
use File::Basename qw(basename dirname);
use FindBin qw($Bin $Script);
use POSIX qw(strftime);
#########################################################################
# Author: XueRen,xueren@genome.cn
# Created Time: 2018年2月28日 星期一 14时48分58秒
#########################################################################
my ($fa,$cut_off,$output,$use);
my $ver="v1.0";
$use=<<USE;
#############################################################################################################

Description： It is used to count fa sequence for N50~N90
Version：$ver;
Parameters:
	
	-fa     fa 序列文件                            must be given ，可以是gz压缩格式。
	-cut    大于等于cut长度的序列进行N50分布统计   default 1,只填写数字，单位是bp  	
	-o      输出文件                               default is fa.N50.stat.txt (默认与输入文件路径一致)
	
#############################################################################################################	
USE
GetOptions(
	"fa=s" =>\$fa,
	"cut=i" =>\$cut_off,
	"o=s" =>\$output,
);
die "there is not enough parameters\n$use" unless $fa;

my $time=&TIME;
my $info=$time." - $Script - INFO - ";
my $erro=$time." - $Script - ERROR - ";
my $warn=$time." - $Script - WARNNING - ";

##############################################Main#########################################
print STDOUT "$info##检查输入参数并开始分析\n";
my $file=basename($fa);
if ($fa =~ /\.gz$/) {
    print STDOUT "$info##Fa文件是gz压缩格式\n";
    open IN,"gzip -dc $fa|" or die print STDERR "$erro##gz压缩文件Fa不能打开或者不存在\n";
}else {
    open IN,"$fa" or die print STDERR "$erro##Fa文件不能打开或者不存在\n";
}
my @len=();
my $t_len=0;
my $n_100=0;
my $n_2000=0;
my $len=0;
my $num=0;
my $GCnum=0;
$cut_off||=1;
while(my $line=<IN>)
{
   chomp($line);
   if($line=~/^>/)
   {
	  $num+=1;
      if($len>=$cut_off){$n_100++;}
      if($len>=2000){$n_2000++;}
      if($len>=$cut_off)
      {
         push @len,$len;
         $t_len+=$len;
      }
      $len=0;
   }
   else
   {
      $GCnum+= $line =~ tr/C/C/;
      $GCnum+= $line =~ tr/c/c/;
      $GCnum+= $line =~ tr/G/G/;
      $GCnum+= $line =~ tr/g/g/;
      $len+=length($line);
   }
}
if ($num==0){print STDERR "$erro##Fa文件格式错误，不存在>\n";die;}
if($len>=$cut_off){$n_100++;}
if($len>=2000){$n_2000++;}
if($len>=$cut_off)
{
   push @len,$len;
   $t_len+=$len;
}
close IN;
print "GC:\t$GCnum\n";
my $GC_P = ($GCnum/$t_len)*100;

my $out;
@len = sort {$b <=> $a} @len;
my $nn=10;
my $sum=0;
my %n50=();
my %l50=();
for(my $i=0;$i<=$#len;$i++)
{
   $sum+=$len[$i];
   while ($sum>=$t_len*$nn/100)
   {
      $n50{$nn}=$len[$i];
      $l50{$nn}=$i+1;
      $nn+=10;  
   }
   last if($nn == 100);
}

$out= "Fa file is: $file\n";
$out.= "Total_length: $t_len\n";
my $result1 = &commify($len[0]);
$out.= "max_length: $result1\n";
$out.= "min_length: $len[-1]\n";
$out.= "Total_number: $num\n";
$out.= "number>=2000bp: $n_2000\n";
$out.= "number>=$cut_off"."bp: $n_100\n";
$out.= "\nIgnore sequences less than $cut_off bp as follows:\n";
$out.= "############################\n";
$out.= "Item\tlength\tnumber\n";
$out.= "N90\t$n50{90}\t$l50{90}\n";
$out.= "N80\t$n50{80}\t$l50{80}\n";
$out.= "N70\t$n50{70}\t$l50{70}\n";
$out.= "N60\t$n50{60}\t$l50{60}\n";
my $result2 = &commify($n50{50});
$out.= "N50\t$result2\t$l50{50}\n";
$out.= "N40\t$n50{40}\t$l50{40}\n";
$out.= "N30\t$n50{30}\t$l50{30}\n";
$out.= "N20\t$n50{20}\t$l50{20}\n";
$out.= "N10\t$n50{10}\t$l50{10}\n";
$out.= "############################\n";
$out.= "GC content\t";
$out.= sprintf("%.2f", $GC_P);
$out.= "%\n";
print STDOUT "$info##统计结果为:\n\n$out\n";

#####检查输出文件
if ($output) {
   if (-d $output || $output=~/\/$/){
        if (! -d $output){&mysystem("mkdir -p $output");}
        $output="$output/fa.N50.stat.xls";
        print STDERR "$warn##输出填写参数为路径，输出文件为$output\n";
    }else{
        $output=~ s/\s+/_/g;
        my $dir=dirname($output);
        if (! -d $dir){&mysystem("mkdir -p $dir");}
        print STDOUT "$info##输出文件为$output\n";
    }
} else {
    my $dir=dirname($fa);
	print STDERR "$warn##输出文件未设置，默认输入文件目录下fa.N50.stat.xls\n";
	$output="$dir/fa.N50.stat.xls";
}

my $out_name=basename($output);
open OUT,">$output";
print OUT "$out";
print STDOUT "$info##分析结束\n";
#########################子函数######################
sub TIME{
	return strftime("%Y-%m-%d %H:%M:%S", localtime(time));
}

sub mysystem{
    my $cmd=shift;
    if(system($cmd)!=0){
        die print STDERR "$erro##'$cmd'没有完成\n" ;
    }
}
sub commify {
    my $num  = shift;
    my ($num_l,$num_r) = split /\./, $num;

    $num_l =~ s/(?<=\d)(?=(\d{3})+$)/,/g;
    my $tmp = reverse $num_r;
    $tmp =~ s/(?<=\d)(?=(\d{3})+$)/,/g;
    $num_r = reverse $tmp;

    return ($num_r eq "") ? $num_l : sprintf("%s.%s",$num_l,$num_r);
}
