%include Solaris.inc
%define pluginname jamendo
%include base.inc
%use gmpcplugin = gmpc-plugin.spec

Name:			SFEgmpc-plugin-%{pluginname}
Summary:                gmpc-%{pluginname} - With the Jamendo plugin you are able to preview music from their database
# Version e.g. 0.20.0
Version:                %{gmpcplugin.version}
 
BuildRequires: SFEgcc
Requires: SFEgccruntime

BuildRequires: SFEgmpc-devel
Requires: SFEgmpc

%description
http://gmpc.wikia.com/wiki/GMPC_PLUGIN_JAMENDO
The jamendo plugin allows you to browse and preview music available on jamendo.
You can find all kinds of genres and preview the music.
This plugin requires JsonGlib to work. 

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
%dir %attr (0755, root, sys) %{_datadir}
#%{_datadir}/gmpc-%{pluginname}/icons/*
%dir %attr (0755, root, other) %{_datadir}/gmpc
%{_datadir}/gmpc/*

%defattr (-, root, bin)
#no locales %dir %attr (0755, root, sys) %{_datadir}
#no locales %attr (-, root, other) %{_datadir}/locale

%changelog
* Fri Jul 27 2012 - Thomas Wagner
- fix permissions for /usr/share/gmpc
* Sat Jun 23 2012 - Thomas Wagner
- fix permissions
* Wed Apr 25 2012 - Thomas Wagner
- add (Build)Requires: SUNWgcc(runtime)
* Tue Apr 24 2012 - Thomas Wagner
- initial spec
- fix double inclusion in %files
