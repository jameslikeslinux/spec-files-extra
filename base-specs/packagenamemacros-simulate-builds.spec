#
#
#   STRONG note: this is an early stage, logic and variable names *might* change
#
#

# owner: Thomas Wagner (tom68) - please ask/discuss if you want non-trivial changes

# TODO: add copyright (CDDL?)


## READ ## place newer build simulation right here

#simulate a OS distro - Solaris 11 Express build 166
%define osdistro 1
%define osbuild 166
%define SXCE 0
%define os2nnn 1
%define solaris11express 1
%define s11ex201100 1
%define s11ex201011 0
%define openindiana 0
%define oi201100 0
%define oi201009 0
%define os201005 0
%define os201003 0
%define os200906 0
%define os200902 0
%define os200811 0
%define osdistrelnumber 166
%define osdistrelname   Solaris 11 Express
%define osdet299999 1

%use packagenamemacross11ex201100 = packagenamemacros.spec

#simulate a OS distro - Solaris 11 Express build 151
%define osdistro 1
%define osbuild 151
%define SXCE 0
%define os2nnn 1
%define solaris11express 1
%define s11ex201100 0
%define s11ex201011 1
%define openindiana 0
%define oi201100 0
%define oi201009 0
%define os201005 0
%define os201003 0
%define os200906 0
%define os200902 0
%define os200811 0
%define osdistrelnumber 151
%define osdistrelname   Solaris 11 Express
%define osdet299999 1

%use packagenamemacross11ex201011 = packagenamemacros.spec

#simulate a OS distro - OI151 build 151 IPS based
%define osdistro 1
%define osbuild 151
%define SXCE 0
%define os2nnn 1
%define solaris11express 0
%define s11ex201100 0
%define s11ex201011 0
%define openindiana 1
%define oi201100 1
%define oi201009 0
%define os201005 0
%define os201003 0
%define os200906 0
%define os200902 0
%define os200811 0
%define osdistrelnumber 151
%define osdistrelname   OpenIndiana
%define osdet299999 1

%use packagenamemacrosoi201100 = packagenamemacros.spec

#simulate a OS distro - OI147 build 147 IPS based
%define osdistro 1
%define osbuild 147
%define SXCE 0
%define os2nnn 1
%define solaris11express 0
%define s11ex201100 0
%define s11ex201011 0
%define openindiana 1
%define oi201100 0
%define oi201009 1
%define os201005 0
%define os201003 0
%define os200906 0
%define os200902 0
%define os200811 0
%define osdistrelnumber 147
%define osdistrelname   OpenIndiana
%define osdet299999 1

%use packagenamemacrosoi201009 = packagenamemacros.spec

#simulate a OS distro - OS2009 developer build 134 IPS based
%define osdistro 1
%define osbuild 134
%define SXCE 0
%define os2nnn 1
%define solaris11express 0
%define s11ex201100 0
%define s11ex201011 0
%define openindiana 1
%define oi201100 0
%define oi201009 0
%define os201005 0
%define os201003 0
%define os200906 1
%define os200902 0
%define os200811 0
%define osdistrelnumber 2009.06
%define osdistrelname   OS2009.06
%define osdet299999 1

%use packagenamemacros134dev = packagenamemacros.spec

#simulate a OS distro - OS2009 release build 111 IPS based
%define osdistro 1
%define osbuild 111
%define SXCE 0
%define os2nnn 1
%define solaris11express 0
%define s11ex201100 0
%define s11ex201011 0
%define openindiana 1
%define oi201100 0
%define oi201009 0
%define os201005 0
%define os201003 0
%define os200906 1
%define os200902 0
%define os200811 0
%define osdistrelnumber 2009.06
%define osdistrelname   OS2009.06
%define osdet299999 1

%use packagenamemacros111rel = packagenamemacros.spec

#simulate a OS distro - OS2008.11 release build 99 IPS based
%define osdistro 1
%define osbuild 99
%define SXCE 0
%define os2nnn 1
%define solaris11express 0
%define s11ex201100 0
%define s11ex201011 0
%define openindiana 1
%define oi201100 0
%define oi201009 0
%define os201005 0
%define os201003 0
%define os200906 0
%define os200902 0
%define os200811 1
%define osdistrelnumber 2008.11
%define osdistrelname   OS2008.11
%define osdet299999 1

%use packagenamemacros99rel = packagenamemacros.spec

#simulate a OS distro - SXCE build 130 SVR4 based
%define osdistro 1
%define osbuild 130
%define SXCE 1
%define os2nnn 0
%define solaris11express 0
%define s11ex201100 0
%define s11ex201011 0
%define openindiana 1
%define oi201100 0
%define oi201009 0
%define os201005 0
%define os201003 0
%define os200906 0
%define os200902 0
%define os200811 0
%define osdistrelnumber SXCEplaceholder
%define osdistrelname   SXCEplaceholder
%define osdet299999 1

%use packagenamemacros130sxce = packagenamemacros.spec

Name: packagenamemacros

%description
Demo the packagenamemacros.inc use for (see filename which OS and osbuild is simulated):

   pkgtool --interactive prep base-specs/packagenamemacros-simulate-builds.spec



%prep

%packagenamemacross11ex201100.prep
%packagenamemacross11ex201011.prep
%packagenamemacrosoi201100.prep
%packagenamemacrosoi201009.prep
%packagenamemacros134dev.prep
%packagenamemacros111rel.prep
%packagenamemacros99rel.prep
%packagenamemacros130sxce.prep

%changelog
* Fri Jun 17 2011 - Thomas Wagner
- adjust changed names for osdistro variables (osdistro.inc)
- add example to Solaris 11 Express, reformatted to highlight interesting settings
- add exmaple of OpenIndiana build 151 (not yet there)
* Sat Oct 30 2010 - Thomas Wagner
- add oi147 to the mix
* Jun 13 2010 - Thomas Wagner
- inital to demo the name resolution depending on the operatingsystem type / distribution with 
  simpulated build numbers and osdistro types
