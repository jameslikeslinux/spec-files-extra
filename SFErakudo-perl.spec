#
# spec file for package SFErakudo-perl
#
# includes module: rakudo-perl
#

%include Solaris.inc
%define srcname rakudo-star
%define srcvers 2011.01

Name:		SFErakudo-perl
Summary:	A Perl 6 implementation built on the Parrot virtual machine
URL:		http://www.rakudo.org/
Vendor:		Rakudo.org
Version:	2011.1
License:	Artistic License 2.0
Source:		http://github.com/downloads/rakudo/star/%srcname-%srcvers.tar.gz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc

BuildRequires:	SFEparrot-devel
BuildRequires:	SFEparrot
Requires:	SFEparrot


%prep
%setup -q -n %srcname-%srcvers


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

perl Configure.pl --prefix=%_prefix
gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT
cd docs
cp UsingPerl6-draft.pdf cheatsheet.txt $RPM_BUILD_ROOT%_docdir/rakudo
cd $RPM_BUILD_ROOT%_prefix
mv man share
chmod +x bin/*

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/perl6
%_bindir/ufo
%_libdir/parrot
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_docdir
%_docdir/rakudo
%_mandir


%changelog
* Fri Mar 11 2011 - Alex Viskovatoff
- Initial spec
