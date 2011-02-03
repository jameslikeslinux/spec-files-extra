#
# spec file for package SFEsane-frontends
#
# includes module(s): sane-frontends
#
%include Solaris.inc
%include packagenamemacros.inc

Name:                    SFEsane-frontends
Summary:                 SANE - Scanner Access Now Easy - frontends
Version:                 1.0.14
Source:			 http://alioth.debian.org/frs/download.php/1140/sane-frontends-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:		%{pnm_buildrequires_SUNWsane_backend_devel}
Requires:		%{pnm_requires_SUNWsane_backend}

%prep
%setup -q -n sane-frontends-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

# /usr/sfw needed for libusb
export CPPFLAGS="-I/usr/sfw/include"
export CFLAGS="%optflags -I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"
./configure --prefix=%{_prefix}			\
	    --libexecdir=%{_libexecdir}         \
            --sysconfdir=%{_sysconfdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info
	    		
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, sys) %{_datadir}
%{_datadir}/sane
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Tue Feb  1 2011 - Thomas Wagner
- change BuildRequires to %{pnm_buildrequires_SUNWsane_backend_devel}
  Requires to %{pnm_requires_SUNWsane_backend}
  %include packagenamemacros.inc
* Sun Nov  5 2006 - laca@sun.com
- Create
