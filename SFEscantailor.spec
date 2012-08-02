# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name scantailor

Name:		SFEscantailor
IPS_Package_Name:	desktop/scanner/scantailor
Summary:	post-processing tool for scanned pages
Version:	0.9.11.1
URL:		http://scantailor.sourceforge.net/
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
Group:		Applications/Graphics and Imaging
License:	GPLv3+
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}_%{version}-build
%include default-depend.inc
BuildRequires:	SFEboost-gpp-devel
Requires:	SFEboost-gpp
BuildRequires:	SFEqt-gpp-devel
Requires:	SFEqt-gpp

%description
Scan Tailor is an interactive post-processing tool for scanned pages. It performs operations such as page splitting, deskewing, adding/removing borders, and others. You give it raw scans, and you get pages ready to be printed or assembled into a PDF or DJVU file. Scanning, optical character recognition, and assembling multi-page documents are out of scope of this project.

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
export CC=gcc
export CXX=g++

export PATH=/usr/g++/bin:$PATH

mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_SKIP_RPATH=0 -DCMAKE_INSTALL_RPATH=/usr/g++/lib

make -j$CPUS

%install
rm -rf %{buildroot}

cd build
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}

%changelog
* Sun Apr 15 2012 - Milan Jurik
- Initial spec
