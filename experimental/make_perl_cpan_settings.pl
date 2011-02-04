#!/usr/bin/perl

use strict;
use warnings;

use CPAN;

&help() unless($ARGV[0]);
use Data::Dumper;
sub p { print Dumper shift }


sub help {
    print <<__HELP;
  make_cpan_settings <ModuleName>

Example:
  make_cpan_settings Unicode::Japanese

__HELP
    exit;
}


sub get_distriute_uri{
    my ($mod)=@_;
    my $uri='';
    foreach my $site(@{$CPAN::Config->{urllist}}) {
	$uri=$site . 'authors/id/'.$mod->{RO}->{CPAN_FILE};
	last;
    }
    return $uri;
}


sub make_defines{
    my ($mod) = @_;
    my @filename=split(/\//,$mod->{RO}->{CPAN_FILE});
    my $progs1=$filename[@filename-1];
    my $progs1_dir=$progs1;
    $progs1_dir=~s/\.tar\.[bg]z2?$//;
    my $uri=get_distriute_uri($mod);
    my $pkg=$mod->{ID};
    $pkg=~ s/::/-/g;
    my $result= <<__END;
PROG1=$progs1
PROG1_DIR=$progs1_dir
PROG1_SITE=$uri
TARGET=perl584-$pkg.pkg
__END
    return $result;
}


# Main

my $mod = CPAN::Shell->expand('Module', $ARGV[0]);

unless($mod){
    print "\n'$ARGV[0]' is not found in CPAN module\n\n";
    print "Explain:\n";
    &help();
}

p $mod;
# p $CPAN::META;
my $pkg=$mod->{ID};
$pkg=~ s/::/-/g;
my $module_name=$pkg;
$pkg=~ tr/A-Z/a-z/;
my $pkgdir=$mod->{ID};
$pkgdir=~ s/::/\//g;
my $arch=`uname -p`;
chomp($arch);

my $vendor=$CPAN::META->instance("CPAN::Author", $mod->{RO}->{CPAN_USERID})->as_glimpse();
chomp($vendor);
$vendor=~s/^.*?\((.+?)\).*?$/$1/;
$vendor=~s/\"//g;

my $logname=`logname`;
chomp($logname);

my $userid=$mod->{RO}->{CPAN_USERID};
$userid=~ tr/A-Z/a-z/;

# ex) 1.01.1 -> 1.1.1
my $ips_version="";
foreach my $num (split(/\./,$mod->{RO}->{CPAN_VERSION})) {
    $ips_version.=int($num).".";
}
chop($ips_version);

# replace version number.
my $version=$mod->{RO}->{CPAN_VERSION};
my $cpan_file=$mod->{RO}->{CPAN_FILE};
$cpan_file=~s/$version/\%\{tarball_version\}/;

# get license file
my $license_url="http://search.cpan.org/src/".$mod->{RO}->{CPAN_USERID}."/".$module_name."-".$mod->{RO}->{CPAN_VERSION}."/LICENSE";
system("wget -O copyright/SFEperl-$pkg.copyright $license_url");

# out spec files
open (OUT,">SFEperl-$pkg.spec") or die ("cannot write SFEperl-$pkg.spec");

print OUT <<_END ;
#
# spec file for package: SFEperl-$pkg
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#
\%include Solaris.inc

\%define tarball_version $mod->{RO}->{CPAN_VERSION}
\%define tarball_name    $module_name

Name:		SFEperl-$pkg
IPS_package_name: library/perl-5/$pkg
Version:	$mod->{RO}->{CPAN_VERSION}
IPS_component_version: $ips_version
Summary:	$mod->{RO}->{description}
License:	Artistic
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://search.cpan.org/~$userid/\%{tarball_name}-\%{tarball_version}
SUNW_Basedir:	\%{_basedir}
SUNW_Copyright: \%{name}.copyright
Source0:	http://search.cpan.org/CPAN/authors/id/$cpan_file

BuildRequires:	SUNWperl584core
BuildRequires:	SUNWperl584usr
Requires:	SUNWperl584core
Requires:	SUNWperl584usr

Meta(info.maintainer):          roboporter by pkglabo.justplayer.com <pkgadmin\@justplayer.com>
Meta(info.upstream):            $vendor
Meta(info.upstream_url):        http://search.cpan.org/~$userid/\%{tarball_name}-\%{tarball_version}
Meta(info.classification):	org.opensolaris.category.2008:Development/Perl

\%description
$mod->{RO}->{description}
\%prep
\%setup -q -n \%{tarball_name}-\%{tarball_version}

\%build
perl Makefile.PL PREFIX=\%{_prefix} DESTDIR=\$RPM_BUILD_ROOT LIB=/usr/perl5/vendor_perl/5.8.4
make

\%install
rm -rf \$RPM_BUILD_ROOT
make pure_install
mkdir -p \$RPM_BUILD_ROOT\%{_datadir}
mv \$RPM_BUILD_ROOT\%{_prefix}/man \$RPM_BUILD_ROOT\%{_datadir}
mv \$RPM_BUILD_ROOT\%{_datadir}/man/man3 \$RPM_BUILD_ROOT\%{_datadir}/man/man3perl

\%clean
rm -rf \$RPM_BUILD_ROOT

\%files
\%defattr(-,root,bin)
\%{_prefix}/perl5
\%attr(755,root,sys) \%dir \%{_datadir}
\%{_mandir}
\#\%attr(755,root,sys) \%dir \%{_bindir}
\#\%{_bindir}/*

\%changelog
_END

close(OUT);

print "1st, check SFEperl-$pkg.spec and copyright/SFEperl-$pkg.copyright.\n";
print "License parameter is always Artistic. check it.\n";
print "2nd,\n../bin/specbuild.sh SFEperl-$pkg.spec\n";

