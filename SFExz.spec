#
# spec file for package SFExz
#
# includes module(s): xz
#

%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use xz_64 = xz.spec
%endif

%include base.inc
%use xz = xz.spec


Name:		SFExz
Name:                    %{xz.name}
IPS_Package_Name:	compress/xz
Summary:    	         %{xz.summary}
Version:                 %{xz.version}
URL:			 %{xz.url}
Source:		http://tukaani.org/xz/xz-%{version}.tar.bz2
SUNW_Copyright: xz-utils.copyright
Group:		Applications/Archivers
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

#%define cc_is_gcc 0

%description
XZ Utils is free general-purpose data compression software with high
compression ratio. XZ Utils were written for POSIX-like systems (GNU/Linux,
*BSDs, etc.), but also work on some not-so-POSIX systems like Windows. XZ Utils
are the successor to LZMA Utils. 

%if %build_l10n
%package l10n
Summary:        %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
Requires:       %{name}
%endif

%prep
rm -rf %{name}-%{version}
%ifarch amd64 sparcv9
mkdir -p %{name}-%{version}/%_arch64
%xz_64.prep -d %{name}-%{version}/%_arch64
%endif

mkdir -p %{name}-%{version}/%base_isa
%xz.prep -d %{name}-%{version}/%base_isa


%build
%ifarch amd64 sparcv9
%xz_64.build -d %{name}-%{version}/%_arch64
%endif

%xz.build -d %{name}-%{version}/%{base_isa}

%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%xz_64.install -d %{name}-%{version}/%_arch64
%endif

%xz.install -d %{name}-%{version}/%{base_isa}

mkdir -p %{buildroot}/%{_bindir}/%{base_isa}
cp -d %{buildroot}/%{_bindir}/lz[a-z]* %{buildroot}/%{_bindir}/%{base_isa}/
cp -d %{buildroot}/%{_bindir}/un[a-z]* %{buildroot}/%{_bindir}/%{base_isa}/
cp -d %{buildroot}/%{_bindir}/xz[a-z]* %{buildroot}/%{_bindir}/%{base_isa}/
for binary in lzmadec lzmainfo xz xzdec xzdiff xzgrep xzless xzmore
  do
  #move real i386/sparc 32 bit binaries to %{_bindir}/%{base_isa}
  mv %{buildroot}/%{_bindir}/$binary %{buildroot}/%{_bindir}/%{base_isa}/
  ln -f -s ../lib/isaexec %{buildroot}/%{_bindir}/$binary
done #for binary
#symbolic links remain in place, they are copied instead

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'


%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(0755, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%attr (-, root, other) %_datadir/locale
%endif

%changelog
* Sun Sep  9 2012 - Thomas Wagner
- add 32/64-bit multiarch
* Sun Jul 1 2012 - Logan Bruns <logan@gedanken.org>
- Added ips name and bumped to 5.0.4
* Tue Jul 26 2011 - N.B.Prashanth
- Added SUNW_Copyright
* Thu Jun 16 2011 - N.B.Prashanth <nbprash.mit@gmail.com>
- Bump to 5.0.3
* Thu Apr 21 2011 - Alex Viskovatoff
- Bump to 5.0.2
* Fri Feb  4 2011 - Alex Viskovatoff
- Bump to 5.0.1
* Fri Nov  5 2010 - Alex Viskovatoff
- Update to 5.0.0, adding l10n
* Wed Jun 02 2010 - brian.cameron@oracle.com
- Initial setup.
