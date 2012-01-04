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

#kerberos
%define pnm_buildrequires_service_security_kerberos_5  SUNWkrb
%define pnm_requires_service_security_kerberos_5       SUNWkrb

%define pnm_buildrequires_SUNWkrb 		SUNWkrb
%define pnm_buildrequires_SUNWkrbr		SUNWkrb
%define pnm_buildrequires_SUNWkrbu		SUNWkrb
%define pnm_requires_SUNWkrb                    SUNWkrb
%define pnm_requires_SUNWkrbr 			SUNWkrb
%define pnm_requires_SUNWkrbu 			SUNWkrb

#samba service/network/samba
%define pnm_buildrequires_service_network_samba	SUNWsmba
%define pnm_requires_service_network_samba	SUNWsmba
%define pnm_buildrequires_SUNWsmba_devel	SUNWsmba
%define pnm_buildrequires_SUNWsmba		SUNWsmba
%define pnm_buildrequires_SUNWsmbar		SUNWsmba
%define pnm_buildrequires_SUNWsmbau		SUNWsmba
%define pnm_requires_SUNWsmba			SUNWsmba
%define pnm_requires_SUNWsmbar			SUNWsmba
%define pnm_requires_SUNWsmbau			SUNWsmba
%define pnm_buildrequires_smba			SUNWsmba
%define pnm_requires_smba			SUNWsmba

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

#samba service/network/samba
%define pnm_buildrequires_service_network_samba		service/network/samba
%define pnm_requires_service_network_samba		service/network/samba
%define pnm_buildrequires_SUNWsmba_devel		service/network/samba
%define pnm_buildrequires_SUNWsmba			service/network/samba
%define pnm_buildrequires_SUNWsmbar			service/network/samba
%define pnm_buildrequires_SUNWsmbau			service/network/samba
%define pnm_requires_SUNWsmba				service/network/samba
%define pnm_requires_SUNWsmbar				service/network/samba
%define pnm_requires_SUNWsmbau				service/network/samba
%define pnm_buildrequires_smba				service/network/samba
%define pnm_requires_smba				service/network/samba

#>=133
%endif
#os2nnn
%endif
#END >=133 AND os2nnn    note: two closing endif

#separate packages for the various openssl pieces (libs, incclude, commands, ...)
#note: for running the build on SXCE we do *not* have the big bang package
#      rename project, so we have to define the target package names on SXCE
#below: our target system is an older build SolarisExpress (up to including 130)
%if %{SXCE}
#spec file orginates from a system/autor using the old package names with SUNW prefix
%define pnm_buildrequires_SUNWopenssl			SUNWopenssl-include
%define pnm_requires_SUNWopenssl			SUNWopenssl-libraries

%define pnm_buildrequires_openssl			SUNWopenssl-include
%define pnm_requires_openssl				SUNWopenssl-libraries

%define pnm_buildrequires_library_security_openssl	SUNWopenssl-include
%define pnm_requires_library_security_openssl		SUNWopenssl-libraries

#note: if you search for SUNWopenssl-include, use SUNWopenssl_include !!
%define pnm_buildrequires_SUNWopenssl_include		SUNWopenssl-include
%define pnm_requires_SUNWopenssl_include		SUNWopenssl-include
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

#Apache on a SXCE or S10  host

##ignored, too old SUNWapchd
##ignored, too old SUNWapchr
##ignored, too old SUNWapchu
#config files of modules are prerequisite to the modules, so only list modules here

%define pnm_buildrequires_SUNWapch22r 		SUNWapch22r
%define pnm_requires_SUNWapch22r		SUNWapch22r

%define pnm_buildrequires_SUNWapch22u		SUNWapch22u
%define pnm_requires_SUNWapch22u		SUNWapch22u

%define pnm_buildrequires_SUNWapch22		SUNWapch22u
%define pnm_requires_SUNWapch22			SUNWapch22u

