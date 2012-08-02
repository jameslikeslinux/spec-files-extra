#
# spec file for package SFEluke
#
# includes module(s): luke
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc

%define srcname luke

Name:                    SFEluke
IPS_Package_Name:	 sfe/database/luke
Summary:                 Luke - Lucene Index Toolbox
Group:                   Utility
Version:                 3.5.0
URL:		         http://code.google.com/p/luke/
Source:		         http://%{srcname}.googlecode.com/files/%{srcname}all-%{version}.jar
License: 		 Apache License, Version 2.0
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: %pnm_requires_java_runtime_default

%description
Lucene is an Open Source, mature and high-performance Java search
engine. It is highly flexible, and scalable from hundreds to millions
of documents.

Luke is a handy development and diagnostic tool, which accesses
already existing Lucene indexes and allows you to display and modify
their content in several ways:

    browse by document number, or by term
    view documents / copy to clipboard
    retrieve a ranked list of most frequent terms
    execute a search, and browse the results
    analyze search results
    selectively delete documents from the index
    reconstruct the original document fields, edit them and re-insert to the index
    optimize indexes
    open indexes consisting of multiple parts, and located on Hadoop filesystem
    and much more... 

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
cp %{SOURCE} $RPM_BUILD_ROOT/usr/bin/luke
chmod 0755 $RPM_BUILD_ROOT/usr/bin/luke

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/luke

%changelog
* Fri Jun 8 2012 - Logan Bruns <logan@gedanken.org>
- Initial spec.
