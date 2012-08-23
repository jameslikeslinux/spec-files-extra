%include Solaris.inc
%define pluginname discogs
%include base.inc
%use gmpcplugin = gmpc-plugin.spec

Name:			SFEgmpc-plugin-%{pluginname}
Summary:                gmpc-%{pluginname} - searches www.discogs.com for images of artists and albums
# Version e.g. 0.20.0
Version:                %{gmpcplugin.version}
 
BuildRequires: SFEgcc
Requires: SFEgccruntime

BuildRequires: SFEgmpc-devel
Requires: SFEgmpc

%description
http://gmpc.wikia.com/wiki/GMPC_PLUGIN_DISCOGS

%prep
%gmpcplugin.prep
 
%build
%gmpcplugin.build
 
%install
%gmpcplugin.install

%clean
%gmpcplugin.clean

%files
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%{_libdir}/gmpc/plugins/*.so
#%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/gmpc-%{pluginname}/icons/*


%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%changelog
* Wed Apr 25 2012 - Thomas Wagner
- remove typo
* Wed Apr 25 2012 - Thomas Wagner
- add (Build)Requires: SUNWgcc(runtime)
* Tue Apr 24 2012 - Thomas Wagner
- bump to 0.20.0
* Wed Oct  6 2010 - Alex Viskovatoff
- *new* - based on SFEgmpc-plugin-albumview.spec
