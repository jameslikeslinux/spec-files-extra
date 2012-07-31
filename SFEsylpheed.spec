#
# spec file for package SUNWsylpheed
#

%include Solaris.inc

%define src_name        sylpheed
#note: download path changes with beta versions
%define src_url         http://sylpheed.sraoss.jp/sylpheed/v3.1


Name:                     SFEsylpheed
IPS_Package_Name:	mail/sylpheed
Summary:                  A GTK+ based, lightweight, and fast e-mail client
Version:                  3.1.2
Group:		Applications/Internet
Source:                   %{src_url}/%{src_name}-%{version}.tar.bz2
License:                  GPLv2+ with openSSL exception
URL:                      http://sylpheed.sraoss.jp/
SUNW_BaseDir:  %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_Copyright:		  sylpheed.copyright
%include default-depend.inc

#what is the build-req. for SUNWlibmsr?? BuildRequires: 
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWopenssl-include
Requires: SUNWlibmsr
Requires: SUNWgnome-base-libs
Requires: SUNWopenssl-libraries


#descriton taken from original sylpheed.spec file:
%description
Sylpheed is an e-mail client (and news reader) based on GTK+, running on
X Window System, and aiming for
 * Quick response
 * Simple, graceful, and well-polished interface
 * Easy configuration
 * Intuitive operation
 * Abundant features
The appearance and interface are similar to some popular e-mail clients for
Windows, such as Outlook Express, Becky!, and Datula. The interface is also
designed to emulate the mailers on Emacsen, and almost all commands are
accessible with the keyboard.

The messages are managed by MH format, and you'll be able to use it together
with another mailer based on MH format (like Mew). You can also utilize
fetchmail or/and procmail, and external programs on receiving (like inc or
imget).

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n %{src_name}-%{version}


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}          \
            --bindir=%{_bindir}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --datadir=%{_datadir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --disable-gtkspell		\
            --enable-shared             \
            --disable-static


make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
install -m 644 *.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc AUTHORS COPYING COPYING.LIB ChangeLog ChangeLog.ja ChangeLog-1.0 ChangeLog-1.0.ja README README.es README.ja INSTALL INSTALL.ja NEWS NEWS-1.0 NEWS-2.0 LICENSE TODO TODO.ja
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/%{src_name}
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}/faq/*/*
%{_datadir}/%{src_name}/manual/*/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*.png
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Sep 14 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 3.1.2
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Mon Jun 6 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 3.1.1
* Sat Apr 16 2011 - Alex Viskovatoff
- bump to 3.1.0
* Thu Oct 16 2009 - Dick Hoogendijk
- update to 2.7.1 stable
* Thu Jan 1 2009 - Dick Hoogendijk
- update to the stable 2.6 release
* Thu Jul 3 2008 - Dick Hoogendijk
- update to the stable 2.5 release
* Mon May 12 2008 - Thomas Wagner
- inital spec including base-specs/syhlpeed.spec from the tarball
