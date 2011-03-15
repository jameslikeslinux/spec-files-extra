#
# spec file for package: tmux
#
# Copyright 2010 Guido Berhoerster.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc
%define srcname tmux
%define _pkg_docdir %_docdir/%srcname

Name:           SFE%srcname
Summary:        Terminal multiplexer
Version:        1.4
License:        ISC ; BSD3c ; BSD 2-Clause
Url:            http://tmux.sourceforge.net/
Source:         %{sf_download}/tmux/%{srcname}-%{version}.tar.gz
# owner:gber date:2010-10-06 type:bug
# include netdb.h which defines MAXHOSTNAMELEN
Patch1:         tmux-01-include-netdb.h.diff
Group:          Applications/System Utilities
Distribution:   OpenIndiana
Vendor:         OpenIndiana Community
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:   %{_basedir}
%include default-depend.inc

Requires:       SFElibevent
BuildRequires:  SFElibevent

# OpenSolaris IPS Package Manifest Fields
Meta(info.upstream):            Nicholas Marriott <nicm@users.sf.net>
Meta(info.maintainer):          Guido Berhoerster <gber@openindiana.org>
Meta(info.repository_url):      http://tmux.cvs.sourceforge.net/viewvc/tmux/tmux/

%description
tmux is a terminal multiplexer: it enables a number of terminals (or windows),
each running a separate program, to be created, accessed, and controlled from a
single screen. tmux may be detached from a screen and continue running in the
background, then later reattached. tmux is intended to be a modern,
BSD-licensed alternative to programs such as GNU screen.

tmux uses a client-server model. The server holds multiple sessions and each
window is a independent entity which may be freely linked to multiple sessions,
moved between sessions and otherwise manipulated. Each session may be attached
to (display and accept keyboard input from) multiple clients.

%prep
%setup -q -n %{srcname}-%{version}
%patch1 -p1

%build
CPUS=$(psrinfo | awk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 %{buildroot}%{_bindir}
install -m 0755 tmux %{buildroot}%{_bindir}/tmux
install -d -m 755 %{buildroot}%{_mandir}/man1
install -m 0644 tmux.1 %{buildroot}%{_mandir}/man1/tmux.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%_bindir/tmux
%dir %attr (-, root, sys) %_datadir
%doc CHANGES FAQ NOTES TODO
%doc examples/screen-keys.conf examples/t-williams.conf examples/vim-keys.conf
%doc examples/h-boetes.conf examples/tmux.vim examples/n-marriott.conf
%doc %_mandir/man1/tmux.1


%changelog
* Mon Mar 14 2011 - Alex Viskovatoff
- Import spec from http://hg.openindiana.org/spec-files-oi-extra/
  installing in /usr and bumping to 1.4
* Wed Oct  6 2010 - gber@openindiana.org
- Initial version.
