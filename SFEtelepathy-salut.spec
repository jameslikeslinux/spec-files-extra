#
# spec file for packages SFEtelepathy-salut
#
# includes module(s): telepathy-salut
#
%include Solaris.inc

%define	src_name	telepathy-salut

Name:		SFEtelepathy-salut
Summary:	Salut is a link-local XMPP (XEP-0174) connection manager
Version:	0.4.0
Group:		Internet
URL:		http://telepathy.freedesktop.org/
Source:		http://telepathy.freedesktop.org/releases/%{src_name}/%{src_name}-%{version}.tar.gz
Patch1:		telepathy-salut-01-sunstudio.diff
Patch2:		telepathy-salut-02-solaris.diff
License:	LGPLv2.1
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SFEtelepathy-glib
BuildRequires: SFEtelepathy-glib-devel
Requires: SUNWavahi-bridge-dsd
BuildRequires: SUNWavahi-bridge-dsd-devel
Requires: SUNWlibsoup
BuildRequires: SUNWlibsoup-devel
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWgtk-doc
BuildRequires: SUNWlxsl
BuildRequires: SFEcheck

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1


%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lnsl -lsocket"
./configure --prefix=%{_prefix}	\
	--libexecdir=%{_libdir}	\
	--disable-debug		\
	--enable-gtk-doc


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# no section 8
install -d 0755 %{buildroot}%{_datadir}/man/man1m
for i in %{buildroot}%{_datadir}/man/man8/*.8
do
  base=`basename $i 8`
  name1m=${base}1m
  mv $i %{buildroot}%{_datadir}/man/man1m/${name1m}
done
rmdir %{buildroot}%{_datadir}/man/man8
for i in %{buildroot}%{_datadir}/man/*/*
do
  sed 's/(8)/(1M)/g' $i | sed '/^\.TH/s/ \"8\" / \"1M\" /g' > $i.new
  mv $i.new $i
done


%clean
rm -rf %{buildroot}


%files
%defattr (-, root, bin)
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/telepathy-salut
%{_datadir}/dbus-1/*
%{_datadir}/man/*
%{_datadir}/telepathy/*

%changelog
* Wed Feb 23 2011 - Milan Jurik
- initial spec
