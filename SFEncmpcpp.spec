#
# spec file for package SFEncmpcpp
#
# includes module: ncmpcpp
#

%include Solaris.inc
%define cc_is_gcc 1
%define _gpp /usr/gnu/bin/g++
%include base.inc
%define srcname ncmpcpp

Name:		SFEncmpcpp
Summary:	Text-mode Music Player Daemon client
URL:		http://unkart.ovh.org/ncmpcpp
Vendor:		Andrzej Rybczak <electricityispower.gmail.com>
Version:	0.5.7
License:	GPLv2
Source:		http://unkart.ovh.org/%srcname/%srcname-%version.tar.bz2

%include default-depend.inc
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	SFEgcc
Requires:	SFEgccruntime
BuildRequires:	SUNWncurses
Requires:	SUNWncurses
BuildRequires:	SFElibmpdclient-devel
Requires:	SFElibmpdclient


%prep
%setup -q -n %srcname-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi
export CFLAGS="%optflags"

# Get compile errors with CC
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/g++
export CXXFLAGS="%cxx_optflags -fpermissive -I/usr/include/ncurses -L/usr/gnu/lib -R/usr/gnu/lib"
export LIBS=-lsocket
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
# Very strangely, without "--without-taglib" link errors are produced
# even if taglib is not installed
./configure --prefix=%_prefix \
            --without-taglib

# line 90 of /usr/gnu/bin/ncursesw5-config inserts a ":" 
# in the lib options
sed 's|-R :/usr/gnu/lib ||' Makefile > Makefile.fixed
mv Makefile.fixed Makefile
cd src
sed 's|-R :/usr/gnu/lib ||' Makefile > Makefile.fixed
mv Makefile.fixed Makefile
cd ..

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/%srcname
%dir %attr (-, root, sys) %_datadir
%_mandir
%dir %attr (-, root, other) %_docdir
%_docdir/%srcname


%changelog
* Mon Jul 18 2011 - Alex Viskovatoff
- Add -fpermissive flag to allow compilation with gcc 4.6
* Sun May 22 2011 - N.B.Prashanth <nbprash.mit@gmail.com>
- Add missing dependencies
- Bump to 0.5.7
* Tue Feb 01 2011 - Alex Viskovatoff
- Add missing dependencies
* Sun Jan 30 2011 - Alex Viskovatoff
- Update to 0.5.6
* Thu Oct 21 2010 - Alex Viskovatoff
- Initial spec
