%define major	0
%define libname	%mklibname unity-2d-private	%{major}
%define develname	%mklibname unity-2d-private	-d

Summary:	Unity interface for non-accelerated graphics cards
Name:		unity-2d
Version:	4.12.1
Release:	1
License:	GPLv3,LGPLv3
Url:		http://launchpad.net/unity-2d
Group:		Graphical desktop/Other
Source0:	%{name}-%{version}.tar.gz
# needed for manpages and gconf files
Source1:	http://archive.ubuntu.com/ubuntu/pool/main/u/unity-2d/%{name}_4.12.0-0ubuntu1.debian.tar.gz

BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(dbusmenu-qt)
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(libqtbamf)
BuildRequires:	pkgconfig(libqtdee)
BuildRequires:	pkgconfig(libutouch-geis)
BuildRequires:	pkgconfig(libwnck-3.0)
BuildRequires:	pkgconfig(dconf-qt)
BuildRequires:	pkgconfig(QtCore)
BuildRequires:	pkgconfig(unity-core-4.0)
BuildRequires:	pkgconfig(xcomposite)
BuildRequires:	%{_lib}qtgconf-devel

Requires:	%{name}-launcher = %{version}-%{release}
Requires:	%{name}-panel = %{version}-%{release}
Requires:	%{name}-places = %{version}-%{release}
Requires:	%{name}-spread = %{version}-%{release}
Requires:	metacity
Requires:	unity-common

%description
Unity interface for non-accelerated graphics cards

The Unity 2D interface installs a fully usable 2D session and provides the
common configuration files and defaults. Installing this package will
offer a session called Unity 2D in your login manager.

Unity 2D is designed to run smoothly without any graphics acceleration.

%package launcher
Summary:	Unity 2d launcher
Group:		Applications/System
Requires:	unity-asset-pool
Suggests:	unity-lens-application
Suggests:	unity-lens-files
Suggests:	unity-lens-music

%description launcher
The Unity 2D launcher displays a list of running applications as well as a
list of favorite applications in a panel at the left of the screen.
Notifications from individual applications are also highlighted in the
launcher.

%package panel
Summary:	Unity 2d panel
Group:		Applications/System
Provides:	indicator-renderer
Suggests:	indicator-application
Suggests:	indicator-appmenu
Suggests:	indicator-datetime
Suggests:	indicator-messages
Suggests:	indicator-session
Suggests:	indicator-sound

%description panel
The Unity 2D panel displays a top panel containing the application menu and
various indicators. It is part of Unity 2D and can not run  as a standalone
application outside of the Unity 2D environment.

%package places
Summary:	Unity 2d places
Group:		Applications/System

%description places
The Unity 2D places overlay over the desktop to provide quick access to
various categories of applications. It is part of Unity 2D and can not run
as a standalone application outside of the Unity 2D environment.

%package spread
Summary:	Unity 2d spread
Group:		Applications/System

%description spread
The Unity 2D spread allows you to display a quick thumbnailed view of open
windows so you can quickly and effectively choose which one you want to
switch to. It is part of Unity 2D and can not run  as a standalone application
outside of the Unity 2D environment.

%package -n %{libname}
Summary:	Private shared library of the Unit-2d
Group:		System/Libraries

%description -n %{libname}
This package provides the shared core libraries for the Unity-2d

Unity interface for non-accelerated graphics cards

%package -n %{develname}
Summary:	Development files of the Unity-2d-rpivate
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
Development files for unity-2d-private

%prep
%setup -q
%apply_patches

%build
%cmake

%make

%install
%makeinstall_std -C build

# install missing manpages and gconf files
tar xzf %SOURCE1
install -d %{buildroot}%{_mandir}/man1
install -m 0755 debian/manpages/%{name}-* %{buildroot}%{_mandir}/man1

install -d %{buildroot}%{_datadir}/gconf
install -m 0644 debian/gconf/ubuntu-2d.*.path %{buildroot}%{_datadir}/gconf

