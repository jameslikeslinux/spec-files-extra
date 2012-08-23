#
# spec file for package: opengrok
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# include module(s): opengrok

%include Solaris.inc
%define _jardir %{_datadir}/lib/java
%define src_name opengrok

Name:		SFEopengrok
Summary:	Very fast indexing and searching software.
Version:	0.10
License:	CDDL
Source:		http://hub.opensolaris.org/bin/download/Project+opengrok/files/%{src_name}-%{version}-src.tar.gz
URL:		http://opensolaris.org/os/project/opengrok/
Group:		Developer/Tool
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:	%{_basedir}
SUNW_Copyright:	%{src_name}.copyright

%include default-depend.inc
BuildRequires:	SUNWj6dev 
BuildRequires:	SUNWant 
BuildRequires:	SFEjflex
BuildRequires:	SUNWxcu4
BuildRequires:	SFEctags
Requires:	SUNWj6rt
Requires:	SFEctags
Requires:	%name-root
Requires:	SUNWtcatu

%description
Wicked fast source code indexing and search software OpenGrok is a fast and usable source code search and cross reference engine, written in Java on top of lucene. It helps you search, cross-reference and navigate your source tree. It can understand various program file formats and version control histories like Mercurial, SCCS, RCS, CVS and Subversion.

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%prep
rm -rf %{src_name}-%{version}-src
%setup -q -n %{src_name}-%{version}-src

%build
ant -lib %{_jardir}:/usr/share/java

%install
rm -rf $RPM_BUILD_ROOT
# copy the files to the RPM_BUILD_ROOT

%define _opengrokdir %{_datadir}/opengrok
%define _opengroklibdir %{_opengrokdir}/lib

install -d $RPM_BUILD_ROOT%{_jardir}
install -d $RPM_BUILD_ROOT%{_opengrokdir}
install -d $RPM_BUILD_ROOT%{_opengroklibdir}
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}/doc
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}/conf
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}/tools

cp -p dist/opengrok.jar $RPM_BUILD_ROOT%{_opengrokdir}/%{opengrok}.jar
ln -s %{opengrok}.jar $RPM_BUILD_ROOT%{_opengrokdir}/opengrok.jar
ln -s ../../opengrok/%{opengrok}.jar $RPM_BUILD_ROOT%{_jardir}/opengrok.jar
cp -p dist/source.war $RPM_BUILD_ROOT%{_opengrokdir}
# below is our own fork ... we should probably build it together with the rest
cp -p dist/lib/*.jar $RPM_BUILD_ROOT%{_opengroklibdir}
cp platform/solaris/smf/ogindexd $RPM_BUILD_ROOT%{_opengroklibdir}

cp -rp README.txt $RPM_BUILD_ROOT%{_docdir}/%{name}
cp -rp doc/EXAMPLE.txt $RPM_BUILD_ROOT%{_docdir}/%{name}/doc
cp -rp OpenGrok $RPM_BUILD_ROOT%{_docdir}/%{name}
cp -rp run.sh $RPM_BUILD_ROOT%{_docdir}/%{name}
cp -rp tools/* $RPM_BUILD_ROOT%{_docdir}/%{name}/tools/

# install smf manifest
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/svc/manifest/site
cp platform/solaris/smf/opengrok.xml $RPM_BUILD_ROOT%{_localstatedir}/svc/manifest/site/%{src_name}.xml
mkdir -p $RPM_BUILD_ROOT/lib/svc/method
cp platform/solaris/smf/svc-opengrok $RPM_BUILD_ROOT/lib/svc/method/svc-opengrok

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_jardir}
%{_opengrokdir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{name}


%files root
%defattr (-, root, sys)
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%attr (0555, root, bin) /lib/svc/method/svc-opengrok
%dir %attr (0755, root, sys) %{_localstatedir}
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/site/%{src_name}.xml


%changelog
* Sat Jul 30 2011 - Milan Jurik
- moved from jucr, needs more work
* Mon Apr 20 2009 - Lubos.Kosco@Sun.COM
- initial version
* Fri Nov 06 2009 - Lubos.Kosco@Sun.COM
- getting ready for new opengrok version
* Fri Jan 15 2010 - Lubos.Kosco@Sun.COM
- opengrok version 0.8.1
