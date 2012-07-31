#
# spec file for package xmlrpc-epi
#
# includes module(s): xmlrpc-epi
#
%include Solaris.inc

Name:                   xmlrpc-epi
Summary:                A general purpose implementation of the xmlrpc specification in C
URL:                    http://xmlrpc-epi.sourceforge.net/
Version:                0.54.2
Source:                 %{sf_download}/xmlrpc-epi/xmlrpc-epi-base/%{version}/xmlrpc-epi-%{version}.tar.bz2
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --includedir=%{_prefix}/include/xmlrpc-epi \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
( Sat Oct 05 2011 - Milan Jurik
- bump to 0.54.2
* Fri Jan 29 2010 - brian.cameron@sun.com
- Initial base spec with version 0.54.1.
