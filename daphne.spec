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
License:      GPL
Group:        Emulators
Version:      1.0
Release:      1.2
Summary:      Multiple Arcade Laserdisc Emulator
Source:       %name-%version-src.tar.bz2
Source1:      %name-1.0beta-linux-data.tar.gz
Patch0:	daphne.dif
Patch1:	daphne-gl.patch
BuildRequires: SDL-devel libogg-devel zlib-devel gcc-c++ SDL_mixer-devel libvorbis-devel glew-devel fdupes mesaglu-devel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Play the original versions of many laserdisc arcade game.

%prep
%setup -q -n src -a 1
%patch0 -p1
%patch1 -p1

%build
cp Makefile.vars.linux_x86 Makefile.vars
make %{?jobs:-j%jobs} \
%ifarch %ix86
I386FLAGS="-DNATIVE_CPU_X86 -DMMX_RGB2YUV -lGL -lGLU" USE_MMX=1
%else
I386FLAGS="-lGL -lGLU"
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

%files
%defattr(-,root,root)
%{_gamesbindir}/%{name}
%{_libdir}/%{name}



%changelog
* Fri Apr 20 2012 Zombie Ryushu <ryushu@mandriva.org> 1.0-1.1mdv2011.0
+ Revision: 792447
- what is fdupes doing?
- what is fdupes doing?

* Fri Apr 20 2012 Zombie Ryushu <ryushu@mandriva.org> 1.0-1
+ Revision: 792424
- GL makefile patch
- GL dependency
- GL dependency
- GL dependency
- First import to Mandriva
- imported package daphne


* Fri Nov 14 2008 - uli@suse.de
- update -> 1.0
* Wed Oct 24 2007 - uli@suse.de
- no -fPIC for ix86 (breaks asm code)
