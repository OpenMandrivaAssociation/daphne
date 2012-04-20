#
# spec file for package spec (Version 2.0)
#
# Copyright (c) 2003 SuSE Linux AG, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://www.suse.de/feedback/
#

# norootforbuild

Name:         daphne
License:      COPYRIGHT
Group:        Emulators
Version:      1.0
Release:      %mkrel 1
Summary:      Multiple Arcade Laserdisc Emulator
Source:       %name-%version-src.tar.bz2
Source1:      %name-1.0beta-linux-data.tar.gz
Patch:        daphne.dif
BuildRequires: SDL-devel libogg-devel zlib-devel gcc-c++ SDL_mixer-devel libvorbis-devel glew-devel fdupes mesaglu-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Play the original versions of many laserdisc arcade game.

%prep
%setup -q -n src -a 1
%patch -p1

%build
cp Makefile.vars.linux_x86 Makefile.vars
make %{?jobs:-j%jobs} \
%ifarch %ix86
I386FLAGS="-DNATIVE_CPU_X86 -DMMX_RGB2YUV" USE_MMX=1
%else
I386FLAGS=""
%endif
cd vldp2
./configure \
%ifnarch %ix86
	--disable-accel-detect
%endif

%ifarch %ix86
make -f Makefile.linux DFLAGS="$RPM_OPT_FLAGS"
%else
make -f Makefile.linux DFLAGS="$RPM_OPT_FLAGS -fPIC"
%endif

%install
# install section
install -D -m 755 ../daphne.bin $RPM_BUILD_ROOT%{_libdir}/%{name}/%{name}
install -m 755 ../libvldp2.so $RPM_BUILD_ROOT%{_libdir}/%{name}
cd daphne
cp -a pics roms sound $RPM_BUILD_ROOT%{_libdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_gamesbindir}
cat <<EOT >$RPM_BUILD_ROOT%{_gamesbindir}/%{name}
#!/bin/sh
cd %{_libdir}/%{name}
exec ./daphne "\$@"
EOT
chmod 755 $RPM_BUILD_ROOT%{_gamesbindir}/%{name}

%fdupes $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_gamesbindir}/%{name}
%{_libdir}/%{name}

