#
# spec file for package SFErcs
#
# includes module: rcs
#

%include Solaris.inc
%define srcname rcs

Name:	        SFErcs
IPS_Package_Name:	developer/versioning/rcs
Summary:	GNU Revision Control System
URL:		http://www.cs.purdue.edu/homes/trinkle/RCS/
Vendor:		GNU Project
Version:        5.8
License:	GPLv2
SUNW_Copyright:	rcs.copyright
Source:		http://www.cs.purdue.edu/homes/trinkle/RCS/rcs-5.8.tar.gz
Source:		http://www.cs.purdue.edu/homes/trinkle/RCS/%srcname-%version.tar.gz
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc


%prep
%setup -q -n %srcname-%version


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} --mandir=%{_mandir}

make -j$CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

rm -rf %{buildroot}%{_infodir}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_bindir
%_bindir/*
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, bin) %_mandir
%dir %attr (0755, root, bin) %_mandir/man1
%_mandir/man1/*.1
%dir %attr (0755, root, bin) %_mandir/man5
%_mandir/man5/rcsfile.5


%changelog
* Mon Dec 05 2011 - Milan Jurik
- bump to 5.8
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Tue Jan 18 2011 - Alex Viskovatoff
- Initial spec