%define pnm_buildrequires_apch22		SUNWapch22u
%define pnm_requires_apch22			SUNWapch22u

#doc
%define pnm_buildrequires_SUNWapch22d		SUNWapch22d
%define pnm_requires_SUNWapch22d		SUNWapch22d
%define pnm_buildrequires_apch22d		SUNWapch22d
%define pnm_requires_apch22d			SUNWapch22d

%define pnm_buildrequires_SUNWapch22m_dtrace	SUNWapch22m-dtrace
%define pnm_requires_SUNWapch22m_dtrace		SUNWapch22m-dtrace
%define pnm_buildrequires_apch22m_dtrace	SUNWapch22m-dtrace
%define pnm_requires_apch22m_dtrace		SUNWapch22m-dtrace

%define pnm_buildrequires_SUNWapch22m_fcgid	SUNWapch22m-fcgid
%define pnm_requires_SUNWapch22m_fcgid		SUNWapch22m-fcgid
%define pnm_buildrequires_apch22m_fcgid		SUNWapch22m-fcgid
%define pnm_requires_apch22m_fcgid		SUNWapch22m-fcgid

%define pnm_buildrequires_SUNWapch22m_proxy_html	SUNWapch22m-proxy-html
%define pnm_requires_SUNWapch22m_proxy_html	SUNWapch22m-proxy-html
%define pnm_buildrequires_apch22m_proxy_html	SUNWapch22m-proxy-html
%define pnm_requires_apch22m_proxy_html		SUNWapch22m-proxy-html

%define pnm_buildrequires_SUNWapch22m_php52	SUNWapch22m-php52
%define pnm_requires_SUNWapch22m_php52		SUNWapch22m-php52
%define pnm_buildrequires_apch22m_php52		SUNWapch22m-php52
%define pnm_requires_apch22m_php52		SUNWapch22m-php52

%define pnm_buildrequires_SUNWapch22m_security	SUNWapch22m-security
%define pnm_requires_SUNWapch22m_security	SUNWapch22m-security
%define pnm_buildrequires_apch22m_security	SUNWapch22m-security
%define pnm_requires_apch22m_security		SUNWapch22m-security

%define pnm_buildrequires_SUNWapch22m_sed	SUNWapch22m-sed
%define pnm_requires_SUNWapch22m_sed		SUNWapch22m-sed
%define pnm_buildrequires_apch22m_sed		SUNWapch22m-sed
%define pnm_requires_apch22m_sed		SUNWapch22m-sed

%define pnm_buildrequires_SUNWapch22m_jk	SUNWapch22m-jk
%define pnm_requires_SUNWapch22m_jk		SUNWapch22m-jk
%define pnm_buildrequires_apch22m_jk		SUNWapch22m-jk
%define pnm_requires_apch22m_jk			SUNWapch22m-jk

%define pnm_buildrequires_SUNWapch22m_xml2enc	SUNWapch22m-xml2enc
%define pnm_requires_SUNWapch22m_xml2enc	SUNWapch22m-xml2enc
%define pnm_buildrequires_apch22m_xml2enc	SUNWapch22m-xml2enc
%define pnm_requires_apch22m_xml2enc		SUNWapch22m-xml2enc

# php
#SUNWphp52d/          SUNWphp52r-mysql/    SUNWphp52r-xdebug/   SUNWphp52u-mysql/    SUNWphp52u-xdebug/
#SUNWphp52r/          SUNWphp52r-pear/     SUNWphp52u/          SUNWphp52u-pear/     
#SUNWphp52r-apc/      SUNWphp52r-pgsql/    SUNWphp52u-apc/      SUNWphp52u-pgsql/    
#SUNWphp52r-idn/      SUNWphp52r-suhosin/  SUNWphp52u-idn/      SUNWphp52u-suhosin/  
#SUNWphp52r-memcache/ SUNWphp52r-tcpwrap/  SUNWphp52u-memcache/ SUNWphp52u-tcpwrap/  


