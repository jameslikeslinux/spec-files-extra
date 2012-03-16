#
# NoCopyright 2009 - Gilles Dauphin 
#
#

%include Solaris.inc

%define texlive_ver	20110705

%define _texmf_dir /usr/texlive

Name:		SFEtexlive-texmf
IPS_Package_Name:	 text/texlive-texmf
Version:	%{texlive_ver}
Summary:	Binaries for the TeX formatting system
URL:		http://tug.org/texlive

Group:		Applications/Publishing
License:	GPLv2 and More
URL:		http://tug.org/texlive/

#Source:		http://mirror.ctan.org/systems/texlive/Source/texlive-%{texlive_ver}-source.tar.lzma
#Source:	http://rlworkman.net/pkgs/sources/12.2/texlive/texlive-20080816-source.tar.bz2
# take care it's big
Source:         ftp://tug.org/historic/systems/texlive/2011/texlive-%{texlive_ver}-texmf.tar.xz

BuildRoot:	%{_tmppath}/%{name}-%{version}-build

BuildRequires:	SUNWzlib
BuildRequires:	SUNWpng
BuildRequires: compress/xz

%description
TeXLive is an implementation of TeX for Linux or UNIX systems. TeX takes
a text file and a set of formatting commands as input and creates a
printable file as output. Usually, TeX is used in conjunction with
a higher level formatting package like LaTeX or PlainTeX, since TeX by
itself is not very user-friendly.

Install texlive if you want to use the TeX text formatting system. Consider
to install texlive-latex (a higher level formatting package which provides
an easier-to-use interface for TeX).

%prep
#%setup -q -c -n %{name}-%{version}
tar xJf %{SOURCE}

