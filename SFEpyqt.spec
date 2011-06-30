#
# spec file for package SFEpyqt
#
# includes module(s): 
#
%include Solaris.inc

%define python_version 2.6

Name:			SFEpyqt
Summary:		Python interface to Qt
License:		GPL
Version:		4.8.3
Source:			http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-x11-gpl-%{version}.tar.gz
URL:			http://www.riverbankcomputing.co.uk/software/pyqt
Group:			Development/Languages/Python
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWPython26
%include default-depend.inc
Requires: SFEqt4
Requires: SFEsip
BuildRequires: SUNWPython26-devel
BuildRequires: SFEsip

%prep
%setup -q -n PyQt-x11-gpl-%{version}

%build
export PYTHON="/usr/bin/python%{python_version}"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export QMAKESPEC=/usr/share/qt/mkspecs/default
python configure.py -w --confirm-license \
    -d %{_libdir}/python%{python_version}/vendor-packages

# Force link with libCrun.  LDFLAGS and LIBS do not seem to be honored
# by configure.py
find . -name "Makefile" | while read makefile; do
        sed 's/^\(LIBS = .*\)/\1 -lCrun/' $makefile > $makefile.new
        mv -f $makefile.new $makefile
done

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Delete optimized py code.
find $RPM_BUILD_ROOT%{_prefix} -type f -name "*.pyo" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/pylupdate4
%{_bindir}/pyuic4
%{_bindir}/pyrcc4
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/sip

%changelog
* Thu Jun 30 2011 - James Lee <jlee@thestaticvoid.com>
- Add runtime dependency on SFEsip, solving "ImportError: No module named sip"
- Force link with libCrun because Python in Solaris doesn't link with it:
  http://download.oracle.com/docs/cd/E18659_01/html/821-1383/bkamv.html
* Tue Feb 01 2011 - Alex Viskovatoff
- bump to 4.8.3, so the tarball downloads
* Sun Nov 07 2010 - Milan Jurik
- bump to 4.8.1 (qt4 support)
* Sat Mar 29 2008 - laca@sun.com
- create