%define pnm_buildrequires_SUNWphp52u		SUNWphp52u
%define pnm_requires_SUNWphp52u			SUNWphp52u
%define pnm_buildrequires_SUNWphp52		SUNWphp52u
%define pnm_requires_SUNWphp52			SUNWphp52u

%define pnm_buildrequires_SUNWphp52r		SUNWphp52r
%define pnm_requires_SUNWphp52r			SUNWphp52r

%define pnm_buildrequires_SUNWphp52d		SUNWphp52d
%define pnm_requires_SUNWphp52d			SUNWphp52d


%define pnm_buildrequires_SUNWphp52r_mysql	SUNWphp52r-mysql
%define pnm_requires_SUNWphp52r_mysql		SUNWphp52r-mysql

%define pnm_buildrequires_SUNWphp52u_mysql	SUNWphp52u-mysql
%define pnm_requires_SUNWphp52u_mysql		SUNWphp52u-mysql

%define pnm_buildrequires_SUNWphp52_mysql	SUNWphp52u-mysql
%define pnm_requires_SUNWphp52_mysql		SUNWphp52u-mysql

%define pnm_buildrequires_php52_mysql		SUNWphp52u-mysql
%define pnm_requires_php52_mysql		SUNWphp52u-mysql

#-apc -idn -memcache skipped, can be added if needed
%define pnm_buildrequires_SUNWphp52_pear	SUNWphp52u-pear
%define pnm_requires_SUNWphp52_pear		SUNWphp52u-pear
%define pnm_buildrequires_php52_pear 		SUNWphp52u-pear
%define pnm_requires_php52_pear 		SUNWphp52u-pear

%define pnm_buildrequires_SUNWphp52_pgsql 	SUNWphp52u-psql
%define pnm_requires_SUNWphp52_pgsql 		SUNWphp52u-psql
%define pnm_buildrequires_SUNWphp52u_pgsql 	SUNWphp52u-psql
%define pnm_requires_SUNWphp52u_pgsql 		SUNWphp52u-psql
%define pnm_buildrequires_SUNWphp52r_pgsql 	SUNWphp52r-psql
%define pnm_requires_SUNWphp52r_pgsql 		SUNWphp52r-psql
%define pnm_buildrequires_php52_pgsql 		SUNWphp52u-psql
%define pnm_requires_php52_pgsql		SUNWphp52u-psql
#-suhosin -tcpwrap -xdebug skipped, can be added if needed

#various packages

%define pnm_buildrequires_SUNWbash              SUNWbash
%define pnm_requires_SUNWbash                   SUNWbash
%define pnm_buildrequires_SUNWpcre              SUNWpcre
%define pnm_requires_SUNWpcre                   SUNWpcre
%define pnm_buildrequires_SUNWggrp              SUNWggrp
%define pnm_requires_SUNWggrp                   SUNWggrp
%define pnm_buildrequires_SUNWlibsasl           SUNWlibsasl
%define pnm_requires_SUNWlibsasl                SUNWlibsasl

#kerberos
%define pnm_buildrequires_service_security_kerberos_5  SUNWkrbu
%define pnm_requires_service_security_kerberos_5       SUNWkrbu

%define pnm_buildrequires_SUNWkrb 		SUNWkrbu
%define pnm_buildrequires_SUNWkrbr		SUNWkrbr
%define pnm_buildrequires_SUNWkrbu		SUNWkrbu
%define pnm_requires_SUNWkrb                    SUNWkrbu
%define pnm_requires_SUNWkrbr 			SUNWkrbr
%define pnm_requires_SUNWkrbu 			SUNWkrbu

