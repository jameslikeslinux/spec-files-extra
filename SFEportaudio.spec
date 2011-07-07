#
# spec file for package SFEportaudio.spec
#
# includes module(s): portaudio
#
%include Solaris.inc

%define src_name	portaudio
%define src_url		http://www.portaudio.com/archives

Name:                   SFEportaudio
Summary:                Portable cross-platform Audio API
Version:                v19_20110326
IPS_component_version:	0.19.0.20110326
Source:                 %{src_url}/pa_stable_%{version}.tgz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:		SUNWaudh

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export CPPFLAGS="-I${PWD}/src/os/unix"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static		\
	    --without-jack		\
	    --enable-cxx

# Parallelism breaks with 16 cpus, so don't use more than 4
make -j$(test $CPUS -ge 4 && echo 4 || echo $CPUS)

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Fri Apr 15 2011 - Milan Jurik
- new snapshot available
* Tue Feb 24 2009 - Albert Lee
- Use included sys/soundcard.h
* Fri Mar 14 2008 - brian.cameron@sun.com
- Bump to the new 20071207 version.  Remove upstream portaudio-01-oss.diff.
* Sat Sep 22 2007 - dougs@truemail.co.th
- disabled building with jack audio
* Sun May 13 2007 - dougs@truemail.co.th
- Fixed typo
* Mon Apr 30 2007 - dougs@truemail.co.th
- Initial version
