#
# spec file for package SFEasterisk
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define src_name   asterisk
%define src_version    1.8.10.0

Name:         	SFE%{src_name}
IPS_Package_Name:	 voip/asterisk
Summary:      	Asterisk : Complete IP PBX in software
Version:      	%{src_version}
License:      	GPLv2
SUNW_Copyright: asterisk.copyright
Group:          Communication
Source:         http://downloads.digium.com/pub/asterisk/releases/%{src_name}-%{version}.tar.gz
Source2:        ext-sources/asterisk.xml
Patch1:        	asterisk-01-oss.diff
Patch2:        	asterisk-02-term.diff
URL:            http://www.asterisk.org
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:      SFEgcc
Requires:           SFEgccruntime

%description 
Asterisk is a complete IP PBX in software. It runs on a wide variety of operating systems and provides all of the features one would expect from a PBX including many advanced features that are often associated with high end (and high cost) proprietary PBXs. Asterisk supports Voice over IP in many protocols, and can interoperate with almost all standards-based telephony equipment using relatively inexpensive hardware.

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep 
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

cp -p %{SOURCE2} asterisk.xml

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir} --localstatedir=%{_localstatedir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# no section 8
install -d 0755 $RPM_BUILD_ROOT%{_datadir}/man/man1m
for i in $RPM_BUILD_ROOT%{_datadir}/man/man8/*.8
do
  base=`basename $i 8`
  name1m=${base}1m
  mv $i $RPM_BUILD_ROOT%{_datadir}/man/man1m/${name1m}
done
rmdir $RPM_BUILD_ROOT%{_datadir}/man/man8
for i in $RPM_BUILD_ROOT%{_datadir}/man/*/*
do
  sed 's/(8)/(1M)/g' $i | sed '/^\.TH/s/ \"8\" / \"1M\" /g' > $i.new
  mv $i.new $i
done

# run dir is swap
rmdir $RPM_BUILD_ROOT%{_localstatedir}/run/%{src_name}
rmdir $RPM_BUILD_ROOT%{_localstatedir}/run

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp asterisk.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,bin)
%{_sbindir}
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%files root
%defattr (-, root, sys)
%{_sysconfdir}
%dir %attr (0755, root, bin) %{_localstatedir}/spool
%{_localstatedir}/spool/*
%dir %attr (0755, root, sys) %{_localstatedir}/log
%{_localstatedir}/log/%{src_name}
%dir %attr (0755, root, other) %{_localstatedir}/lib
%{_localstatedir}/lib/%{src_name}
%dir %attr (0755, root, sys) /var/svc
%class(manifest) %attr(0444, root, sys) /var/svc/manifest/site/asterisk.xml

%changelog
* Thu Mar 8 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.8.10.0
* Fri Mar 2 2012 - Logan Bruns <logan@gedanken.org>
- Added an smf manifest.
* Tue Feb 22 2012 - Logan Bruns <logan@gedanken.org>
- bump to 1.8.9.2 and add IPS package name
* Fri Jul 22 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sat Mar 19 2011 - Milan Jurik
- bump to 1.8.3.2
* Wed Feb 02 2011 - Milan Jurik
- /var/run is under core system control
* Mon Jan 24 2011 - Milan Jurik
- bump to 1.8.2.2
* Wed Jan 05 2011 - Milan Jurik 
- bump to 1.8.1.1
* Fri Nov 26 2010 - Milan Jurik
- major update to 1.8.0
* Sun Oct 14 2007 - laca@sun.com
- fix some directory attributes
* Sat Aug 11 2007 - <shivakumar dot gn at gmail dot com>
- Initial spec.
