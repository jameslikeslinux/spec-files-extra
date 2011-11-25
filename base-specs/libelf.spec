#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

Name:                libelf
Summary:             A Library to Manipulate ELf Files
Version:	0.8.13
Source:              http://www.mr511.de/software/libelf-%{version}.tar.gz
Patch1:		libelf-01-shared-x86.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%{cxx_optflags}"
export PKG_CONFIG_PATH="%{_libdir}/pkgconfig"
export PERL_PATH=/usr/perl5/bin/perl
export LDFLAGS="%{_ldflags} -L%{_libdir} -R%{_libdir}"

autoconf
./configure --prefix=$RPM_BUILD_ROOT%{_prefix}	\
	    --bindir=%{_bindir}	\
	    --libdir=$RPM_BUILD_ROOT%{_libdir}	\
	    --mandir=%{_mandir}	\
            --enable-shared 

make -j$CPUS

%install
make install

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Nov 25 2011 - Milan Jurik
- bump to 0.8.13
* Thu Feb 25 2010 - jchoi42@pha.jhu.edu
- Initial spec
