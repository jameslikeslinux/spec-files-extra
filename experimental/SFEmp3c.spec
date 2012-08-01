#
# spec file for package SFEmp3c
#

%include Solaris.inc

%define cc_is_gcc 1
%define _gpp /usr/sfw/bin/g++
%include base.inc


Name:                    SFEmp3c
Summary:                 mp3c - ripp audio cd
URL:                     http://wspse.de/WSPse/Linux-MP3c.php3
Version:                 0.31
Source:                  ftp://ftp.wspse.de/pub/linux/wspse/mp3c-%{version}.tar.bz2
Patch1:			mp3c-01-cdio-define.diff
Patch2:			mp3c-02-use-cd-paranoia-and-not-cdda2wav.diff


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#TODO: BuildReqirements:
#TODO: Reqirements:

%include default-depend.inc

BuildRequires: SUNWncurses-devel
Requires: SUNWncurses
#BuildRequires: SFElame-devel
Requires: SFElame
#BuildRequires: SFElibcdio
Requires: SFElibcdio

%prep
%setup -q -n mp3c-%version
%patch1 -p1
%patch2 -p1

%build

export CC=gcc
export CXX=g++

export CFLAGS="%optflags -I/usr/include/ncurses "
export CXXFLAGS="%cxx_optflags -I/usr/include/ncurses "
export LDFLAGS="%_ldflags %{gnu_lib_path} -lsocket -lnsl"



./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --disable-static


make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README BATCH.README CDDB_HOWTO ChangeLog INSTALL NEWS AUTHORS BUGS COPYING FAQ OTHERS TODO ABOUT-NLS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (-, root, other) %{_datadir}/doc
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Sat Oct  1 2011 - Thomas Wagner
- fix permissions /usr/share/doc
- LDFLAGS add %{gnu_lib_path} to have ncurses found
- add Requires: SFElame, SFElibcdio (to get cd-paranoia)
* Mon Feb 23 2009  - Thomas Wagner
- Initial spec