#samba
%define pnm_buildrequires_service_network_samba	SUNWsmbu
%define pnm_requires_service_network_samba	SUNWsmbu
%define pnm_buildrequires_SUNWsmba_devel 	SUNWsmbu
%define pnm_buildrequires_SUNWsmba		SUNWsmbu
%define pnm_buildrequires_SUNWsmbar		SUNWsmbr
%define pnm_buildrequires_SUNWsmbau		SUNWsmbu
%define pnm_requires_SUNWsmba			SUNWsmbu
%define pnm_requires_SUNWsmbar			SUNWsmbr
%define pnm_requires_SUNWsmbau			SUNWsmbu
%define pnm_buildrequires_smba			SUNWsmbu
%define pnm_requires_smba			SUNWsmbu


##TODO## Add your packages here in case you specify an old
# package name now with the pnm_buildrequires_SUNWoldname makro

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

##TODO##define exact osbuild number where SUNWfreetype disappeared
#rules: if osdistro does not know freetype2, then use SFEfreetype (2.x)
#defaults for all builds < 133 (just to have somehting to start with)

#the default settings from the other p*inc files are valid or overwritten here
%define pnm_buildrequires_SUNWfreetype2		SUNWfreetype2
%define pnm_requires_SUNWfreetype2		SUNWfreetype2
%define pnm_buildrequires_freetype2		SUNWfreetype2
%define pnm_requires_freetype2			SUNWfreetype2
#SFEfreetype replaced with SUNWfreetype2 
#NOTE: no "2" at the end!
%define pnm_buildrequires_SUNWfreetype_devel 	SUNWfreetype2
%define pnm_requires_SUNWfreetype		SUNWfreetype2

##TODO## which osbuild version is right?
%if %( expr %{osbuild} '<' 133 )
#replace requested SUNWfreetype2* with SFE version on older
#osbuild version
#NOTE: might adjust exact osbuild version later
%define pnm_buildrequires_SUNWfreetype2_devel	SFEfreetype-devel
%define pnm_buildrequires_SUNWfreetype2		SFEfreetype
%define pnm_requires_SUNWfreetype2		SFEfreetype
%define pnm_buildrequires_freetype2		SFEfreetype-devel
%define pnm_requires_freetype2			SFEfreetype
%define pnm_buildrequires_system_library_freetype_2	SFEfreetype-devel
%define pnm_requires_system_library_freetype_2	SFEfreetype
#SFE requested
%define pnm_buildrequires_SFEfreetype_devel	SFEfreetype-devel
%define pnm_requires_SFEfreetype		SFEfreetype
%endif
#END < 133

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



#special case, pkgtool/pkgbuild can't see if packages are installed if
#meta-package data/docbook is requested (it shows never as being installed).
#up to 133 it was developer/documentation-tool/gtk-doc
#NOTE we overwrite what the include for 134 has defined
%if %( expr %{osbuild} '>=' 134 )
%define pnm_buildrequires_developer_documentation_tool_gtk_doc    developer/documentation-tool/gtk-doc
%define pnm_requires_developer_documentation_tool_gtk_doc         developer/documentation-tool/gtk-doc
%define pnm_buildrequires_SUNWgtk_doc_devel     developer/documentation-tool/gtk-doc
%define pnm_buildrequires_SUNWgtk_doc           developer/documentation-tool/gtk-doc
%define pnm_requires_SUNWgtk_doc                developer/documentation-tool/gtk-doc
%define pnm_buildrequires_gtk_doc               developer/documentation-tool/gtk-doc
%define pnm_requires_gtk_doc                    developer/documentation-tool/gtk-doc
%define pnm_buildrequires_SUNWgtk_doc		developer/documentation-tool/gtk-doc
%define pnm_requires_SUNWgtk_doc		developer/documentation-tool/gtk-doc
%define pnm_buildrequires_SUNWgnome_xml         developer/documentation-tool/gtk-doc
%define pnm_requires_SUNWgnome_xml              developer/documentation-tool/gtk-doc
%define pnm_buildrequires_SUNWgtk_doc           developer/documentation-tool/gtk-doc
%define pnm_requires_SUNWgtk_doc                developer/documentation-tool/gtk-doc
%define pnm_buildrequires_data_docbook          developer/documentation-tool/gtk-doc
%define pnm_requires_data_docbook               developer/documentation-tool/gtk-doc
%endif
#END >= 134

