#
# spec file for package SFElibotr
#
# includes module(s): libotr
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define srcname libotr

Name:                    SFElibotr
IPS_Package_Name:	 library/security/libotr
Summary:                 libotr - Off-the-Record Messaging Library and Toolkit
Group:                   Utility
Version:                 3.2.0
URL:		         http://www.cypherpunks.ca/otr/
Source:		         http://www.cypherpunks.ca/otr/libotr-%version.tar.gz
License: 		 LGPL
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: system/library/security/libgcrypt

%description
This is a library and toolkit which implements Off-the-Record (OTR) Messaging.

OTR allows you to have private conversations over IM by providing:
 - Encryption
   - No one else can read your instant messages.
 - Authentication
   - You are assured the correspondent is who you think it is.
 - Deniability
   - The messages you send do _not_ have digital signatures that are
     checkable by a third party.  Anyone can forge messages after a
     conversation to make them look like they came from you.  However,
     _during_ a conversation, your correspondent is assured the messages
     he sees are authentic and unmodified.
 - Perfect forward secrecy
   - If you lose control of your private keys, no previous conversation
     is compromised.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# we don't need the utilities that are under GPL instead of LGPL (if
# we do they should be in a separate package.)
rm -rf $RPM_BUILD_ROOT/usr/share/man
rm -rf $RPM_BUILD_ROOT/usr/bin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libotr.*
%dir %attr (0755, root, bin) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/libotr.pc
%dir %attr (0755, root, bin) %{_includedir}/libotr
%{_includedir}/libotr/*.h
%dir %attr (0755, root, bin) %{_datadir}/aclocal
%{_datadir}/aclocal/libotr.m4

%changelog
* Thu Mar 1 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
