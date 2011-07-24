#
# spec file for package SFEhunspell
#
# includes module: hunspell
#

####				USING WITH EMACS			    ####
#
# NOTE: To use Hunspell under Emacs, at least Emacs 23 is required.
# NOTE: For some reason, unless Emacs is started from the command line, hunspell
# WILL NOT FIND THE DICTIONARIES.  Also, for languages other than English,
# ispell often fails, complaining of "misalignment".
# It is necessary to redefine ispell's dictionary definitions, which are
# intended for aspell.  For example, place this in your .emacs file:
#
# (setq ispell-dictionary-base-alist
#   '((nil ; default
#      "[A-Za-z]" "[^A-Za-z]" "[']" t ("-d" "en_US") nil utf-8)
#     ("english" ; US English
#      "[A-Za-z]" "[^A-Za-z]" "[']" t ("-d" "en_US") nil utf-8)
#     ("german"  ; FRG German
#      "[A-Za-zäöüßA-ZÄÖÜ]" "[^A-Za-zäöüßA-ZÄÖÜ]" "[']" t ("-d" "de_DE") nil utf-8)
#     ("french"
#      "[A-Za-zÀÂÆÇÈÉÊËÎÏÔÙÛÜàâçèéêëîïôùûü]" "[^a-zÀÂÆÇÈÉÊËÎÏÔÙÛÜàâçèéêëîïôùûü]"
#      "[']" t ("-d" "fr_FR") nil utf-8)
#     ("portugese" ; Brazilian Portugese
#      "[a-zàáâãçéêíóôõúüA-ZÀÁÂÃÇÉÊÍÓÔÕÚÜ]" "[^a-zàáâãçéêíóôõúüA-ZÀÁÂÃÇÉÊÍÓÔÕÚÜ]"
#      "" nil ("-d" "pt_BR") nil utf-8)
#     ("russian"
#      "[А-Яа-яёЁ]" "[^А-Яа-яёЁ]" "[']" t ("-d" "ru_RU") nil utf-8)
# ))
#
# (eval-after-load "ispell"
#   '(setq ispell-dictionary "english"
# 	 ispell-extra-args '("-a")
# 	 ispell-silently-savep t))
#
# (setq-default ispell-program-name "hunspell")


%include Solaris.inc
%define srcname hunspell

Name:		SFEhunspell
Summary:	Spell checker
URL:		http://hunspell.sourceforge.net
Vendor:		László Németh
Version:	1.3.2
License:	MPL 1.1/GPL 2.0/LGPL 2.1
Source:		http://downloads.sourceforge.net/%srcname/%srcname-%version.tar.gz
Patch1:		hunspell-01-dict-path.diff

%include default-depend.inc
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
BuildRequires:	SUNWgmake
BuildRequires:	SUNWaconf
BuildRequires:	SUNWgnu-automake-19
BuildRequires:	SFElibiconv-devel
BuildRequires:	SUNWncurses
Requires:	SUNWncurses
Requires:	SUNWgnu-readline
Requires:	SFElibiconv
Requires:	SUNWmyspell-dictionary-en

%package devel
Summary:	%summary - development files
SUNW_BaseDir:	%_basedir
%include default-depend.inc
Requires:	%name


%prep
%setup -q -n %srcname-%version
%patch1 -p1

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
export CFLAGS="%optflags"

export CXXFLAGS="%cxx_optflags -I/usr/include/ncurses"
export LIBS="-lsocket -lpthread -lCrun"
export LDFLAGS="%_ldflags %gnu_lib_path"
./configure --prefix=%_prefix --enable-threads=solaris --disable-static --with-ui --with-readline

gmake -j$CPUS


%install
rm -rf %buildroot

gmake install DESTDIR=%buildroot

rm -f %buildroot%_libdir/lib*a

%clean
rm -rf %buildroot


%files
%defattr (-, root, bin)
%_bindir/*
%_libdir/*.so*
%dir %attr (-, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/%srcname.pc
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/locale
%attr (-, root, other) %_datadir/locale/*
%_mandir

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_includedir
%_includedir/*


%changelog
* Sat Jul 23 2011 - Alex Viskovatoff
- Use SUNWncurses instead of SFEncursesw
* Fri Jun 10 2011 - Alex Viskovatoff <herzen@imap.cc>
- don't create separate IPS devel package
* Sun Apr  3 2011 - Alex Viskovatoff <herzen@imap.cc>
- bump to 1.3.2
* Wed Mar 23 2011 - Alex Viskovatoff
- bump to 1.3.1
* Fri Feb  4 2011 - Alex Viskovatoff
- update to 1.2.14
* Wed Nov 10 2010 - Alex Viskovatoff
- add another missing build dep; do not package static lib
- add patch to make Hunspell find dictionaries without depending on DICPATH
* Mon Nov 08 2010 - Milan Jurik
- add missing build dep
* Thu Oct 14 2010 - Alex Viskovatoff
- Initial spec
