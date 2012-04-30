#
# spec file for package SFEpngcheck
#
# includes module(s): pngcheck
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname pngcheck

Name:                    SFEpngcheck
IPS_Package_Name:	 image/pngcheck
Summary:                 pngcheck - verifies the integrity of PNG, JNG and MNG files
Group:                   Utility
Version:                 2.3.0
URL:		         http://www.libpng.org/pub/png/apps/pngcheck.html
Source:		         %{sf_download}/project/png-mng/%{srcname}/%{version}/%{srcname}-%{version}.tar.gz
License:      	         GPL
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
pngcheck verifies the integrity of PNG, JNG and MNG files (by checking
the internal 32-bit CRCs [checksums] and decompressing the image
data); it can optionally dump almost all of the chunk-level
information in the image in human-readable form. For example, it can
be used to print the basic statistics about an image (dimensions, bit
depth, etc.); to list the color and transparency info in its palette
(assuming it has one); or to extract the embedded text
annotations. This is a command-line program with batch capabilities.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version

%build

$CC $CFLAGS -DUSE_ZLIB -o pngcheck pngcheck.c -lz
$CC $CFLAGS -DUSE_ZLIB -o pngsplit gpl/pngsplit.c -lz

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
cp pngcheck pngsplit $RPM_BUILD_ROOT/usr/bin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Sun Apr 29 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
