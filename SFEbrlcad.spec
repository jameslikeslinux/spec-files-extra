#
# spec file for package SFEbrlcad
#
# includes module(s): brlcad
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

Name:                    SFEbrlcad
Summary:                 cross-platform solid modeling system (BRL-CAD) 
Version:                 7.20.4
Source:                  %{sf_download}/brlcad/brlcad-%{version}.tar.bz2
License: 		 LGPL
URL:                     http://brlcad.org
Group:                   Productivity/Graphics/CAD
Patch1:                  brlcad-01-opennurbs_brep_region.diff
Patch2:                  brlcad-02-pkg.diff
Patch3:                  brlcad-03-if_mem.diff
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

# Note on BRL-CAD 7.14.x for Solaris - Ken Mays 
# Sourceforge has a 7.14.0 binary for Solaris x86 
# URL: https://sourceforge.net/projects/brlcad/files/BRL-CAD%20for%20Solaris/7.14.0/
# BRL-CAD_7.14.0_solaris_x86.pkg.bz2 
#

%include default-depend.inc

BuildRequires: SFEcmake 
Requires: SUNWcsu
BuildRequires:      SFEgcc
Requires:           SFEgccruntime

%prep
%setup -q -n brlcad-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

bash autogen.sh

export PATH=$PATH:/usr/perl5/bin
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
# export CXXFLAGS="%cxx_optflags -library=no%Cstd -I%{stdcxx_include}"
# export LDFLAGS="%_ldflags -L%{stdcxx_lib} -R%{stdcxx_lib} -lstdcxx4 -Wl,-zmuldefs"
export CXXFLAGS="%cxx_optflags"
#export LDFLAGS="%_ldflags -L/usr/gnu/lib -lm -lnsl -lsocket"
export LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib -R%{_libdir}/brlcad/lib -lm -lnsl -lsocket"
export CPPFLAGS="-I/usr/gnu/include"

mkdir -p builds/unix
cd builds/unix

../../configure --prefix=%{_libdir}/brlcad \
            --mandir=%{_mandir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir}       \
            --disable-strict            \
            --with-tcl=/usr/gnu/lib     \
            --with-tk=/usr/gnu/lib      \
            --disable-tcl-build         \
            --disable-tk-build          \
            --disable-documentation

#cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=%{_libdir}/brlcad ../..

# Note: parallel build is not reliable
make VERBOSE=1 -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT/*
cd builds/unix
make install DESTDIR=$RPM_BUILD_ROOT

DOC="$RPM_BUILD_ROOT/usr/share"
cp "$RPM_BUILD_ROOT/usr/share/COPYING" "$DOC/doc"
cp "$RPM_BUILD_ROOT/usr/share/AUTHORS" "$DOC/doc"
cp "$RPM_BUILD_ROOT/usr/share/INSTALL" "$DOC/doc"
cp "$RPM_BUILD_ROOT/usr/share/HACKING" "$DOC/doc"
cp "$RPM_BUILD_ROOT/usr/share/NEWS"    "$DOC/doc"
cp "$RPM_BUILD_ROOT/usr/share/README"  "$DOC/doc"

rm "$RPM_BUILD_ROOT/usr/share/COPYING"
rm "$RPM_BUILD_ROOT/usr/share/AUTHORS"
rm "$RPM_BUILD_ROOT/usr/share/INSTALL"
rm "$RPM_BUILD_ROOT/usr/share/HACKING"
rm "$RPM_BUILD_ROOT/usr/share/NEWS"   
rm "$RPM_BUILD_ROOT/usr/share/README" 

mkdir "$DOC/brlcad"
mv "$DOC"/doc/* "$DOC"/brlcad
mv "$DOC"/brlcad "$DOC"/doc

mkdir -p $RPM_BUILD_ROOT/usr/bin/
ln -s %{_libdir}/brlcad/bin/mged $RPM_BUILD_ROOT/usr/bin/mged

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}/brlcad
%dir %attr (0755, root, bin) %{_libdir}/brlcad/bin
%{_libdir}/brlcad/bin/*
%{_libdir}/brlcad/lib/*
%{_libdir}/brlcad/include/*

#%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/*

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3/*
%dir %attr(0755, root, bin) %{_mandir}/man5/*
%dir %attr(0755, root, bin) %{_mandir}/mann/*

%dir %attr(0755, root, bin) %{_datadir}/tclscripts
%{_datadir}/tclscripts/*

%dir %attr(0755, root, bin) %{_datadir}/db
%{_datadir}/db/*

%dir %attr(0755, root, bin) %{_datadir}/pix
%{_datadir}/pix/*

%dir %attr(0755, root, bin) %{_datadir}/html
%{_datadir}/html/*

%dir %attr(0755, root, bin) %{_datadir}/plugins
%{_datadir}/plugins/*

%dir %attr(0755, root, bin) %{_datadir}/sample_applications
%{_datadir}/sample_applications/*

%dir %attr(0755, root, bin) %{_datadir}/vfont
%{_datadir}/vfont/*

%dir %attr(0755, root, bin) %{_datadir}/nirt
%{_datadir}/nirt/*

%dir %attr(0755, root, bin) %{_datadir}/data
%{_datadir}/data/*

#%dir %attr(0755, root, bin) %{_datadir}/brlcad
#%{_datadir}/brlcad/*

%dir %attr(0755, root, bin) %{_datadir}/doc/brlcad
%{_datadir}/doc/brlcad/*


%changelog
* Thu Apr 26 2012 - Logan Bruns <logan@gedanken.org>
- Bumped to 7.20.4
* Tue Jun 7 2011 - Ken Mays <kmays2000 at gmail.com>
- Bumped to 7.20.0
- Modified for SFEcmake build system
* Tue Feb 5 2007 - pradhap (at) gmail.com
- Initial brlcad spec file.

