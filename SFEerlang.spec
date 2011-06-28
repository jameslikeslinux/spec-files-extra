#
# spec file for package: SFEerlang
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

%include Solaris.inc
%define cc_is_gcc 1

%define SFEunixodbc      %(/usr/bin/pkginfo -q SUNWunixodbc && echo 0 || echo 1)

%define mybindir %{_bindir}
%ifarch amd64 sparcv9 
%include arch64.inc
%define myldflags -m64 %{_ldflags}
%define wx_config /usr/gnu/bin/%{_arch64}/wx-config
%use erlang_64 = erlang.spec
%endif
%include base.inc
%define myldflags %{_ldflags}
%define wx_config /usr/gnu/bin/wx-config
%if %can_isaexec
%define mybindir %{_bindir}/%{base_isa}
%endif
%use erlang = erlang.spec

Name:		SFEerlang
Version:	%{erlang.version}
Summary:	Erlang programming language and OTP libraries
License:	Erlang Public License
Distribution:   OpenSolaris
Vendor:         OpenSolaris Community
Url:		http://www.erlang.org/
SUNW_BaseDir:	/
SUNW_Copyright:	%{name}.copyright

Source0:	epmd.xml

%include default-depend.inc
BuildRequires:	SFEgcc
BuildRequires:	SUNWj6dev
BuildRequires:	SUNWopenssl-include
BuildRequires:	SUNWopenssl-libraries
BuildRequires:	SFEwxwidgets-gnu-devel
Requires:	SFEgccruntime
Requires:	SUNWopenssl-libraries
Requires:	SFEwxwidgets-gnu

%if %SFEunixodbc
BuildRequires: SFEunixodbc-devel
Requires: SFEunixodbc
%else
BuildRequires: SUNWunixodbc
Requires: SUNWunixodbc
%endif

Meta(info.maintainer):		James Lee <jlee@thestaticvoid.com>
Meta(info.upstream):		erlang-bugs@erlang.org
Meta(info.upstream_url):	http://www.erlang.org/
Meta(info.classification):	org.opensolaris.category.2008:Development/Other Languages

%description
Open Source Erlang is a functional programming language designed at the
Ericsson Computer Science Laboratory.

Some of Erlang main features are:

 * Clear declarative syntax and is largely free from side-effects;
 * Builtin support for real-time, concurrent and distributed programming;
 * Designed for development of robust and continously operated programs;
 * Dynamic code replacement at runtime.

The Erlang distribution also includes OTP (Open Telecom Platform) which
provides a reach set of libraries and applications. 

%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
%ifarch amd64 sparcv9
mkdir %{name}-%{version}/%{_arch64}
%erlang_64.prep -d %{name}-%{version}/%{_arch64}
%endif
mkdir %{name}-%{version}/%{base_arch}
%erlang.prep -d %{name}-%{version}/%{base_arch}

%build
%ifarch amd64 sparcv9
%erlang_64.build -d %{name}-%{version}/%{_arch64}
%endif
%erlang.build -d %{name}-%{version}/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%erlang_64.install -d %{name}-%{version}/%{_arch64}
%endif
%erlang.install -d %{name}-%{version}/%{base_arch}

%if %can_isaexec
cd $RPM_BUILD_ROOT%{_bindir}
for i in dialyzer epmd erl erlc escript run_erl run_test to_erl typer; do
	ln -s ../lib/isaexec $i
done
%endif

rm -rf $RPM_BUILD_ROOT%{_datadir}/info

# copy epmd SMF manifest
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/svc/manifest/network
cp %{SOURCE0} $RPM_BUILD_ROOT%{_localstatedir}/svc/manifest/network/epmd.xml

%clean
rm -rf $RPM_BUILD_ROOT

%if %(test -f /usr/sadm/install/scripts/i.manifest && echo 0 || echo 1)
%iclass manifest -f i.manifest
%endif

%files
%defattr(-,root,bin)
%ifarch amd64 sparcv9
%{_bindir}/%{_arch64}/dialyzer
%{_bindir}/%{_arch64}/epmd
%{_bindir}/%{_arch64}/erl
%{_bindir}/%{_arch64}/erlc
%{_bindir}/%{_arch64}/escript
%{_bindir}/%{_arch64}/run_erl
%{_bindir}/%{_arch64}/run_test
%{_bindir}/%{_arch64}/to_erl
%{_bindir}/%{_arch64}/typer
%{_libdir}/%{_arch64}/erlang
%endif
%if %can_isaexec
%{_bindir}/%{base_isa}/dialyzer
%{_bindir}/%{base_isa}/epmd
%{_bindir}/%{base_isa}/erl
%{_bindir}/%{base_isa}/erlc
%{_bindir}/%{base_isa}/escript
%{_bindir}/%{base_isa}/run_erl
%{_bindir}/%{base_isa}/run_test
%{_bindir}/%{base_isa}/to_erl
%{_bindir}/%{base_isa}/typer
%hard %{_bindir}/dialyzer
%hard %{_bindir}/epmd
%hard %{_bindir}/erl
%hard %{_bindir}/erlc
%hard %{_bindir}/escript
%hard %{_bindir}/run_erl
%hard %{_bindir}/run_test
%hard %{_bindir}/to_erl
%hard %{_bindir}/typer
%else
%{_bindir}/dialyzer
%{_bindir}/epmd
%{_bindir}/erl
%{_bindir}/erlc
%{_bindir}/escript
%{_bindir}/run_erl
%{_bindir}/run_test
%{_bindir}/to_erl
%{_bindir}/typer
%endif
%{_libdir}/erlang
%defattr(-,root,sys)
%dir %{_localstatedir}/svc/manifest/network
%class(manifest) %attr(444,root,sys) %{_localstatedir}/svc/manifest/network/epmd.xml

%changelog
* Tue Jun 28 2011 - James Lee <jlee@thestaticvoid.com>
- Add odbc dependency.
- Add epmd service.
* Wed Jun 15 2011 - James Lee <jlee@thetsaticvoid.com>
- Update for SFE inclusion
* Fri Jan 21 2011 - James Lee <jlee@thestaticvoid.com>
- Initial version
