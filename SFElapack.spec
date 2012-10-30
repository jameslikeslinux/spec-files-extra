#
# spec file for package SFElapack.spec
#
# includes module(s): lapack
#
%include Solaris.inc

#%ifarch amd64 sparcv9
#%include arch64.inc
#%use lapack64 = lapack.spec
#%endif

%include base.inc
%use lapack = lapack.spec

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:		SFElapack
IPS_Package_Name:	library/lapack
Summary:	%{lapack.summary}
Version:	%{lapack.version}
License:	Lapack License
SUNW_Copyright:	lapack.copyright
Group:		System/Libraries
URL:		%{lapack.url}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWcsl
Requires: SUNWcsl
BuildRequires: SUNWlibms
Requires: SUNWlibms
BuildRequires: SFEgcc
Requires: SFEgccruntime
BuildRequires: SFExblas
Requires: SFExblas


%prep
rm -rf %name-%version
mkdir %name-%version
#%ifarch amd64 sparcv9
#mkdir %name-%version/%_arch64
#%lapack64.prep -d %name-%version/%_arch64
#%endif

mkdir %name-%version/%{base_arch}
%lapack.prep -d %name-%version/%{base_arch}

%build
#%ifarch amd64 sparcv9
#%lapack64.build -d %name-%version/%_arch64
#%endif

%lapack.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
#%ifarch amd64 sparcv9
#%lapack64.install -d %name-%version/%_arch64
#%endif

%lapack.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/lib*.a
%{_libdir}/lib*.so
#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%{_libdir}/%{_arch64}/lib*.a
#%{_libdir}/%{_arch64}/lib*.so
#%endif

%changelog
* Fri Oct 26 2012 - Logan Bruns <logan@gedanken.org>
- bump to 3.4.2
* Sun Jun 17 2012 - Thomas Wagner
- add missing (Build)Requires
* Mon Apr 30 2012 - Pavel Heimlich
- make shared libraries
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Tue May 25 2010 - Milan Jurik
- disable multiarch support, not stable with Sun studio Fortran and unsupported with gfortran yet
* Mon May 24 2010 - Milan Jurik
- multiarch support
* Wed Dec 10 2008 - dauphin@enst.fr
- Initial version