#special case, pkgtool/pkgbuild can't see if packages are installed if
#meta-package x11/client is requested. up to 143 it was TBD
#NOTE we overwrite what the include for 133 / 134 has defined (target was x11/client)
%if %( expr %{osbuild} '>=' 144 )
%define pnm_buildrequires_x11_clients compatibility/packages/SUNWxwplt
%define pnm_requires_x11_clients compatibility/packages/SUNWxwplt
%define pnm_buildrequires_SUNWxwplt_devel compatibility/packages/SUNWxwplt
%define pnm_buildrequires_SUNWxwplt compatibility/packages/SUNWxwplt
%define pnm_requires_SUNWxwplt compatibility/packages/SUNWxwplt
%define pnm_buildrequires_xwplt compatibility/packages/SUNWxwplt
%define pnm_requires_xwplt compatibility/packages/SUNWxwplt
%define pnm_buildrequires_compatibility_packages_SUNWxwplt compatibility/packages/SUNWxwplt
%define pnm_requires_compatibility_packages_SUNWxwplt compatibility/packages/SUNWxwplt
%endif
#END >= 144


##TODO## volunteers may implement the rules noted below
#2010-09-14 SUNWgraphviz removed from spec-files
#a) when was SUNWgraphviz added
#b) when was SUNWgraphviz removed from the builds
#%if %( expr %{osbuild} '>' 000 )
#%endif

#packages no longer available, we could bail out or just require a core package
#to continue for now, we just set a already existing package name, the spec file 
#might fail compiling or have reduced functionality then -> up to the individual
#spec file maintainer how to solve that

#cases >=156
%if %{solaris11express}
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
%endif
#END solaris11express

# audio headers got renamed several times, then 
# included in other package
%if %{solaris11express}
%if %( expr %{osbuild} '>=' 163 )
#with 163 system/header/header-audio moved into system/header
%define pnm_buildrequires_SUNWaudh_devel 			system/header
%define pnm_buildrequires_SUNWaudh 				system/header
%define pnm_requires_SUNWaudh 					system/header
%define pnm_buildrequires_audh 					system/header
%define pnm_requires_audh 					system/header
%define pnm_buildrequires_system_header_header_audio		system/header
%define pnm_requires_system_header_header_audio 		system/header
%endif
#END >=163
%endif
#END solaris11express

#START setting perl5, defaults  - Part 1 of 3
#define perl defaults, primarily shared settings and default version, paths
#for older osbuilds/osdistros like OpenSolaris 134, SXCE/Nevada, Solaris 10
#STRONG NOTE: located *below* the osdistro and osbuild sections, there is *another*
#section evaluating the resulting paths on the disk, those are specific
#to the perl version in use. We hope, that we do not need to handle special
#cases there, e.g. this would be an odd distro deciding to relocate to 
#another path layout on disk....

#note: older Solaris releases did include "micro"-versionnumber in 
#modules path, e.g. vendor_perl/5.8.4
#more fresh versions do only set major.minor, this is e.g. vendor_perl/5.12
%define perl_version 5.8.4
%define perl_major_version 5
%define perl_major_minor_version 5.8
%define perl_major_minor_micro_version 5.8.4

###TODO## not clear if we should require SUNWperl584core or SUNWperl584usr
#both?
#note: the name is subject to change if we find a better one
#_default string is not meant to be a part of the package name...
%define pnm_buildrequires_perl_default	SUNWperl584core, SUNWperl584usr
%define pnm_requires_perl_default	SUNWperl584core, SUNWperl584usr

# NOTE the section sitting below the distro specfic settings
# where the resulting paths on the disk are evaluated!

#END setting perl5, defaults  - Part 1 of 3



#START setting perl5, changes with specific builds and distros  - Part 2 of 3

