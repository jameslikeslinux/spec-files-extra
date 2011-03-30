# place defines to match older packages here - this include file is the first of a series
# 

##TODO## list
#see below, handle /var/sadm/pkg/SUNWruby18r /var/sadm/pkg/SUNWruby18u

# there are very old build out there, we might not need
# to write special logic for builds older then build 81
# at least we should have logic for build 111 (or 101)
# and younger (there are lots of installs out there)

# normally packages are not too much fragmented into
# subpackages. (exception: openssl where we simply
# require all sub packages to keep things easy)

# in general:
#    pnm_buildrequires_packagenames     packagename-devel (on this special range of builds, -devel 
#                                                          if that exists, else just the package name)
#         pnm_requires_packagenames     packagename (on this special range of builds)

# note: the right hand side changes depending on the range of the build number where the include
# file is intended for. the left hand side always lists the package names in currently three
# variants: old SVR4 from SolarisExpress/early or OS2008/OS2009 the early OpenSolaris IPS based
# then the names on OpenSolaris IPS-base without the SUNW prefix and before the big renaming
# around build 133/134


# below this section will be overwritten by the include files for the later builds
# it is there so support build machines with osbuild < 133 or < 134
# but the spec file shave been written with package names presen on
# machines with newer osbuild / after the big package renaming bang

#note defines below will be overwritten with a new target package name
#because it got renamed by the two big renaming projects, 
#starting with build ??? and build 133/134 
#openssl is always a special case since sub packages got combined
#below: our target system is an IPS based OS2008/OS2009/OS2010 
#         *before the big package renaming party*
##TODO## check osbuilds 129 .. 135 to be fully covered! Else run
# pkgtool --interactive prep base-specs/packagenamemacros.spec
# and mail us the output
#note name aliasing the package on build say "< 133" should work
#cases os2nnn
%if %{os2nnn}
%define pnm_buildrequires_SUNWopenssl			SUNWopenssl
%define pnm_buildrequires_SUNWopenssl_include           SUNWopenssl
#handy alias based on typo
%define pnm_buildrequires_SUNWopenssl_includes		SUNWopenssl
%define pnm_buildrequires_SUNWopenssl_commands		SUNWopenssl
%define pnm_buildrequires_SUNWopenssl_libraries		SUNWopenssl
%define pnm_buildrequires_SUNWopensslr			SUNWopenssl

%define pnm_requires_SUNWopenssl			SUNWopenssl
%define pnm_requires_SUNWopenssl_include		SUNWopenssl
#handy alias based on typo
%define pnm_requires_SUNWopenssl_includes		SUNWopenssl
%define pnm_requires_SUNWopenssl_commands		SUNWopenssl
%define pnm_requires_SUNWopenssl_libraries		SUNWopenssl
%define pnm_requires_SUNWopensslr			SUNWopenssl

%define pnm_buildrequires_openssl			SUNWopenssl
%define pnm_requires_openssl				SUNWopenssl

%define pnm_buildrequires_library_security_openssl	SUNWopenssl
%define pnm_requires_library_security_openssl		SUNWopenssl

#SUNWwgetu/SUNWwgetr/SUNWwget wget web/wget
%define pnm_buildrequires_web_wget			SUNWwget
%define pnm_requires_web_wget				SUNWwget
%define pnm_buildrequires_wget				SUNWwget
%define pnm_requires_wget				SUNWwget
%define pnm_buildrequires_SUNWwgetu			SUNWwget
%define pnm_requires_SUNWwgetu				SUNWwget
%define pnm_buildrequires_SUNWwgetr			SUNWwget
%define pnm_requires_SUNWwgetr				SUNWwget
%define pnm_buildrequires_SUNWwget			SUNWwget
%define pnm_requires_SUNWwget				SUNWwget

#SUNWGtku/SUNWGtkr/SUNWGtk Gtk library/desktop/gtk1
%define pnm_buildrequires_library_desktop_gtk1		SUNWGtk
%define pnm_requires_library_desktop_gtk1		SUNWGtk
%define pnm_buildrequires_SUNWGtk_devel			SUNWGtk
%define pnm_buildrequires_SUNWGtk			SUNWGtk
%define pnm_requires_SUNWGtk				SUNWGtk
%define pnm_buildrequires_Gtk				SUNWGtk
%define pnm_requires_Gtk				SUNWGtk

%define pnm_requires_SUNWGtku				SUNWGtk
%define pnm_requires_SUNWGtkr				SUNWGtk

%endif
#END os2nnn

