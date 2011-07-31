#
# spec file for package SFEmono
#
# includes module(s): mono
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

Name:         SFEmono
License:      Other
Group:        System/Libraries
Version:      2.10.2
Summary:      mono - .NET framework
Source:       http://go-mono.com/sources/mono/mono-%{version}.tar.bz2
Patch2:       mono-02-sgen.diff
URL:          http://www.mono-project.com/Main_Page
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWgnome-base-libs
Requires: %name-root
BuildRequires:	SFEgcc
Requires:	SFEgccruntime

%package root
Summary:       %{summary} - / filesystem
SUNW_BaseDir:  /
%include default-depend.inc

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%name

%prep
%setup -q -n mono-%version
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CC=/usr/gcc/4.6/bin/gcc
export CXX=/usr/gcc/4.6/bin/g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
		--bindir=%{_prefix}/mono/bin \
		--mandir=%{_mandir} \
		--libdir=%{_libdir} \
		--libexecdir=%{_libexecdir} \
		--sysconfdir=%{_sysconfdir}	\
		--with-gc=boehm			\
		--with-sgen=yes			\
		--disable-static		\
		--enable-shared			\
		--with-large-heap		\
		--enable-dtrace=no

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

mv $RPM_BUILD_ROOT%{_mandir}/man1 $RPM_BUILD_ROOT%{_mandir}/man1mono
cd $RPM_BUILD_ROOT%{_mandir}/man1mono
for fn in *; do
    f=`basename $fn .1`
    sed -e 's/^\.TH \([^ ]*\) 1/.TH \1 1MONO/' $f.1 > $f.1mono
    rm -f $f.1
done
ln -s mcs.1mono gmcs.1mono

mv $RPM_BUILD_ROOT%{_mandir}/man5 $RPM_BUILD_ROOT%{_mandir}/man5mono
cd $RPM_BUILD_ROOT%{_mandir}/man5mono
for fn in *; do
    f=`basename $fn .5`
    sed -e 's/^\.TH \([^ ]*\) 5/.TH \1 5MONO/' $f.5 > $f.5mono
    rm -f $f.5
done

%if %build_l10n
%else
#REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, bin)
%{_prefix}/mono/bin
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/mono
%{_libdir}/mono/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/mono*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1mono
%{_mandir}/man1mono/*
%dir %attr(0755, root, bin) %{_mandir}/man5mono
%{_mandir}/man5mono/*

%files root
%defattr (-, root, sys)
%{_sysconfdir}/mono

%files devel
%defattr (-, root, bin)
%{_includedir}/mono*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/mono-source-libs
%{_libdir}/monodoc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Jul Sun 31 2011 - Milan Jurik
- bump to 2.10.2, more work needs to be done
* Mon Sep 03 2007 - trisk@acm.jhu.edu
- Add patch for readdir_r stack corruption and bug
* Sun Sep 02 2007 - trisk@acm.jhu.edu
- Bump to 1.2.5
- Unbreak patches
* Tue Aug 14 2007 - trisk@acm.jhu.edu
- Add patch2 http://bugzilla.gnome.org/show_bug.cgi?id=370081
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Sat Mar 17 2007 - laca@sun.com
- bump to 1.2.3.1
* Thu Nov 30 2006 - laca@sun.com
- bump to 1.2
* Sat Oct 14 2006 - laca@sun.com
- bump to 1.1.18
* Wed Sep  7 2006 - jedy.wang@sun.com
- bump to 1.1.17.1
* Sat Jul 15 2006 - laca@sun.com
- rename to SFEmono
- bump to 1.1.16.1
- include Solaris.inc
- force using gcc
- move bin files to /usr/mono/bin
* Wed Jul 12 2006 - jedy.wang@sun.com
- Initial spec
