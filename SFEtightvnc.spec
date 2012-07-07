#
# spec file for package SFEtightvnc
#
# includes module(s): tightvnc
#
# Owner: laca
#
%include Solaris.inc
%include usr-gnu.inc
%include packagenamemacros.inc

Name:                    SFEtightvnc
IPS_Package_Name:	desktop/remote-desktop/tightvnc
Summary:                 VNC (Virtual Network Computing) client
Version:                 1.3.10
Group:		Applications/Internet
URL:                     http://www.tightvnc.com/
Source:                  %{sf_download}/vnc-tight/tightvnc-%{version}_unixsrc.tar.bz2
Patch1:			tightvnc-01-csw-0003-libdix.a-after-libos.a.patch 
License:		 GPLv2
SUNW_Copyright:		 tightvnc.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWjpg
Requires: SUNWlibmsr
Requires: %{pnm_requires_perl_default}
Requires: SUNWxwplt
Requires: SUNWzlib
BuildRequires: %{pnm_buildrequires_SUNWxwopt}

%prep
%setup -q -n vnc_unixsrc
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

#correct cc path
cc_dir=`dirname $CC`
perl -pi -e "s,/opt/SUNWspro/bin,${cc_dir},g" \
    Xvnc/config/cf/sun.cf

export CC_include=`find $cc_dir/.. -name "CC"|grep include|head -1`
perl -pi -e "s,/opt/SUNWspro/SC3.0/include/CC,${CC_include},g" \
    Xvnc/config/cf/sun.cf


export PATH=/usr/openwin/bin:${PATH}
export LDFLAGS="%{_ldflags}"
export CFLAGS="%optflags"
xmkmf
make World
cd Xvnc
./configure 
# parallel build fails sometimes
make

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
./vncinstall $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_mandir}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Sat Jul  7 2012 - Thomas Wagner
- change to (Build)Requires to %{pnm_buildrequires_SUNWxwopt}
* Sat Sep  3 2011 - Thomas Wagner
- add patch1 tightvnc-01-csw-0003-libdix.a-after-libos.a.patch 
  to avoid: ffsl os/libos.a(WaitFor.o)\n ld: fatal: symbol referencing errors.
* Thu Sep  1 2011 - Alex Viskovatoff
- bump to 1.3.10; install in /usr/gnu to avoid conflict with tigervnc
* Sun Feb 22 2009 - Thomas Wagner
- add Conflicts: SUNWxvnc, Conflicts: SUNWvncviewer
* Fri Jun 22 2007 - laca@sun.com
- re-rename to SFEtightvnc, leaving the clean-ups in and re-adding the
  viewer
* Mon Jun 11 2007 - laca@sun.com
- copy from SFE, rename from SFEtightvnc to SUNWvncserver and delete
  the viewer from the package
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Add Requires/BuildRequries after check-deps.pl run.
* Mon Mar 05 2007 - nonsea@users.sourceforge.net
- Bump to 1.3.8.
* Mon Jan 22 2007 - daymobrew@users.sourceforge.net
- Add -n so that the viewer pkg is SFEvncviewer not SFEtightvnc-SFEvncviewer.
* Fri Jan 19 2007 - daymobrew@users.sourceforge.net
- Use $CC instead of `which cc`. Remove '-j $CPUS' from 'make' call as it
  breaks the build.
* Thu Jan 18 2007 - halton.huo@sun.com
- Make it can be built when SunStudio is not installed under /opt/SUNWspro
- Fix build and install error
- Add package SFEvncviewer
* Fri Jan 12 2007 - daymobrew@users.sourceforge.net
- Initial spec

