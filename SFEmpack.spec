# spec file for package SFEmpack.spec
#


##TODO## run check-deps.pl on this package and add correct Build/Runtime
##       dependencies later

%include Solaris.inc
%include packagenamemacros.inc

%define src_name mpack

Name:            SFEmpack
Summary:         tools for encoding/decoding MIME messages - mpack munpack
Version:         1.6
Source:          http://ftp.andrew.cmu.edu/pub/mpack/mpack-%{version}.tar.gz
License:         CMU (MIT like)
Url:             http://ftp.andrew.cmu.edu/pub/mpack/
%include default-depend.inc

# OpenSolaris IPS Package Manifest Fields
Meta(info.upstream): anibal@debian.org
Meta(info.maintainer): Thomas Wagner <tom68@users.sourceforge.net>
Meta(info.repository_url): http://ftp.andrew.cmu.edu/pub/mpack/mpack-%{version}.tar.gz
Meta(info.classification): org.opensolaris.category.2008:Applications/Internet
Meta(info.detailed_url):   http://ftp.andrew.cmu.edu/pub/mpack/

BuildRoot:       %{_tmppath}/%{name}-%{version}-build

SUNW_BaseDir:    %{_basedir}
SUNW_Copyright:  %{name}.copyright
BuildRequires:	%{pnm_buildrequires_python_default}
Requires:	%{pnm_requires_python_default}
BuildRequires:	%{pnm_buildrequires_python_default}-extra
Requires:	%{pnm_requires_python_default}-extra
BuildRequires:	SUNWbash

##TODO## sort out BuildRequires
#BuildRequires:	%{pnm_buildrequires_python_default}-cherrypy
#BuildRequires:	%{pnm_buildrequires_python_default}-imaging
#BuildRequires:	%{pnm_buildrequires_python_default}-ply
#BuildRequires:	%{pnm_buildrequires_python_default}-pyopenssl
#BuildRequires:	%{pnm_buildrequires_python_default}-zope-interface
#BuildRequires:	%{pnm_buildrequires_python_default}-ctypes
#BuildRequires:	%{pnm_buildrequires_python_default}-simplejson

#Requires:	%{pnm_requires_python_default}-cherrypy
#Requires:	%{pnm_requires_python_default}-imaging
#Requires:	%{pnm_requires_python_default}-ply
#Requires:	%{pnm_requires_python_default}-pyopenssl
#Requires:	%{pnm_requires_python_default}-zope-interface
#Requires:	%{pnm_requires_python_default}-ctypes
#Requires:	%{pnm_requires_python_default}-simplejson


%description
tools for encoding/decoding MIME messages

%prep

%setup -q -c -n %{src_name}-%{version}

%build


cd %{src_name}-%{version}

CC=cc CXX=CC ./configure --prefix=%{_prefix} \
	--exec-prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--mandir=%{_mandir} \
	--libexecdir=%{_prefix}/lib \
	--disable-static \
	--disable-dynamic \
	--enable-shared
[ $? -ne 0 ] && exit 1			# Early error exit

make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC



%install


rm -rf $RPM_BUILD_ROOT
cd %{src_name}-%{version}

make install  DESTDIR=$RPM_BUILD_ROOT





%files
%defattr (-, root, bin)
%doc  %{src_name}-%{version}/Changes %{src_name}-%{version}/INSTALL %{src_name}-%{version}/README.mac %{src_name}-%{version}/README.unix
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Wed Jul 20 2011 - Thomas Wagner
- migrated over from spec-files-jucr
- make use of pnm_macros for e.g. Python26 packages
* Wed Jul 22 17:37:20 2009
- Initial spec machine generated by roboporter
-  on: Wed Jul 22 17:37:20 2009
## Re-build 24/09/09