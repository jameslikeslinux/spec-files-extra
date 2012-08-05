#
# spec file for package libvpx
#

Name:		libvpx
License:	BSD
Version:	1.1.0
Source:		http://webm.googlecode.com/files/%{name}-v%{version}.tar.bz2
Patch1:		libvpx-01-shared.diff
Patch2:		libvpx-02-mapfile.diff
Patch3:		libvpx-03-rtcd.diff

%prep
%setup -q -n %{name}-v%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%define archis64 %( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} && echo 1 || echo 0 )

%if %archis64
%define _target x86_64-solaris-gcc
%else
%define _target x86-solaris-gcc
%endif

%ifarch sparc
%define _target sparc-solaris-gcc
%endif

./configure --prefix=%{_prefix} --libdir=%{_libdir} \
	--enable-vp8 --enable-postproc --enable-runtime-cpu-detect \
	--enable-shared --disable-examples \
	--target=%{_target}

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

# Clean up unpackaged files.
rm $RPM_BUILD_ROOT%{_libdir}/*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Aug 05 2012 - Milan Jurik
- bump to 1.1.0
* Sun Oct 23 2011 - Milan Jurik
- bump to 0.9.7-p1
* Fri Mar 18 2011 - Milan Jurik
- fix x86 multiarch
* Thu Mar 17 2011 - Milan Jurik
- initial spec