#the distro specific settings below.
#set specifics for more fresh osbuild/osdistro like Solaris 11 Express, OpenIndiana
#which integrate perl 5.10 or newer (please add more sections for overrides in 
#different distro releases. Order is: greatest osbuild must be listed last to
#override previous settings)

#set perl5 for Solaris11Express
%if %{os2nnn}
%if %{solaris11express}
##TODO## remove this todo once the perl version to use is known and set the exact build number
%if %( expr %{osbuild} '>=' 166 )
#set perl5 for Solaris 11 Express
%define perl_version 5.12
%define perl_major_minor_version 5.12
%define perl_major_minor_micro_version 5.12.3
#runtime/perl-512 or library/perl-5/sun-solaris-512
%define pnm_buildrequires_perl_default runtime/perl-512
%define pnm_requires_perl_default	runtime/perl-512
%endif
##TODO## remove this todo once the perl version to use is known and set the exact build number
#END >= 166
%endif
#END solaris11express
%endif
#END os2nnn

#set perl5 for OpenIndiana
%if %{os2nnn}
%if %{openindiana}
##TODO## monitor closely when OpenIndiana starts shipping complete module sets with e.g. perl-512
%if %( expr %{osbuild} '>=' 151 )
#set perl5 for OpenIndiana 
%define perl_version 5.10.0
%define perl_major_minor_version 5.10
##TODO## determine correct version %define perl_major_minor_micro_version 5.10.x
%define perl_major_minor_micro_version 5.10.0
#runtime/perl-510
%define pnm_buildrequires_perl_default runtime/perl-510
%define pnm_requires_perl_default	runtime/perl-510
%endif
#END >= 151
%endif
#END openindiana
%endif
#END os2nnn

#add more distro here

#END setting perl5, changes with specific builds and distros  - Part 2 of 3


#START setting perl5, all builds, evaluated paths  - Part 3 of 3
# this is the section noted above which evaluates the resulting paths on the
# disk for the defaults for perl or the distro specific changed values e.g.
# more fresh perl version 5.8.4 -> 5.12 

#vendor_perl
# echo %{_prefix}/%{perl_path_vendor_perl}         -> prints /usr/perl5/vendor_perl
%define perl_path_vendor_perl perl%{perl_major_version}/vendor_perl

# echo %{_prefix}/%{perl_path_vendor_perl_version} -> prints /usr/perl5/vendor_perl/5.8.4 (or 5.10.0)
%define perl_path_vendor_perl_version perl%{perl_major_version}/vendor_perl/%{perl_version}


#site_perl
# echo %{_prefix}/%{perl_path_site_perl}           -> prints /usr/perl5/site_perl
%define perl_path_site_perl perl%{perl_major_version}/site_perl

# echo %{_prefix}/%{perl_path_site_perl_version}   -> prints /usr/perl5/site_perl/5.8.4 (or 5.10.0)
%define perl_path_site_perl_version perl%{perl_major_version}/site_perl/%{perl_version}

#END setting perl5, all builds, evaluated paths  - Part 3 of 3


#START setting Python, defaults  - Part 1 of 1
#define Python defaults, primarily shared settings and default versions and paths
#NOTE: we start initially only with setting Python 2.6 for *ALL* osbuild / osdistro
#this is to be extended in the future as required (for older osbuild/osdistro, *or* 
#for next Python 2.x or 3.x)

%define python_version 2.6
%define python_major_version 2
%define python_major_minor_version 2.6
%define python_major_minor_micro_version 2.6.4

#note: the name is subject to change if we find a better one
#_default string is not meant to be a part of the package name...
%define pnm_buildrequires_python_default	SUNWPython26-devel,SUNWPython26
%define pnm_requires_python_default	SUNWPython26

# add sub-packagenames like "SUNWPython26-extra" and "-cherrypy" to the end, see examples:
#  BuildRequires:	%{pnm_buildrequires_python_default}-extra 
#  Requires:		%{pnm_requires_python_default}-extra 
#  BuildRequires:	%{pnm_buildrequires_python_default}-cherrypy
#  Requires:		%{pnm_requires_python_default}-cherrypy