#IPS has a problem: pkg info SUNWopenssl says *not installed* but at the same
#time pkg info openssl (or library/security/openssl) says installed.
#this is problematic, since based on the SUNWopenssl alias name it is still
#tobe seen as *installed* - every package prerequisite check by the old
#compatibilty/alias name *is* *failing* then
#below: our target system is an IPS based OS2010++ ... incl. Oracle Solaris 11 Express
#         *AFTER the big package renaming party*
#note: target is "openssl" which is understood by 133/134++ releases as installed
#and still works with early opensolaris builds as well
##TODO## this is accumulative (see above %if %{os2nnn} w/o osbuild detection

#cases >=133 AND os2nnn
%if %{os2nnn}
##TODO## Re-visit this buildnumber, was this 133 or 134 ? (pkg info SUNWopenssl says not installed)
%if %( expr %{osbuild} '>=' 133 )
%define pnm_buildrequires_SUNWopenssl			library/security/openssl
%define pnm_buildrequires_SUNWopenssl_include           library/security/openssl
#handy alias based on typo
%define pnm_buildrequires_SUNWopenssl_includes		library/security/openssl
%define pnm_buildrequires_SUNWopenssl_includes		library/security/openssl
%define pnm_buildrequires_SUNWopenssl_commands		library/security/openssl
%define pnm_buildrequires_SUNWopenssl_libraries		library/security/openssl
%define pnm_buildrequires_SUNWopensslr			library/security/openssl

%define pnm_requires_SUNWopenssl			library/security/openssl
%define pnm_requires_SUNWopenssl_include		library/security/openssl
#handy alias based on typo
%define pnm_requires_SUNWopenssl_includes		library/security/openssl
%define pnm_requires_SUNWopenssl_commands		library/security/openssl
%define pnm_requires_SUNWopenssl_libraries		library/security/openssl
%define pnm_requires_SUNWopensslr			library/security/openssl

%define pnm_buildrequires_openssl			library/security/openssl
%define pnm_requires_openssl				library/security/openssl

%define pnm_buildrequires_library_security_openssl	library/security/openssl
%define pnm_requires_library_security_openssl		library/security/openssl


%define pnm_buildrequires_library_python_2_python_gnome_libs_26	library/python-2/python-gnome-libs-26
%define pnm_requires_library_python_2_python_gnome_libs_26	library/python-2/python-gnome-libs-26
%define pnm_buildrequires_SUNWgnome_python26_libs_devel	library/python-2/python-gnome-libs-26
%define pnm_requires_SUNWgnome_python26_libs_devel	library/python-2/python-gnome-libs-26
%define pnm_buildrequires_SUNWgnome_python26_libs	library/python-2/python-gnome-libs-26
%define pnm_requires_SUNWgnome_python26_libs		library/python-2/python-gnome-libs-26


#SUNWwgetu/SUNWwgetr/SUNWwget wget web/wget
%define pnm_buildrequires_web_wget			web/wget
%define pnm_requires_web_wget				web/wget
%define pnm_buildrequires_wget				web/wget
%define pnm_requires_wget				web/wget
%define pnm_buildrequires_SUNWwgetu			web/wget
%define pnm_requires_SUNWwgetu				web/wget
%define pnm_buildrequires_SUNWwgetr			web/wget
%define pnm_requires_SUNWwgetr				web/wget
%define pnm_buildrequires_SUNWwget			web/wget
%define pnm_requires_SUNWwget				web/wget

#SUNWGtku/SUNWGtkr/SUNWGtk Gtk library/desktop/gtk1
%define pnm_buildrequires_library_desktop_gtk1		library/desktop/gtk1
%define pnm_requires_library_desktop_gtk1		library/desktop/gtk1
%define pnm_buildrequires_SUNWGtk_devel			library/desktop/gtk1
%define pnm_buildrequires_SUNWGtk			library/desktop/gtk1
%define pnm_requires_SUNWGtk				library/desktop/gtk1
%define pnm_buildrequires_Gtk				library/desktop/gtk1
%define pnm_requires_Gtk				library/desktop/gtk1

%define pnm_requires_SUNWGtku				library/desktop/gtk1
%define pnm_requires_SUNWGtkr				library/desktop/gtk1

#os2nnn
%endif
#>=130
%endif
#END >=133 AND os2nnn    note: two closing endif