install -d %{buildroot}%{_datadir}/gconf/ubuntu-2d/default
install -m 0644 debian/20_ubuntu-2d-gconf-default %{buildroot}%{_datadir}/gconf/ubuntu-2d/default

install -d %{buildroot}%{_datadir}/gconf/ubuntu-2d/mandatory
install -m 0644 debian/20_ubuntu-2d-gconf-mandatory %{buildroot}%{_datadir}/gconf/ubuntu-2d/mandatory

install -d %{buildroot}%{_datadir}/apport/package-hooks
install -m 0644 debian/%{name}.py %{buildroot}%{_datadir}/apport/package-hooks

# im not sure this is right
install -d %{buildroot}%{_datadir}/gconf/defaults
install -m 0644 debian/unity-2d.gconf-defaults %{buildroot}%{_datadir}/gconf/defaults/10_unity-2d

# launcher links against this lib and its not installed
# install -d %{buildroot}%{_libdir}/unity-2d/plugins/launcher
install -m 0644 build/launcher/app/libuqlauncher.so %{buildroot}%{_libdir}

%find_lang %{name}

%files -f %{name}.lang
%{_datadir}/GConf/gsettings/unity-2d.convert
%{_datadir}/glib-2.0/schemas/com.canonical.Unity2d.gschema.xml
# missing found in the ubuntu pkg
%{_datadir}/apport/package-hooks/%{name}.py
%{_datadir}/gconf/defaults/10_unity-2d
%{_datadir}/gconf/ubuntu-2d.default.path
%{_datadir}/gconf/ubuntu-2d.mandatory.path
%{_datadir}/gconf/ubuntu-2d/default/20_ubuntu-2d-gconf-default
%{_datadir}/gconf/ubuntu-2d/mandatory/20_ubuntu-2d-gconf-mandatory
# huh copied from ubuntu lib pkg
%{_datadir}/unity-2d/warty-final-ubuntu.jpg

%files launcher
%{_bindir}/unity-2d-launcher
%{_datadir}/dbus-1/services/unity-2d-launcher.service
%{_datadir}/unity-2d/launcher/*.qml
%{_datadir}/unity-2d/launcher/artwork/*.png
%{_datadir}/applications/unity-2d-launcher.desktop
%{_libdir}/libuqlauncher.so
%{_mandir}/man1/%{name}-launcher.1*

%files panel
%{_bindir}/unity-2d-panel
%{_datadir}/applications/unity-2d-panel.desktop
%{_libdir}/unity-2d/plugins/panel/*.so.%{major}*
%{_mandir}/man1/%{name}-panel.1*
# split into its own devel pkg???
%{_libdir}/unity-2d/plugins/panel/*.so

%files places
%{_bindir}/unity-2d-places
%{_datadir}/dbus-1/services/unity-2d-places.service
%{_datadir}/unity-2d/places/*.qml
%{_datadir}/unity-2d/places/artwork/*.png
%{_datadir}/unity-2d/places/artwork/*.sci
%{_datadir}/unity-2d/places/artwork/*.svg
%{_datadir}/unity-2d/places/*.js
%{_datadir}/applications/unity-2d-places.desktop
%{_mandir}/man1/%{name}-places.1*

%files spread
%{_bindir}/unity-2d-spread
%{_datadir}/dbus-1/services/unity-2d-spread.service
%{_datadir}/unity-2d/spread/*.qml
%{_datadir}/unity-2d/spread/*.js
%{_mandir}/man1/%{name}-spread.1*

%files -n %{libname}
%{_libdir}/libunity-2d-private.so.%{major}*
%{_libdir}/qt4/imports/Unity2d/qmldir
%{_libdir}/qt4/imports/Unity2d/GnomeBackground.qml
%{_libdir}/qt4/imports/Unity2d/libunity-2d-private-qml.so

%files -n %{develname}
%{_includedir}/unity-2d-private/*.h
%{_libdir}/pkgconfig/unity-2d-private.pc
%{_libdir}/libunity-2d-private.so

