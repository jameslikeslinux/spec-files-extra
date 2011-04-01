#
# spec file for package SFErsync
#

%include Solaris.inc
%include usr-gnu.inc

Name:                    SFErsync
Summary:                 rsync - fast incremental file transfer (%{_basedir}/gnu/bin/rsync)
URL:                     http://rsync.samba.org/
Version:                 3.0.8
Source:                  http://rsync.samba.org/ftp/rsync/rsync-%{version}.tar.gz


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc



%prep
%setup -q -n rsync-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
##export CC=/usr/gnu/bin/gcc
##export CXX=/usr/gnu/bin/g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --disable-static


gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
#in case old pkgbuild does not automaticly place %doc files there
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc COPYING INSTALL NEWS OLDNEWS README TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Fri Apr 01 20011 - Thomas Wagner
- Initial spec
