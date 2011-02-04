#
# spec file for package SFEarj.spec
#
# includes module(s): arj
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc


%define src_name	arj
%define src_url		http://downloads.sourceforge.net
%define src_version 3.10.22
# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

Name:                   SFEarj
Summary:                ARJ - File archiving utlitity
Version:                %{src_version}
Source:                 http://downloads.sourceforge.net/%{src_name}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
Patch0:                 %{src_name}-01-%{version}.gcc.diff

Requires: SUNWcsl
Requires: SUNWlibms
BuildRequires: SUNWgcc

# OpenSolaris IPS Manifest Fields
Meta(info.upstream): Andrew Belov <andrew_belov@users.sourceforge.net>
Meta(info.maintainer): pkgbuild-sfe-devel@lists.sourceforge.net
Meta(info.classification): org.opensolaris.category.2008:Applications/System Utilities



%prep
%setup -q -n %{src_name}-%{version}
%patch0 -p1
cd gnu
autoconf
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir}
cd ..
gmake prepare RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%build

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

(CC=gcc CXX=g++ gmake ; /usr/bin/echo)
#check if arj executable got created, probably others still missing
#problem is: "Patch" not found by proram postproc
[ -x ./solaris2.11/en/rs/arj/arj ] 

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*

%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/*

%dir %attr(0755,root,sys) %{_datadir}
%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/*

%changelog
* Fri Feb  4 2011 - Thomas Wagner
- very dirty hack. program postproc complains about "Patch" not found. packetize anways.
  probably we need this source instead: http://arj.sourceforge.net/files/arjs_310
* Sun Oct 14 2007 - laca@sun.com
- fix _datadir permissions
* Sat Aug 11 2007 - ananth@sun.com
- Initial version
