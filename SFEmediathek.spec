#
# spec file for package SFEre2c
#

%include Solaris.inc

%define src_name  mediathek
%define subdir    mediathek

Name:                    SFEmediathek
Summary:                 mediathek - download TV broadcasters online offers, download podcasts
URL:                     http://mediathek.org/
Version:                 2.5.0
#      http://downloads.sourceforge.net/project/zdfmediathk/Mediathek/Mediathek%202.5.0/Mediathek_2.5.0.zip
Source:                  %{sf_download}/project/zdfmediathk/Mediathek/Mediathek\ %{version}/Mediathek_%{version}.zip
#      http://downloads.sourceforge.net/project/zdfmediathk/Mediathek/Mediathek%202.5.0/Kurzanleitung_2.5.0.pdf
Source2:                 %{sf_download}/project/zdfmediathk/Mediathek/Mediathek\ %{version}/Kurzanleitung_%{version}.pdf


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc

%description
Das Programm durchsucht die Mediathek verschiedener Sender (ARD, ZDF, Arte, 3Sat, MDR, NDR, ORF, SF), lädt Beiträge mit einem Programm eigener Wahl und kann Themen als Abos anlegen und neue Beiträge automatisch downloaden. Es gibt auch eine Möglichkeit, Podcast zu verwalten und zu Downloaden.


%prep
%setup -c -q -n %{src_name}-%version
cp -p %{SOURCE2} .

%build
#nothing to do

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p             $RPM_BUILD_ROOT%{_basedir}/lib/%{subdir}/
cp -p  Mediathek.jar $RPM_BUILD_ROOT%{_basedir}/lib/%{subdir}/
cp -pr lib/          $RPM_BUILD_ROOT%{_basedir}/lib/%{subdir}/
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
echo "java -jar "%{_basedir}/lib/%{subdir}/"Mediathek.jar" > $RPM_BUILD_ROOT%{_bindir}/%{src_name}
chmod a+rx $RPM_BUILD_ROOT%{_bindir}/%{src_name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc Kurzanleitung_%{version}.pdf
%dir %attr (0755, root, bin) %{_basedir}/lib/%{subdir}/
%{_basedir}/lib/%{subdir}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}


%changelog
* Fri Jul 15 2011 - Thomas Wagner
- bump to version 2.5.0
- new URLs
* Sun Apr 25 2010 - Thomas Wagner
- Initial spec
