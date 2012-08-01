#
# spec file for package: sbcl
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s):
#

Name:		sbcl
Version:	1.0.49
Source0:	http://voxel.dl.sourceforge.net/sourceforge/sbcl/%{name}-%{version}-source.tar.bz2
Source1:	http://voxel.dl.sourceforge.net/sourceforge/sbcl/%{bindist}-binary.tar.bz2

%prep
%setup -q
bzip2 -dc %{SOURCE1} | tar -xf -

%build
%define unquoted_libdir %(echo %{_libdir})
sed 's@SBCL_PREFIX"/lib/sbcl/"@"%{unquoted_libdir}/sbcl/"@' src/runtime/runtime.c > src/runtime/runtime.c.new
mv -f src/runtime/runtime.c.new src/runtime/runtime.c
SBCL_ARCH=%{sbclarch} sh make.sh --prefix=%{_prefix} --xc-host="%{bindist}/src/runtime/sbcl --core %{bindist}/output/sbcl.core --disable-debugger --no-sysinit --no-userinit"

%install
INSTALL_ROOT=$RPM_BUILD_ROOT%{_prefix} sh install.sh

%clean
rm -rf $RPM_BUILD_ROOT
