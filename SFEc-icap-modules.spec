#
# spec file for package SFEc-icap-modules
#
# includes module(s): c-icap-modules
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define	src_name c_icap_modules

Name:		SFEc-icap-modules
Summary:	C-ICAP modules
License:	GPLv2
SUNW_Copyright:	c-icap-modules.copyright
Version:	0.1.6
Group:		System/Utilities
URL:		http://c-icap.sourceforge.net/
Source:		%{sf_download}/c-icap/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SFEclamav-devel
Requires:	SFEclamav
BuildRequires:	SFEc-icap-devel
Requires:	SFEc-icap
BuildRequires:	SFEbdb
Requires:	SFEbdb

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CFLAGS="%optflags -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"

./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --sysconfdir=%{_sysconfdir}		\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --disable-static			\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/c_icap/*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}/c_icap/*.so*

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%changelog
* Tue Jul 12 2011 - Milan Jurik
- bump to 0.1.6
* Tue Mar 29 2011 - Milan Jurik
- initial spec
