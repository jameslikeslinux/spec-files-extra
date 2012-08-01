#
# spec file for package root
#
# Copyright 2011 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
Name:         root
License:      LGPL
Group:        Applications/Math
Version:      %{rootversion}
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      ROOT - toolkit for physics analysis
Source:       ftp://root.cern.ch/root/root_v%{version}.source.tar.gz
URL:          http://root.cern.ch/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%description
The ROOT system provides a set of OO frameworks with all the 
functionality needed to handle and analyze large amounts of data in 
a very efficient way. Having the data defined as a set of objects, 
specialized storage methods are used to get direct access to the 
separate attributes of the selected objects, without having to touch 
the bulk of the data. Included are histograming methods in an 
arbitrary number of dimensions, curve fitting, function evaluation, 
minimization, graphics and visualization classes to allow the easy 
setup of an analysis system that can query and process the data 
interactively or in batch mode, as well as a general parallel processing 
framework, PROOF, that can considerably speed up an analysis.


%prep
%setup -q -n root


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

# By setting _prefix, ROOT is compiled with static directory names
# You should not set the ROOTSYS environment variable
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
%if %with_roofit
            --enable-roofit		\
%endif
%if %with_python
            --enable-python		\
%endif
%if %with_pythia8
            --enable-pythia8		\
            --with-pythia8-incdir=%{_includedir}/pythia8.1 \
%endif
%if %with_mathmore
            --enable-mathmore		\
%endif
            --etcdir=%{_rootsysconfdir}

$MAKE -j$CPUS 

%install
$MAKE install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Wed Jan 18 2012 - James Choi
- Initial spec
