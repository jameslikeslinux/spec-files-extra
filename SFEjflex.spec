#
# spec file for package: jflex
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# include module(s): jflex
#

%include Solaris.inc
%define _jardir %{_datadir}/lib/java

Name:		SFEjflex
Summary:	Lexical analyzer generator (also known as scanner generator) for Java
Version:	1.4.3
License:	GPL
Source:		http://jflex.de/jflex-%{version}.tar.gz
Patch1:		jflex-01-classpath.diff
Patch2:		jflex-02-buildxml.diff
URL:		http://jflex.de/
Group:		Development/Tools
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:	%{_basedir}

%include default-depend.inc
BuildRequires: SUNWj6dev 
BuildRequires: SUNWant 
BuildRequires: SUNWjunit
Requires: SUNWj6rt

%description
JFlex is a lexical analyzer generator (also known as scanner generator) 
for Java(tm), written in Java(tm). It is also a rewrite of the very useful 
tool JLex which was developed by Elliot Berk at Princeton University. 

JFlex is designed to work together with the LALR parser generator CUP 
by Scott Hudson, and the Java modification of Berkeley Yacc BYacc/J by 
Bob Jamison. It can also be used together with other parser generators 
like ANTLR or as a standalone tool. 
 
%prep
%setup -q -n jflex-%{version}
%patch1 -p0
%patch2 -p0

%build
(cd src; env \
#JAVA_HOME=$(JDK) \
#"ANT_HOME=$(ANTHOME)" \
ant -lib %{_jardir} jar )

%install
rm -rf $RPM_BUILD_ROOT
# copy the files to the RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_jardir}
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_docdir}/jflex

cp -p lib/JFlex.jar $RPM_BUILD_ROOT%{_jardir}/jflex-%{version}.jar
ln -s jflex-%{version}.jar $RPM_BUILD_ROOT%{_jardir}/JFlex.jar
cp -p bin/jflex $RPM_BUILD_ROOT%{_bindir}

cp -rp doc/* $RPM_BUILD_ROOT%{_docdir}/jflex
cp -rp examples $RPM_BUILD_ROOT%{_docdir}/jflex

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755,root,sys) %{_datadir}/lib
%{_jardir}
%dir %attr (0755,root,other) %{_docdir}
%{_docdir}/jflex

%changelog
* Wed Mar 16 2011 - Milan Jurik
- import to SFE
* Mon Apr 27 2009 - Lubos.Kosco@Sun.COM
- initial version