#separate packages for the various openssl pieces (libs, incclude, commands, ...)
#note: for running the build on SXCE we do *not* have the big bang package
#      rename project, so we have to define the target package names on SXCE
#below: our target system is an older build SolarisExpress (up to including 130)
%if %{SXCE}
#spec file orginates from a system/autor using the old package names with SUNW prefix
%define pnm_buildrequires_SUNWopenssl			SUNWopenssl-includes
%define pnm_requires_SUNWopenssl			SUNWopenssl-libraries

%define pnm_buildrequires_openssl			SUNWopenssl-includes
%define pnm_requires_openssl				SUNWopenssl-libraries

%define pnm_buildrequires_library_security_openssl	SUNWopenssl-includes
%define pnm_requires_library_security_openssl		SUNWopenssl-libraries

%define pnm_buildrequires_SUNWopenssl_includes		SUNWopenssl-includes
%define pnm_requires_SUNWopenssl_includes		SUNWopenssl-includes
%define pnm_buildrequires_SUNWopenssl_libraries		SUNWopenssl-libraries
%define pnm_requires_SUNWopenssl_libraries		SUNWopenssl-libraries

##TODO##
#/var/sadm/pkg/SUNWruby18r
#/var/sadm/pkg/SUNWruby18u

#SUNWwgetu/SUNWwgetr/SUNWwget wget web/wget
%define pnm_buildrequires_web_wget			SUNWwgetu
%define pnm_requires_web_wget				SUNWwgetu
%define pnm_buildrequires_wget				SUNWwgetu
%define pnm_requires_wget				SUNWwgetu
%define pnm_buildrequires_SUNWwget			SUNWwgetu
%define pnm_requires_SUNWwget				SUNWwgetu
%define pnm_buildrequires_SUNWwgetu			SUNWwgetu
%define pnm_requires_SUNWwgetu				SUNWwgetu
%define pnm_buildrequires_SUNWwgetr			SUNWwgetr
%define pnm_requires_SUNWwgetr				SUNWwgetr

#SUNWGtku/SUNWGtkr/SUNWGtk Gtk library/desktop/gtk1
%define pnm_buildrequires_library_desktop_gtk1		SUNWGtku
%define pnm_requires_library_desktop_gtk1		SUNWGtku
%define pnm_buildrequires_SUNWGtk_devel			SUNWGtku
%define pnm_buildrequires_SUNWGtk			SUNWGtku
%define pnm_requires_SUNWGtk				SUNWGtku
%define pnm_buildrequires_Gtk				SUNWGtku
%define pnm_requires_Gtk				SUNWGtku

%define pnm_requires_SUNWGtku				SUNWGtku
%define pnm_requires_SUNWGtkr				SUNWGtkr


#SUNWghostscriptu/SUNWghostscriptr/SUNWghostscript -> use always SUNWghostscriptu on SXCE
#ghostscript and print/filter/ghostscript
%define pnm_buildrequires_print_filter_ghostscript	SUNWghostscriptu
%define pnm_requires_print_filter_ghostscript		SUNWghostscriptu
%define pnm_buildrequires_ghostscript			SUNWghostscriptu
%define pnm_requires_ghostscript			SUNWghostscriptu
#never existed SUNWghostscript_devel
%define pnm_buildrequires_SUNWghostscript		SUNWghostscriptu
%define pnm_requires_SUNWghostscript			SUNWghostscriptu
%define pnm_buildrequires_SUNWghostscriptr		SUNWghostscriptr
%define pnm_requires_SUNWghostscriptr			SUNWghostscriptr
%define pnm_buildrequires_SUNWghostscriptu		SUNWghostscriptu
%define pnm_requires_SUNWghostscriptu			SUNWghostscriptu
%endif
#END SXCE

#note: for simple cases don't open another separate include file
#packagenames.define-133.inc or packagenames.define-specialcases-133.inc
#just do it here instead.
#package names in sync with SXCE and os2nnn but got incorporated into other
#packages, examples. SUNWhea SUNWsfwhea

#pre/including nnn: SUNWhea    -> past nnn replacement is
#NOTE: superseeding the previous definitions SUNWsfwhea
#cases >=133
%define pnm_buildrequires_SUNWhea	    system/header
%define pnm_requires_SUNWhea		    system/header
%define pnm_buildrequires_system_header	    system/header
%define pnm_requires_system_header	    system/header
#>=133

#NOTE: this section might be superseeded by lower build numbers 
#cases <133
%if %( expr %{osbuild} '<' 133 )
%define pnm_buildrequires_SUNWhea		SUNWhea
%define pnm_requires_SUNWhea	 		SUNWhea
#this might be overwritten again by builds below 130
%define pnm_buildrequires_system_header		SUNWhea
%define pnm_requires_system_header		SUNWhea
%endif
#END <133

