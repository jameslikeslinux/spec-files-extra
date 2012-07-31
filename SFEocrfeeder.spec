#
# spec file for package SFEocrfeeder
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): ocrfeeder
#
%include Solaris.inc

%define python_version  2.6

%define src_name ocrfeeder
%define src_url http://ftp.gnome.org/pub/gnome/sources/ocrfeeder/0.7/

Name:		SFEocrfeeder
IPS_Package_Name:	image/ocrfeeder
Summary:	OCRFeeder - Optical Character Recognition program
Version:	0.7.8
Group:		Graphical desktop/GNOME/OCR
URL:		http://live.gnome.org/OCRFeeder
Source:		%{src_url}/%{src_name}-%{version}.tar.xz
License:	GPLv3
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWPython26
Requires:	SUNWPython26
BuildRequires:	SFEpy26goocanvas
Requires:	SFEpy26goocanvas
BuildRequires:	SFEpython26-enchant
Requires:	SFEpython26-enchant
Requires:	SFEpython26-imaging-sane
BuildRequires:	SFEpython26-reportlab
Requires:	SFEpython26-reportlab
Requires:	SFEunpaper

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
Requires:	%{name}
%endif

%description
OCRFeeder is a complete Optical Character Recognition and Document Analysis
and Recognition program.

%prep
xz -dc  %SOURCE | tar -xf -

%build
cd %{src_name}-%version
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export PYTHON=/usr/bin/python%{python_version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}

make -j $CPUS

%install
cd %{src_name}-%version
rm -rf %buildroot
make install DESTDIR=$RPM_BUILD_ROOT  \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm -f {} ';'

%if %build_l10n
%else
#REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf %buildroot

%files
%defattr(-,root,bin)
%_bindir
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/ocrfeeder
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_mandir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*
%{_libdir}/python%{python_version}/vendor-packages

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Mar 25 2012 - Milan Jurik
- bump to 0.7.8
* Sat Mar 26 2011 - Milan Jurik
- initial spec
