%include Solaris.inc
%define pluginname mserver
%include base.inc
%use gmpcplugin = gmpc-plugin.spec

Name:			SFEgmpc-plugin-%{pluginname}
Summary:                gmpc-%{pluginname} - Mserver allows you to play local files on a remote or local mpd server. Stream music files to your mpd that are not in your database. 
# Version e.g. 0.20.0
Version:                %{gmpcplugin.version}
 
BuildRequires: SFEgcc
Requires: SFEgccruntime
BuildRequires: SFElibmicrohttpd
Requires: SFElibmicrohttpd


BuildRequires: SFEgmpc-devel
Requires: SFEgmpc
BuildRequires: SFEtaglib-devel
Requires: SFEtaglib

%description
http://gmpc.wikia.com/wiki/Mserver
How it works: Mserver is compiled using the libmicrohttp library, which enables applications to function as a minimal webserver. As MPD is perfectly capable of playing Streams out of the box, you get a list of streams in your playback queue after adding the files. 

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
%dir %attr (0755, root, other) %{_datadir}/gmpc
%{_datadir}/gmpc/plugins/*


%changelog
* Thu May 31 2012 - Thomas Wagner
- add (Build)Requires: SFElibmicrohttpd
* Wed Apr 25 2012 - Thomas Wagner
- add (Build)Requires: SUNWgcc(runtime)
* Tue Apr 24 2012 - Thomas Wagner
- bump to 0.20.0
* Sat Feb 21 2009 - Thomas Wagner
- add (Build-)Requires: SFEgmpc(-devel) (moved from base-specs/gmpc-plugin.spec)
- removed %doc from %files (usually no docs contained in plugins)
* Sun Dec 02 2007 - Thomas Wagner
- rework into base-spec
- bump to 0.15.5.0
