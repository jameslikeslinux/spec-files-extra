#
# Default system dependencies for PERL packages on Solaris
#

%include packagenamemacros.inc

BuildRequires:  %pnm_buildrequires_perl_default
Requires:       %pnm_requires_perl_default

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif

%define perl_bin /usr/bin