#BIG NOTE read the "perl" examples in this file *IF* you want to 
#extend the logic to define a new osbuild/osdistro or switch to
#another Python version, e.g. 2.7 or 3.0 only for specific osbuild/osdistro
#combinations.
#Mind to write the same comments as for the perl section "Part n of m" to 
#highlight that a value may be re-defined later on for special cases
#END setting Python


#START setting mysql, defaults  - Part 1 of 3
#define mysql defaults, primarily shared settings and default version, paths
#for older osbuilds/osdistros like OpenSolaris 134, SXCE/Nevada, Solaris 10
#STRONG NOTE: located *below* the osdistro and osbuild sections, there is *another*
#section evaluating the resulting paths on the disk, those are specific
#to the mysql version in use. We hope, that we do not need to handle special
#cases there, e.g. this would be an odd distro deciding to relocate to 
#another path layout on disk....
##TODO## Solaris 10's mysql versions *not yet* covered here

#from SXCE on we have this:
%define mysql_version 5.1
%define mysql_major_version 5
%define mysql_major_minor_version 5.1
##not defined %define mysql_major_minor_micro_version 5.1.X

#we simplify the veriants for mysql, we try to use only the newer one
#for *all* consuming spec files.
#include file /usr/mysql/5.1/include/mysql/mysql.h is in SUNWmysql51u
%define pnm_buildrequires_mysql_default	SUNWmysql51u
%define pnm_requires_mysql_default	SUNWmysql51u

#END setting mysql, defaults  - Part 1 of 3

#START setting mysql, changes with specific builds and distros  - Part 2 of 3
#set mysql for Solaris11Express or OpenIndiana or OpenSolaris
%if %{os2nnn}
#older IPS systems
%define pnm_buildrequires_mysql_default	SUNWmysql51
%define pnm_requires_mysql_default	SUNWmysql51
%if %( expr %{osbuild} '>=' 133 )
#from build 133 and up we have
#database/mysql-51
%define pnm_buildrequires_mysql_default	database/mysql-51
%define pnm_requires_mysql_default	database/mysql-51
%endif
#END >= 133
%endif
#END os2nnn

#add more distro here

#END setting mysql, changes with specific builds and distros  - Part 2 of 3

#START setting mysql, all builds, evaluated paths  - Part 3 of 3
# this is the section noted above which evaluates the resulting paths on the
# disk for the defaults for mysql or the distro specific changed values e.g.
# if a more fresh mysql version stores files somewehre else

#set handy partial paths to default locations where important mysql files
#are stored
#note: simplyfication: %{_prefix} must be prepended by the spec file itself

#example:
#the mysql.h file would be found with CFLAGS="-I%{_prefix}/%{mysql_default_includedir}"
%define mysql_default_includedir	mysql/%{mysql_major_minor_version}/include
#more information: #include "mysql/mysql.h" -->> /usr/mysql/5.1/include/mysql/mysql.h 

#the mysql libs would be found with LDFLAGS and/or CFLAGS="-L%{_prefix}/%{mysql_default_libdir} -R%{_prefix}/%{mysql_default_libdir}"
%define mysql_default_libdir	mysql/%{mysql_major_minor_version}/lib

#END setting mysql, all builds, evaluated paths  - Part 3 of 3


#  pkg contents -r -m system/header/header-audio
# set name=pkg.fmri value=pkg://solaris/system/header/header-audio@0.5.11,5.11-0.163:20110410T085804Z
# set name=variant.arch value=sparc value=i386
# set name=org.opensolaris.consolidation value=osnet
# set name=variant.opensolaris.zone value=global value=nonglobal
# set name=pkg.renamed value=true
# depend fmri=consolidation/osnet/osnet-incorporation type=require
# depend fmri=pkg:/system/header@0.5.11,5.11-0.163 type=require
 
 
#place very special cases here, for instance in Solaris 10
##TODO## for a future version



