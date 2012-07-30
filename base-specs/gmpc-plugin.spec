#
# base-spec file for package SFEgmpc-plugin-**** (plugin)
#
# use gcc to compile
#

%include Solaris.inc
%define cc_is_gcc 1


%if %{!?plugindownloadname:0}%{?plugindownloadname:1}
%else
%define plugindownloadname %{pluginname}
%endif

Name:			gmpc-plugin-%{pluginname}
URL:                     http://sarine.nl/gmpc
Version:                 0.20.0
Source:			 http://download.sarine.nl/Programs/gmpc/%{version}/gmpc-%{plugindownloadname}-%{version}.tar.gz

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%prep
%setup -q -n gmpc-%{plugindownloadname}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export LDFLAGS="-lX11"
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++

CC=$CC CXX=$CXX XGETTEXT=/bin/gxgettext MSGFMT=/bin/gmsgfmt ./configure --prefix=%{_prefix} \
	--mandir=%{_mandir} \
	--libdir=%{_libdir}              \
	--libexecdir=%{_libexecdir}      \
	--sysconfdir=%{_sysconfdir}      \
        --disable-static

  

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
#rm -f $RPM_BUILD_ROOT%{_libdir}/gmpc/plugins/*.la
gfind $RPM_BUILD_ROOT -name \*.la -exec rm {} \;
gfind $RPM_BUILD_ROOT -name \*.a -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

#NOTE: below %files, is not used in this include system.
%files
%defattr(-, root, bin)
#see other files which include this one here


%changelog
* Wed Apr 25 2012 - Thomas Wagner
- remove (Build)Requires: SUNWgcc(runtime) because pkgtool/pkgbuild fully 
  ignores them in consuming spec file if this file is included with %use
* Tue Apr 24 2012 - Thomas Wagner
- add --disable-static
- add removal for .a files
* Wed Oct  6 2010 - Alex Viskovatoff
- bump to 0.20.0; use gmake, gfind, gxgettext, gmsgfmt
* Sun Sep 27 2009 - Thomas Wagner
- bump to 0.19.0, remove sub version strings, new Download-URL
* Sat Feb 21 2009 - Thomas Wagner
- moved (Build-)Requirements SFEgmpc(-devel) over to the plugin specs to be effective
- add case for last.fm isn't lastfm -> plugindownloadname which defaults to pluginname
* Sun Dec 02 2007 - Thomas Wagner
- initial base-spec for gmpc-plugin