%build
set -x
cd texlive-%{version}-texmf
# keep english and french doc ( on est jamais mieux servi que par ...)
rm -rf texmf-doc/doc/bulgarian
rm -rf texmf-doc/doc/czechslovak
rm -rf texmf-doc/doc/dutch
rm -rf texmf-doc/doc/finnish
rm -rf texmf-doc/doc/italian
rm -rf texmf-doc/doc/mongolian
rm -rf texmf-doc/doc/polish
rm -rf texmf-doc/doc/portuguese
rm -rf texmf-doc/doc/slovak
rm -rf texmf-doc/doc/slovenian
rm -rf texmf-doc/doc/spanish
rm -rf texmf-doc/doc/thai
rm -rf texmf-doc/doc/turkish
rm -rf texmf-doc/doc/ukrainian
rm -rf texmf-doc/doc/vietnamese
# done in SFEtexlive.spec
rm texmf/dvipdfmx/dvipdfmx.cfg 
rm texmf/web2c/texmf.cnf
rm texmf/xdvi/XDvi
rm texmf/xdvi/xdvi.cfg
rm texmf-dist/scripts/tex4ht/ht.sh
rm texmf-dist/scripts/tex4ht/mk4ht.pl
#
rm -f texmf-dist/scripts/bengali/ebong.py
rm -f texmf-dist/scripts/context/ruby/texmfstart.rb
rm -f texmf-dist/scripts/context/stubs/unix/context
rm -f texmf-dist/scripts/context/stubs/unix/ctxtools
rm -f texmf-dist/scripts/context/stubs/unix/exatools
rm -f texmf-dist/scripts/context/stubs/unix/luatools
rm -f texmf-dist/scripts/context/stubs/unix/makempy
rm -f texmf-dist/scripts/context/stubs/unix/mpstools
rm -f texmf-dist/scripts/context/stubs/unix/mptopdf
rm -f texmf-dist/scripts/context/stubs/unix/mtxrun
rm -f texmf-dist/scripts/context/stubs/unix/mtxtools
rm -f texmf-dist/scripts/context/stubs/unix/pdftools
rm -f texmf-dist/scripts/context/stubs/unix/pdftrimwhite
rm -f texmf-dist/scripts/context/stubs/unix/pstopdf
rm -f texmf-dist/scripts/context/stubs/unix/rlxtools
rm -f texmf-dist/scripts/context/stubs/unix/runtools
rm -f texmf-dist/scripts/context/stubs/unix/texexec
rm -f texmf-dist/scripts/context/stubs/unix/texfind
rm -f texmf-dist/scripts/context/stubs/unix/texfont
rm -f texmf-dist/scripts/context/stubs/unix/texshow
rm -f texmf-dist/scripts/context/stubs/unix/textools
rm -f texmf-dist/scripts/context/stubs/unix/texutil
rm -f texmf-dist/scripts/context/stubs/unix/tmftools
rm -f texmf-dist/scripts/context/stubs/unix/xmltools
rm -f texmf-dist/scripts/dviasm/dviasm.py
rm -f texmf-dist/scripts/epspdf/epspdf
rm -f texmf-dist/scripts/epspdf/epspdftk
rm -f texmf-dist/scripts/glossaries/makeglossaries
rm -f texmf-dist/scripts/mkjobtexmf/mkjobtexmf.pl
rm -f texmf-dist/scripts/oberdiek/pdfatfi.pl
rm -f texmf-dist/scripts/pdfcrop/pdfcrop.pl
rm -f texmf-dist/scripts/perltex/perltex.pl
rm -f texmf-dist/scripts/ppower4/pdfthumb.texlua
rm -f texmf-dist/scripts/ppower4/ppower4.texlua
rm -f texmf-dist/scripts/pst-pdf/ps4pdf
rm -f texmf-dist/scripts/pst2pdf/pst2pdf.pl
rm -f texmf-dist/scripts/tex4ht/htcontext.sh
rm -f texmf-dist/scripts/tex4ht/htlatex.sh
rm -f texmf-dist/scripts/tex4ht/htmex.sh
rm -f texmf-dist/scripts/tex4ht/httex.sh
rm -f texmf-dist/scripts/tex4ht/httexi.sh
rm -f texmf-dist/scripts/tex4ht/htxelatex.sh
rm -f texmf-dist/scripts/tex4ht/htxetex.sh
rm -f texmf-dist/scripts/texcount/TeXcount.pl
rm -f texmf-dist/scripts/thumbpdf/thumbpdf.pl
rm -f texmf-dist/scripts/vpe/vpe.pl
rm -f texmf/doc/bibtex8/00readme.txt
rm -f texmf/doc/bibtex8/HISTORY
rm -f texmf/doc/bibtex8/csfile.txt
rm -f texmf/doc/bibtex8/file_id.diz
rm -f texmf/doc/tetex/TETEXDOC.pdf
rm -f texmf/doc/tetex/teTeX-FAQ
rm -f texmf/dvips/base/color.pro
rm -f texmf/dvips/base/crop.pro
rm -f texmf/dvips/base/finclude.pro
rm -f texmf/dvips/base/hps.pro
rm -f texmf/dvips/base/special.pro
rm -f texmf/dvips/base/tex.pro
rm -f texmf/dvips/base/texc.pro
rm -f texmf/dvips/base/texps.pro
rm -f texmf/dvips/gsftopk/render.ps
rm -f texmf/scripts/a2ping/a2ping.pl
rm -f texmf/scripts/epstopdf/epstopdf.pl
rm -f texmf/scripts/pkfix/pkfix.pl
rm -f texmf/scripts/ps2eps/ps2eps.pl
rm -f texmf/scripts/simpdftex/simpdftex
rm -f texmf/scripts/tetex/e2pall.pl
rm -f texmf/scripts/tetex/texdoctk.pl
rm -f texmf/scripts/texlive/getnonfreefonts.pl
rm -f texmf/scripts/texlive/rungs.tlu
rm -f texmf/scripts/texlive/texdoc.tlu
rm -f texmf/texconfig/README
rm -f texmf/texconfig/g/generic
rm -f texmf/texconfig/generic
rm -f texmf/texconfig/tcfmgr
rm -f texmf/texconfig/tcfmgr.map
rm -f texmf/texconfig/v/vt100
rm -f texmf/texconfig/x/xterm
rm -f texmf/web2c/mktex.opt
rm -f texmf/web2c/mktexdir
rm -f texmf/web2c/mktexdir.opt
rm -f texmf/web2c/mktexnam
rm -f texmf/web2c/mktexnam.opt
rm -f texmf/web2c/mktexupd
rm -f texmf/xdvi/pixmaps/toolbar.xpm
rm -f texmf/xdvi/pixmaps/toolbar2.xpm
# keep here
# texmf/scripts/texlive/tlmgr.pl
# texmf/web2c/fmtutil.cnf



%install
rm -rf ${RPM_BUILD_ROOT}
cd texlive-%{version}-texmf

mkdir -p ${RPM_BUILD_ROOT}/usr/texlive
mv * ${RPM_BUILD_ROOT}/usr/texlive

%clean
rm -rf ${RPM_BUILD_ROOT}


%files
%defattr (-,root,bin)
%dir %attr (0755, root, sys) /usr
# config files
%dir %attr (0755, root, bin) %{_texmf_dir}
%{_texmf_dir}/*

%changelog
* Thu Mar 15 2012 - Logan Bruns <logan@gedanken.org>
- update to 20110705 
* Aug 2009 - Gilles Dauphin
- Initial setup .