%changelog
* Wed Jan  4 2012 - Thomas Wagner
- pkgtool/pkgbuild can't see if packages are installed: meta-package data/docbook
  is requested. up to 133 it was developer/documentation-tool/gtk-doc,
  now it's a never installed package because it got renamed to an incorporation
* Sat Dec 10 2011 - Thomas Wagner
- make SUNWsmba* be service/network/samba (>=133)
* Mon Nov  7 2011 - Thomas Wagner
- handle cases x11/client not being resolved properly pnm_buildrequires_SUNWxwplt compatibility/packages/SUNWxwplt (>=144)
* Sat Aug 13 2011 - Thomas Wagner
- handle SUNWsmba_devel/SUNWsmbau/SUNWsmbar/SUNWsmba/smba/service_network_samba
- handle SUNWfreetype2/freetype2/SFEfreetype_devel/SFEfreetype/system_library_freetype_2
- fix selected metapackage to get installed-detection with autodeps satisfied for
  SUNWgtk_doc/developer_documentation_tool_gtk_doc/data_docbook (not fully tested)
* Mon Aug  2 2011 - Thomas Wagner
- handle special macro name pnm_buildrequires_mysql_default pnm_requires_mysql_default
  and macros for mysql version.
  add macro to point to the mysql_default_includedir and mysql_default_libdir.
  SUNWmysql51/SUNWmysql51u/database/mysql-51 is initially the only mysql-version
  for *all* osbuild / osdistro, to be extended as required later (for older 
  osbuild/osdistro, *or* for next mysql-versions 5.x or 6.x...)
* Mon Aug  1 2011 - Thomas Wagner
- handle SUNWkrb/SUNWkrbu/SUNWkrbr/service_security_kerberos_5
* Sun Jul 31 2011 - Thomas Wagner
- add SVR4 package names for SUNWbash SUNWpcre SUNWggrp SUNWlibsasl
- fix name *openssl-include  *openssl-includes
* Wed Jul 20 2011 - Thomas Wagner
- handle special macro name pnm_buildrequires_python_default pnm_requires_python_default
  and macros for python version.
  SUNWPython26 is initially the only Python-version for *all* osbuild / osdistro, to
  be extended as required later (for older osbuild/osdistro, *or* for next Python 2.x or 3.x)
* Sat Jul 16 2011 - Thomas Wagner
- handle SUNWapch22** (subset only. old SXCE/IPS_old/IPS_new_names)
- handle SUNWphp52**  (subset only. old SXCE/IPS_old/IPS_new_names)
* Thu Jun 23 2011 - Thomas Wagner
- enhance default (Build)Requires pnm_buildrequires_perl_default to include both
  SUNWperl584core, SUNWperl584usr. Only affects older distributions
* Sun Jun 19 2011 - Thomas Wagner
- handle SUNWaudh|audh|system/header/header-audio moved into system/header (>=163 s11ex)
* Fri Jun 17 2011 - Thomas Wagner
- handle different perl versions (5.8.4, 5.10, 5.12) and module paths 
- set perl to 5.12 on Solaris 11 to have modules in directory vendor_perl/5.12 (and not in 5.12.3)
- set perl to 5.10 on OpenIndiana to have modules in directory vendor_perl/5.10 (and not in 5.10.0)
- add note about omitting "micro"-versionnumber from the path to modules
- handle special macro name pnm_buildrequires_perl5_default pnm_requires_perl5_default (note: renamed!):
   SUNWperl584core/SUNWperl584usr runtime/perl-510 runtime/perl-512 (note the _default string)
- fine tune perl_vesion to be 5.10.0 and higher version numbers remain as 5.12 (w/o micro version)
- rename pnm_buildrequires_perl5_default to pnm_buildrequires_perl_default (+requires)
- remove >"< from %define perl_path_<vendor|site>*
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
