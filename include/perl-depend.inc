#
# Default system dependencies for PERL packages on Solaris
#

#let it default to 0 (undefined = not included)
%if %{!?packagenamemacros:0}
#already included
%else
%include packagenamemacros.inc
%endif

BuildRequires:  %{pnm_buildrequires_perl_default}
Requires:       %{pnm_requires_perl_default}

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif

%define perl_bin /usr/bin


%changelog
* Sat Aug  4 2012 - Thomas Wagner
- don't re-include packagenamemacros.inc if it already is before
