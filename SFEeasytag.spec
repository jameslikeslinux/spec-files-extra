# =========================================================================== 
#                    Spec File
# =========================================================================== 
%include Solaris.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	easytag
%define src_version	2.1
%define pkg_release	1

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	%{src_name}
Summary:      	Easytag :  EasyTAG - Tag editor for MP3, Ogg Vorbis files and more
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	GPL
Group:          Entertainment
Source:         http://nchc.dl.sourceforge.net/sourceforge/easytag/%{src_name}-%{version}.tar.bz2
Patch:        	easytag2.1-01-libnsl.diff
Vendor:       	http://easytag.sourceforge.net
URL:            http://easytag.sourceforge.net
Packager:     	Shivakumar GN
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build

#Requires:      
#BuildRequires: 

%description 
EasyTAG - Tag editor for MP3, Ogg Vorbis files and more

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}-%{version}
./configure --prefix=%{_prefix}

%patch0 -p 1

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build
make

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Install-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

%install
make install DESTDIR=$RPM_BUILD_ROOT

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

%dir %attr (0755, root, sys) %{_prefix}/man
%{_prefix}/man/*

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/pixmaps
%{_datadir}/%{src_name}

%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*

%changelog
* 2007.Aug.11 - <shivakumar dot gn at gmail dot com>
- Initial spec.
