%include Solaris.inc
%define pluginname mdcover
%include base.inc
%use gmpcplugin = gmpc-plugin.spec

Name:			SFEgmpc-plugin-%{pluginname}
Summary:                gmpc-%{pluginname} - This plugin collects metadata by checking the directory where the music is located
# Version e.g. 0.20.0
Version:                %{gmpcplugin.version}
 
BuildRequires: SFEgmpc-devel
Requires: SFEgmpc

%description
http://gmpc.wikia.com/wiki/GMPC_PLUGIN_MDCOVER
Mdcover plugin is a for gmpc. It looks in the location where the music file is located to collect metadata. It does this based on a set of rules.
Parsing rules

    * Cover art 

Cover art is searched in the directory the song is located. It looks for .gif,.png,.jpg,.jpeg files. dot files are ignored beside .folder.jpg. If the last directory in the path is CD [0-9] or DISC [0-9] mdcover also checks the parent directory.

    * Artist Art 

In the directory of the song mdcover checks for $artist.jpg, it also checks the parent directories.

    * Biography 

In the directory of the song mdcover checks for BIOGRAPHY, it also checks the parent directories.

    * Album information 

In the directory of the song mdcover checks for $album.txt, it also checks the parent directories.

    * Lyrics 

In the directory of the song mdcover checks for $title.lyrics. 

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

%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale

%changelog
* Tue Apr 24 2012 - Thomas Wagner
- bump to 0.20.0
* Sat Feb 21 2009 - Thomas Wagner
- add (Build-)Requires: SFEgmpc(-devel) (moved from base-specs/gmpc-plugin.spec)
- removed %doc from %files (usually no docs contained in plugins)
* Sun Dec 02 2007 - Thomas Wagner
- rework into base-spec
- bump to 0.15.5.0
