# =========================================================================== 
#                    Spec File
# =========================================================================== 

%include Solaris.inc

%include packagenamemacros.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	easytag
%define src_version	2.1.7
%define pkg_release	2

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	SFE%{src_name}
IPS_package_name: audio/easytag
Summary:      	Tag editor for MP3, Ogg Vorbis files and more
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	GPLv2+
SUNW_Copyright: easytag.copyright
Group:          Applications/Sound and Video
Source:         %{sf_download}/easytag/%{src_name}-%{version}.tar.bz2
Patch1:        	easytag-01-configure.diff
Patch2:        	easytag-02-mp4_missing_u_intnn_t.diff
URL:            http://easytag.sourceforge.net
BuildRoot:      %{_tmppath}/%{src_name}-%{version}-build

#Requires:      
#BuildRequires: 
%if %option_with_gnu_iconv
Requires: SUNWgnu-libiconv
Requires: SUNWgnu-gettext
%else
Requires: SUNWuiu8
%endif

BuildRequires: %{pnm_buildrequires_SUNWgtk2_devel}
Requires:      %{pnm_requires_SUNWgtk2}
BuildRequires: %{pnm_buildrequires_SUNWpango_devel}
Requires:      %{pnm_requires_SUNWpango}
BuildRequires: %{pnm_buildrequires_SUNWglib2_devel}
Requires:      %{pnm_requires_SUNWglib2}
BuildRequires: %{pnm_buildrequires_SUNWflac_devel}
Requires:      %{pnm_requires_SUNWflac}
BuildRequires: %{pnm_buildrequires_SUNWspeex_devel}
Requires:      %{pnm_requires_SUNWspeex}
BuildRequires: SFElibid3tag-devel
Requires:      SFElibid3tag
BuildRequires: SFElibmp4v2-devel
Requires:      SFElibmp4v2
#C++ by studio compilers:
BuildRequires: SUNWid3lib-devel
Requires:      SUNWid3lib

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%description 
EasyTAG - Tag editor for MP3, Ogg Vorbis files and more

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}-%{version}
%patch1 -p 1
%patch2 -p 1

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags -I/usr/include/id3"
export CXXFLAGS="%cxx_optflags -I/usr/include/id3"
export LDFLAGS="%{_ldflags} -lnsl"
%if %option_with_gnu_iconv
export CFLAGS="$CFLAGS -I/usr/gnu/include -L/usr/gnu/lib -R/usr/gnu/lib -lintl"
%endif

export AR=/usr/bin/ar


./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --datadir=%{_datadir} \
            --libdir=%{_libdir} \
            --bindir=%{_bindir} \
            --sysconfdir=%{_sysconfdir} \
            --disable-static \
            --enable-dynamic

gmake -j$CPUS || $AR -ts src/id3lib/libid3bugfix.a
gmake -j$CPUS


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Install-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

%install
rm -rf $RPM_BUILD_ROOT
gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# File permissions, ownership information. Note the difference between 
# bin(_bindir),share(_datadir) & share/applications
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/%{src_name}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Sun Apr 21 2012 - Thomas Wagner
- Bump to 2.1.7
- re-enable mp4v2 (easytag 2.1.7 has a fix to enable mp4v2)
- add patch easytag-02-mp4_missing_u_intnn_t.diff for missing u_int8_t uint32_t
- add call to "ar" to fix static library with c++wrapper for id3lib
* Fri Apr 21 2012 - Thomas Wagner
- add missing dependencies
- use pnm_macros
- repair compile to really include id3lib
* Tue Sep 28 2011 - Alex Viskovatoff
- disable mp4, which breaks the build
* Sat Jul 23 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Sun Oct 17 2010 - Alex Viskovatoff
- Do not run autoconf: that breaks the build and is not required for tarballs
- Patch configure instead of configure.in, just removing references to stdc++
- Add -lnsl to LDFLAGS
* Thu Jun 10 2010 - pradhap (at) gmail.com
- Bump to 2.1.6
* Sun Feb 24 2008 - trisk@acm.jhu.edu
- Replace patch1, update build rules
* Mon Dec 31 2007 - markwright@internode.on.net
- Added -f option to line rm -rf $RPM_BUILD_ROOT%{_datadir}/locale 

* Sat 17 Nov 2007 - daymobrew@users.sourceforge.net.
- Add support for Indiana, including l10n package.

* Sat 11 Aug 2007 - <shivakumar dot gn at gmail dot com>
- Initial spec.
