# base-specs/lxml.spec for SFElxml.spec

# owner: tom68

#%define downloadversion  2.9.0-rc2
%define downloadversion  2.8.0
# NO UNTESTED VERSION BUMPS PLEASE
%define downloadversionstripped  %( echo %downloadversion | sed -e 's/-rc.*//' )


Name:                    SFElxml
Summary:                 The XML library (gnu)
Version:                 %{downloadversion}
Source:                  ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz
URL:			 http://xmlsoft.org


%prep
%setup -q -n libxml2-%version
echo "pwd: "
pwd


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%{optflags} -I%{gnu_inc}"
export CXXFLAGS="%{cxx_optflags} -I%{gnu_inc}"
##TODO is this right/needed at all? -llzma
export LDFLAGS="%{_ldflags} -llzma %{gnu_lib_path}"

./configure --prefix=%{_prefix} \
                                    --sysconfdir=%{_sysconfdir} \
				    --bindir=%{_bindir} \
				    --libdir=%{_libdir} \
				    --libexecdir=%{_libexecdir} \
                                    --includedir=%{_includedir} \
%if %{opt_arch64}
                                    --without-python \
%endif
                                    --mandir=%{_mandir} \
                                    --disable-static
 
gmake -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
rm -f $RPM_BUILD_ROOT/%{_libdir}/xml2Conf.sh

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Sep  9 2012 - Thomas Wagner
- fix build
* Sat Sep  8 2012 - Thomas Wagner
- split out base-specs/lxml.spec for proper multiarch
