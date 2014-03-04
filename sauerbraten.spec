Summary:	3D first-person game engine
Name:		sauerbraten
Version:	0.0
Release:	0.6.20130203%{?dist}

License:	zlib
URL:		http://www.sauerbraten.org/
Source:		http://downloads.sourceforge.net/project/sauerbraten/sauerbraten/2013_01_04/%{name}_2013_02_03_collect_edition_linux.tar.bz2
Source1:	sauerbraten.desktop
Source2:	sauerbraten.png

BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel
BuildRequires:	mesa-libGL-devel
BuildRequires:	zlib-devel

Requires:	sauerbraten-data = %{version}-%{release}


%description
Sauerbraten is a networked fast-paced 3D first person first-person shooter
game. It supports rather modern graphic effects and a some nice graphic
details.

The game client also works as the map editor. It is even possible to create
and/or edit a map together with other people over a network connection.

Sauerbraten might be considered unsuitable for children.

This package installs the game client and map editor.


%package server
Summary:	Standalone server for the Sauerbraten game
Requires:	%{name}%{?_isa} = %{version}-%{release}


%description server
Sauerbraten is a networked fast-paced 3D first person first-person shooter
game. It supports rather modern graphic effects and a some nice graphic
details.

The game client also works as the map editor. It is even possible to create
and/or edit a map together with other people over a network connection.

This package installs the standalone server for Sauerbraten.


%package data
Summary:	Game content for the Sauerbraten game
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch


%description data
Sauerbraten is a networked fast-paced 3D first person ego-shooter game. It
supports rather modern graphic effects and a some nice graphic details.

The game client also works as the map editor. It is even possible to create
and/or edit a map together with other people over a network connection.

This package installs maps, textures, sounds, etc. of Sauerbraten.


%prep
%setup -q -n %{name}

%build
cd src
sed -i "s|-O3 -fomit-frame-pointer|%{optflags}|g" Makefile
make %{?_smp_mflags}

%install
mkdir -p bin
mv src/sauer_client bin/client
mv src/sauer_server bin/server
mkdir -p %{buildroot}%{_datadir}/{applications,pixmaps}
cp %{SOURCE1} %{buildroot}%{_datadir}/applications/
cp %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/
mkdir -p %{buildroot}%{_libdir}/%{name}
cp -a bin %{buildroot}%{_libdir}/%{name}
mkdir -p %{buildroot}%{_bindir}

cat <<EOF >%{buildroot}%{_bindir}/%{name}
#!/bin/sh

SAUER_DIR=%{_datadir}/%{name}
SAUER_DIR_PRIVATE=\$HOME/.sauerbraten
cd \$SAUER_DIR_PRIVATE
test -L data && rm data
test -L packages && rm packages
test -d data || mkdir data
test -d packages || mkdir packages
exec %{_libdir}/%{name}/bin/client -r -q\$SAUER_DIR_PRIVATE "\$@" -k\$SAUER_DIR 
EOF

chmod 755 %{buildroot}%{_bindir}/%{name}
ln -sf %{_libdir}/%{name}/bin/server %{buildroot}%{_bindir}/%{name}-server

# install maps
install -dD %{buildroot}%{_datadir}/sauerbraten
mv data/ %{buildroot}%{_datadir}/sauerbraten/
mv packages %{buildroot}%{_datadir}/sauerbraten/


%files
%{_bindir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/bin
%{_libdir}/%{name}/bin/client
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png


%files server
%doc server-init.cfg
%{_bindir}/%{name}-server
%dir %{_libdir}/%{name}/bin
%{_libdir}/%{name}/bin/server


%files data
%dir %{_datadir}/sauerbraten/
%{_datadir}/sauerbraten/*


%changelog
* Tue Mar  4 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 0.0-0.6.20130203.R
- update to 20130203

* Mon Jan 14 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 0.0-0.5.20130107.R
- update to 20130107 snapshot (rfr#322)

* Thu Oct 21 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 0.0-0.4.20100728.R
- clean spec, added R to release

* Mon Mar 21 2011 Arkady L. Shane <ashejn@yandex-team.ru> - 0.0-0.4.20100728
- fix source url

* Thu Oct  6 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 0.0-0.3.20100728
- rebuilt against gcc bug

* Mon Sep 20 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 0.0-20100728
- update to 20100728

* Fri Nov 20 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 0.0-20090619svn1980
- initial build for Fedora