#pre/including 130: SUNWsfwhea -> past 130 replacement is system/header
##TODO## please verify build numbers and intended replacement packagename
%define pnm_buildrequires_SUNWsfwhea	    system/header
%define pnm_requires_SUNWsfwhea		    system/header
%define pnm_buildrequires_system_header	    system/header
%define pnm_requires_system_header	    system/header

#NOTE: including SUNWhea too
#cases <130
%if %( expr %{osbuild} '<' 130 )
%define pnm_buildrequires_SUNWhea		SUNWsfwhea
%define pnm_requires_SUNWhea	 		SUNWsfwhea
%define pnm_buildrequires_SUNWsfwhea		SUNWsfwhea
%define pnm_requires_SUNWsfwhea	 		SUNWsfwhea
%define pnm_buildrequires_system_header		SUNWsfwhea
%define pnm_requires_system_header		SUNWsfwhea
%endif
#END <130


#SPECIAL CASE: SFE package was replacved with a SUNW package - one day this will
#be migrated to translation table in an exteral file
#with one build number the SUNWsane-backend was added, so SFEsane-backends was deleted (oh!)
#just replace the SFEsane-backends starting with that build-number with the SUNWsane-backend
#or the package-rename-project's new name
#http://opensolaris.org/jive/thread.jspa?threadID=62982  -->> snv90 introduced SUNWsane-backend

#default: nothing to do for the SUNW variants, pkg / IPS knows about 
#the SUNWsane-backend replacement image/scanner/xsane/sane-backends
#cases >91
%define pnm_buildrequires_SFEsane_backend_devel		SUNWsane-backend-devel
%define pnm_requires_SFEsane_backend	 		SUNWsane-backend
%define pnm_buildrequires_SUNWsane_backend_devel		SUNWsane-backend-devel
%define pnm_requires_SUNWsane_backend	 		SUNWsane-backend
%define pnm_buildrequires_image_scanner_xsane_sane_backends	SUNWsane-backend-devel
%define pnm_requires_image_scanner_xsane_sane_backends 		SUNWsane-backend
#>91

#we need SFE version on very old builds
%if %( expr %{osbuild} '<=' 90 )
#running an old build or Solaris 10
%define pnm_buildrequires_SFEsane_backend_devel		SFEsane-backend-devel
%define pnm_requires_SFEsane_backend	 		SFEsane-backend
%define pnm_buildrequires_SUNWsane_backend_devel	SFEsane-backend-devel
%define pnm_requires_SUNWsane_backend	 		SFEsane-backend
%define pnm_buildrequires_image_scanner_xsane_sane_backends	SFEsane-backend-devel
%define pnm_requires_image_scanner_xsane_sane_backends 		SFEsane-backend
%endif
#END <=90

#SUNWfftw3 was added with build 107
#http://wikis.sun.com/display/OSOLInstall/Build+107
#pkgs know about the renaming, so just handle a switch to SFEfftw3 in case
#the osbuild is too old

#defaults for all builds >= 107 - let pkg do the names translation if needed
#cases >=107
%define pnm_buildrequires_SFEfftw3		SUNWfftw3
%define pnm_requires_SFEfftw3			SUNWfftw3
%define pnm_buildrequires_SUNWfftw3		SUNWfftw3
%define pnm_requires_SUNWfftw3	 		SUNWfftw3
%define pnm_buildrequires_library_fftw_3	SUNWfftw3
%define pnm_requires_library_fftw_3	 	SUNWfftw3
#>=107

%if %( expr %{osbuild} '<' 107 )
#running an old build or Solaris 10
%define pnm_buildrequires_SFEfftw3		SFEfftw3
%define pnm_requires_SFEfftw3	 		SFEfftw3
%define pnm_buildrequires_SUNWfftw3		SFEfftw3
%define pnm_requires_SUNWfftw3	 		SFEfftw3
%define pnm_buildrequires_library_fftw_3	SFEfftw3
%define pnm_requires_library_fftw_3	 	SFEfftw3
%endif
#END <107


#http://mail.opensolaris.org/pipermail/opensolaris-announce/2008-October.txt
#repo additions, SUNWlibmikmod

#defaults for all builds >= 99 - let pkg do the names translation if needed
%define pnm_buildrequires_SFElibmikmod		SUNWlibmikmod
%define pnm_requires_SFElibmikmod		SUNWlibmikmod
%define pnm_buildrequires_SUNWlibmikmod		SUNWlibmikmod
%define pnm_requires_SUNWlibmikmod		SUNWlibmikmod

