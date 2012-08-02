#
# spec file for package SFEsdl-perl
#
# includes module(s): sdl-perl
#
%include Solaris.inc
%include packagenamemacros.inc

Name:                    SFEsdl-perl
IPS_Package_Name:	library/perl-5/sdl
Summary:                 SDL Perl is a multimedia binding for Perl, using the Simple DirectMedia Layer and OpenGL.
Version:                 1.20.0
Source:                  http://zarb.org/~gc/t/SDL_perl-%{version}.tar.gz
URL:                     http://sdl.perl.org/

# owner:alfred date:2009-01-12 type:bug
# https://sourceforge.net/tracker/index.php?func=detail&aid=2500626&group_id=11529&atid=361529
Patch1:                  sdl-perl-01-solaris.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
BuildRequires: %pnm_buildrequires_perl_default
BuildRequires:           SUNWlibsdl-devel
Requires:                SUNWlibsdl
BuildRequires:           SFEsdl-image-devel
Requires:                SFEsdl-image
BuildRequires:           SFEsdl-gfx-devel
Requires:                SFEsdl-gfx
BuildRequires:           SFEsdl-mixer-devel
Requires:                SFEsdl-mixer
BuildRequires:           SFEsdl-net-devel
Requires:                SFEsdl-net
BuildRequires:           SFEsdl-ttf-devel
Requires:                SFEsdl-ttf

%prep
%setup -q -n SDL_perl-%{version}
%patch1 -p1

%build
./configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -r $RPM_BUILD_ROOT/usr/perl5/5.12/lib/*/perllocal.pod

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_basedir}/perl5
%{_basedir}/perl5/*

%changelog
* Tue Nov 22 2011 - Thomas Wagner
- conflicting file (foomatic-* delivers in error as well) SFEperl-io-compress-zlib.spec
* Mon Oct 17 2011 - Milan Jurik
- add IPS package name
* Mon Apr 12 2010 - Milan Jurik
- adding missing SDL build deps
* Sun Apr 11 2010 - Milan Jurik
- adding missing build deps
* Mon Jan 12 2009 - alfred.peng@sun.com
- Initial version
