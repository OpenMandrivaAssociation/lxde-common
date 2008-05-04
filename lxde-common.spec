Summary:	A set of default configuration for LXDE
Name:	  	lxde-common
Version:	0.3.2.1
Release:	%mkrel 1
License:	GPLv2+
Group:		Graphical desktop/Other
Source0: 	http://dfn.dl.sourceforge.net/sourceforge/lxde/%name-%version.tar.bz2
URL:		http://lxde.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	gtk+2-devel
Requires:	smproxy
Requires:	xscreensaver
Requires:	openbox
Requires:	lxpanel
Requires:	pcmanfm

%description
This package provides a set of default configuration for LXDE.

%package -n nuoveXT2-icon-theme
Summary:	nuoveXT2 icon theme
Group:		Graphical desktop/Other

%description -n nuoveXT2-icon-theme
This package contains nuoveXT2 icon theme for LXDE.

%prep
%setup -q

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%{find_lang} %{name}

# we do not need this file
rm -f %buildroot%{_datadir}/xsessions/LXDE.desktop

# instead, we use wmsession.d
install -d %buildroot%_sysconfdir/X11/wmsession.d/
cat > %buildroot%_sysconfdir/X11/wmsession.d/26LXDE << EOF
NAME=LXDE
DESC=Lightweight X11 Desktops Environment
EXEC=/usr/bin/startlxde
SCRIPT:
exec /usr/bin/startlxde
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%make_session

%postun
%make_session

%post -n nuoveXT2-icon-theme
%update_icon_theme nuoveXT2

%postun -n nuoveXT2-icon-theme
%clean_icon_theme nuoveXT2

%files -f %{name}.lang
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/xdg/lxsession/LXDE/autostart
%config(noreplace) %{_sysconfdir}/xdg/lxsession/LXDE/config
%config(noreplace) %{_sysconfdir}/xdg/lxsession/LXDE/default
%{_sysconfdir}/X11/wmsession.d/26LXDE
%{_bindir}/*
%{_datadir}/lxde
%{_datadir}/lxpanel
%{_mandir}/man1/*

%files -n nuoveXT2-icon-theme
%defattr(-, root, root)
%{_iconsdir}/nuoveXT2