%if %( expr %{osbuild} '<' 99 )
#running an old build or Solaris 10
%define pnm_buildrequires_SFElibmikmod		SFElibmikmod
%define pnm_requires_SFElibmikmod	 	SFElibmikmod
%define pnm_buildrequires_SUNWlibmikmod		SFElibmikmod
%define pnm_requires_SUNWlibmikmod	 	SFElibmikmod
%endif
#END <99

#defaults for all builds >= 116 - let pkg do the names translation if needed
%define pnm_buildrequires_SFEgdbm		SUNWgnu-dbm
%define pnm_requires_SFEgdbm			SUNWgnu-dbm
%define pnm_buildrequires_SUNWgnu_dbm		SUNWgnu-dbm
%define pnm_requires_SUNWgnu_dbm		SUNWgnu-dbm

%if %( expr %{osbuild} '<' 116 )
#running an old build or Solaris 10
%define pnm_buildrequires_SFEgdbm		SFEgdbm
%define pnm_requires_SFEgdbm		 	SFEgdbm
%define pnm_buildrequires_SUNWgnu_dbm		SFEgdbm
%define pnm_requires_SUNWgnu_dbm	 	SFEgdbm
%endif
#END <116


#packages no longer available, we could bail out or just require a core package
#to continue for now, we just set a already existing package name, the spec file 
#might fail compiling or have reduced functionality then -> up to the individual
#spec file maintainer how to solve that

#cases >=156
%if %( expr %{osbuild} '>=' 156 )
#https://defect.opensolaris.org/bz/attachment.cgi?id=4441
#(the attachment link from above is in: https://defect.opensolaris.org/bz/show_bug.cgi?id=17668)
%define pnm_buildrequires_library_python_2_python_pigment_26	SUNWcs
%define pnm_requires_library_python_2_python_pigment_26		SUNWcs
%define pnm_buildrequires_SUNWlibpigment			SUNWcs
%define pnm_buildrequires_SUNWlibpigment_devel			SUNWcs
%define pnm_buildrequires_SUNWlibpigment_python26		SUNWcs
%define pnm_buildrequires_SUNWlibpigment_python26_devel		SUNWcs
%define pnm_requires_SUNWlibpigment				SUNWcs
%define pnm_requires_SUNWlibpigment_devel			SUNWcs
%define pnm_requires_SUNWlibpigment_python26			SUNWcs
%define pnm_requires_SUNWlibpigment_python26_devel		SUNWcs

%endif
#END >=156

#place very special cases here, for instance in Solaris 10
##TODO## for a future version



%changelog
* Sat Mar 27 2011 - Thomas Wagner
- handle SUNWGtku/SUNWGtkr/SUNWGtk Gtk library/desktop/gtk1
* Sat Mar 19 2011 - Thomas Wagner
- handle more cases SUNWwgetu/SUNWwgetr/SUNWwget wget web/wget (>=133)
- make endifs pretty commented
- reduce "else" code paths by negating %if clauses (new build numbers have less %if clauses)
* Fri Mar 18 2011 - Thomas Wagner
- make libpigment a dummy because obsoleted/removed (>=156)
* Thr Mar 17 2011 - Thomas Wagner
- handle SUNWwgetu/SUNWwgetr/SUNWwget wget web/wget
- handle SUNWghostscriptu/SUNWghostscriptr/SUNWghostscript ghostscript print/filter/ghostscript
- handle more cases of SUNWopenssl* (still incomplete)
- handle SFEgdbm or SUNWgnu-dbm (>=116)
* Wed Mar 16 2011 - Thomas Wagner
- improve/add support for pkg info SUNWopenssl reported as not installed (but renamed)
* Mon Feb 28 2011 - Thomas Wagner
- add alias ending on "s" helping with easy typos:
  pnm_buildrequires_SUNWopenssl_include / pnm_buildrequires_SUNWopenssl_includes (note the "s" at the end)
* Sun Feb  7 2011 - Thomas Wagner
- handle SFElibmodmod and SUNWlibmikmod (>=90)
* Wed Feb  2 2011 - Thomas Wagner
- handle SUNWsfehea and SUNWhea - system/header (>= 130, >= 133) (perl modules)
- handle SFEsane-backend | SUNWsane-backend (>= 90) make pnm*SUNWsane-backend 
  require SFEsane-backend below 90 (would need undelete of SFEsane-backend.spec)
- handle SFEfftw3 | SUNWfftw3 (>= 107)
* Sat Jun 12 2010 - Thomas Wagner
- initial include file
