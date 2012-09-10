# base-specs/xz.spec for SFExl.spec


Name:		SFExz
Version:	5.0.4
Summary:	LZMA utils
URL:		http://tukaani.org/xz
Source:		http://tukaani.org/xz/xz-%{version}.tar.bz2


%prep
%setup -q -c -n xz-%{version}


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

cd xz-%{version}
export CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64"
export CXXFLAGS="%{cxx_optflags} -D_FILE_OFFSET_BITS=64"
export LDFLAGS="%{_ldflags} -D_FILE_OFFSET_BITS=64"

./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir}         \
            --mandir=%{_mandir}                 \
            --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info          \
	    --disable-static			\
	    --disable-assembler

gmake -j$CPUS

%install
cd xz-%{version}
gmake install DESTDIR=${RPM_BUILD_ROOT}

%if %build_l10n
%else
[ -d $RPM_BUILD_ROOT%{_datadir}/locale ] && rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}


%changelog
* Sun Sep  9 2012 - Thomas Wagner
- split out base-specs/xz.spec for multiarch
