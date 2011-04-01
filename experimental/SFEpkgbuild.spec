#
# spec file for package SFEpkgbuild
#

# NOTE: To make the unpatched pkgbuild find the patches, use
#	pkgtool build --patches=patches/pkgbuild experimental/SFEpkgbuild.spec
  
# Vanilla pkgbuild's default install prefix is /opt/pkgbuild
# We follow the SFE convention of installing in /usr
# Use pkgbuild --define 'pkgbuild_prefix /path/to/dir'
# to define a different install prefix.

%{?!pkgbuild_prefix:%define pkgbuild_prefix /usr}
%define _prefix %{pkgbuild_prefix}

%define srcname pkgbuild
%define _pkg_docdir %_docdir/%srcname

Name:         SFEpkgbuild
#IPS_Package_Name: package/pkgbuild
License:      GPL
Group:        Development/Tools/Other
URL:	      http://pkgbuild.sourceforge.net/
Version:      1.3.103
Release:      1
BuildArch:    noarch
Vendor:	      OpenSolaris Community
Summary:      pkgbuild - rpmbuild-like tool for building Solaris packages
Source:       http://prdownloads.sourceforge.net/pkgbuild/pkgbuild-%{version}.tar.bz2
# First three patches are taken from here:
# http://solaris.bionicmutton.org/hg/kde4-specs-460/file/d57ba60c50da/setup/common/patches
Patch1:       pkgbuild/pkgbuild-patchdir.diff
Patch2:       pkgbuild/pkgbuild-postprocess-debug-separate.diff
Patch3:       pkgbuild/pkgbuild-local.diff
Patch4:       pkgbuild/pkgbuild-xz.diff
BuildRoot:    %{_tmppath}/%{name}-%{version}-build

%if %_is_pkgbuild
#SUNW_Pkg:                  SFpkgbuild
SUNW_MaxInst:              1000
SUNW_BaseDir:              %{pkgbuild_prefix}
SUNW_Copyright:            http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
# OpenSolaris IPS Package Manifest Fields
Meta(info.upstream):	 	Laszlo (Laca) Peter <laca@sun.com>
Meta(info.maintainer):	 	Laszlo (Laca) Peter <laca@opensolaris.org>
Meta(info.repository_url):	http://pkgbuild.cvs.sourceforge.net/viewvc/pkgbuild/pkgbuild/
Meta(info.classification):	org.opensolaris.category.2008:System/Packaging
%endif

%ifos Solaris
Requires:     SUNWbash
Requires:     SUNWperl584core
Requires:     SUNWgpch
%else
Requires:     perl >= 5.0.0
Requires:     patch
%endif
Requires:     SFExz

%description
A tool for building Solaris SVr4 packages based on RPM spec files.
Most features and some extensions of the spec format are implemented.

%prep
%setup -q -n pkgbuild-%version
# Descriptions of patches 2 and 3 are taken from here:
# http://solaris.bionicmutton.org/hg/kde4-specs-460/file/ed3b4f8dbad1/setup/common/install-pkgbuild
# patch letting pkgtool find patches in subdirectories
%patch1
# patch for separating debug files
%patch2 -p1
# patch for publishing to a local repository via the file protocol
%patch3
# patch to make pkgbuild recognize xz compressed archives
%patch4

%build
./configure --prefix=%{pkgbuild_prefix} --docdir=%_docdir/%srcname
#./configure --prefix=%{pkgbuild_prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc COPYING AUTHORS NEWS
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%attr (0755, root, bin) %{_bindir}
%attr (0755, root, bin) %{_libdir}
%{_datadir}/%{srcname}
%{_mandir}

%changelog
* Fri Apr  1 2011 - Alex Viskovatoff <herzen@imap.cc>
- new experimental SFEpkgbuild.spec, using 4 patches
* Tue Jun 22 2010 - laca@sun.com
- updated %files for new doc and man pages
* Fri Apr 17 2009 - laca@sun.com
- add IPS Meta tags
* Fri Aug 11 2006 - <laca@sun.com>
- delete topdir stuff, we have per-user topdirs now
* Mon Aug 08 2005 - <laca@sun.com>
- add GNU Patch dependency
* Thu Dec 09 2004 - <laca@sun.com>
- Remove %topdir/* from the pkgmap and create these directories in %post
* Fri Mar 05 2004 - <laca@sun.com>
- fix %files
* Wed Jan 07 2004 - <laszlo.peter@sun.com>
- initial version of the spec file
