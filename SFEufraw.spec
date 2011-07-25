#
# spec file for package SFEufraw
#
# includes module(s): ufraw
#

%include Solaris.inc
%include stdcxx.inc
%include packagenamemacros.inc

Name:		SFEufraw
Summary:	Ufraw - Raw Photo Converter
Group:		Graphics
Version:	0.18
Source:		%{sf_download}/ufraw/ufraw-%{version}.tar.gz
Patch1:		ufraw-01-openmp.diff
Patch2:		ufraw-02-sunstudio.diff
URL:		http://ufraw.sourceforge.net/
License:	GPLv2
SUNW_Copyright:	ufraw.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#BuildRequires: SUNWlcms-devel
BuildRequires: SUNWlcms
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SFEgtkimageview
Requires: SUNWlcms
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-img-editor
Requires: SUNWjpg
Requires: SUNWTiff
Requires: SUNWmlib
Requires: SUNWzlib
Requires: SUNWlibms
Requires: SUNWlibexif
Requires: SUNWdcraw
Requires: SFEgtkimageview

BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-img-editor-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWTiff-devel
BuildRequires: SUNWmlibh
BuildRequires: SUNWlibm
BuildRequires: SUNWlibexif-devel
# dos2unix:
BuildRequires: SUNWesu
# pod2man:
BuildRequires: %pnm_buildrequires_perl_default
BuildRequires: SUNWgnome-common-devel
Requires: SUNWlibstdcxx4
BuildRequires: SUNWlibstdcxx4

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n ufraw-%version
touch NEWS
touch AUTHORS
for f in *.[ch]; do dos2unix -ascii $f $f; done
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export PKG_CONFIG_PATH="%{_libdir}/pkgconfig"
export LDFLAGS="%_ldflags  -L/usr/sfw/lib -R/usr/sfw/lib  -L/usr/gnu/lib -R/usr/gnu/lib"
export POD2MAN=/usr/perl5/bin/pod2man

export CXX="${CXX} -norunpath"
export CFLAGS="%optflags -DSOLARIS"
export CXXFLAGS="%cxx_optflags -library=no%Cstd -I%{stdcxx_include}"
export LDFLAGS="%_ldflags -L%{stdcxx_lib} -R%{stdcxx_lib} -lstdcxx4 -Wl,-zmuldefs"

./configure --prefix=%{_prefix}	\
	--enable-extras		\
	--enable-contrast	\
	--mandir=%{_mandir}	\
	--bindir=%{_bindir}	\
	--libdir=%{_libdir}	\
	--includedir=%{_includedir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make BASENAME=${RPM_BUILD_ROOT}%{_prefix}	\
     MANDIR=${RPM_BUILD_ROOT}%{_mandir} DESTDIR=$RPM_BUILD_ROOT install
# dcraw in SUNWdcraw
rm ${RPM_BUILD_ROOT}%{_bindir}/dcraw

%if %{build_l10n}
%else
#rmdir $RPM_BUILD_ROOT/%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT/%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
##TODO## check applications directory
#%dir %attr (0755, root, other) %{_datadir}/applications
#%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
/usr/lib/gimp/2.0/plug-ins/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Mon Jul 25 2011 - N.B.Prashanth
- add SUNW_Copyright
* Tue Mar 01 2011 - Milan Jurik
- bump to 0.18
* 18 May 2010 - Gilles Dauphin
- check where is gtkimageview
* Tue Mar 30 2010 - Milan Jurik
- update to 0.16
* Sun Oct 11 2009 - Milan Jurik
- add external dcraw dependency
* Mon Feb 09 2009 - Thomas Wagner
- add %dir %attr (0755, root, sys) %{_datadir} - otherwise share permission conflict
- try flags Obsoletes Provides Conflicts SUNWdcraw
* Sun Jan 11 2008 - Thomas Wagner
- adjust %doc
- extra package build_l10n
- Obsolete SUNWdcraw not optimal, should be Provides: SUNWdcraw
* Fri Jan  9 2008 - Thomas Wagner
- temporarily force compiler to gcc
- add patch2 to change args to ctime_r ... needs check about patch1
- remove obsolete patch1 which is really about configure.ac
- bump to 0.15
* Wed Oct 17 2007 - laca@sun.com
- bump to 0.12.1
* Wed Jul  5 2006 - laca@sun.com
- bump to 0.8.1
- rename to SFEufraw
- move to /usr
- update file attributes
* Fri May  5 2006 - damien.carbery@sun.com
- Bump to 0.8.
* Thu Apr  6 2006 - damien.carbery@sun.com
- Update Build/Requires after check-deps.pl run.
* Thu Mar 30 2006 - damien.carbery@sun.com
- Change Source URL to working server and add project URL.
* Fri Mar 17 2006 - markgraf@neuro2.med.uni.magdeburg.de
- Initial spec
