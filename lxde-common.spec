Summary:	A set of default configuration for LXDE
Name:	  	lxde-common
Version:	0.5.0
Release:	%mkrel 1
License:	GPLv2+
Group:		Graphical desktop/Other
Source0: 	http://dfn.dl.sourceforge.net/sourceforge/lxde/%name-%version.tar.gz
# Mandriva customization patch
Patch101:	lxde-common-0.3.2.1-use-mandriva-backgrounds.patch
Patch102:	lxde-common-0.3.2.1-add-mcc-to-panel.patch
Patch103:	lxde-common-0.4-lxpanel-customization.patch
URL:		http://lxde.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:	noarch
Requires:	smproxy
Suggests:	xscreensaver
Requires:	openbox
Requires:	lxpanel
Requires:	lxsession >= 0.4.1
Requires:	pcmanfm
Requires:	lxterminal
Requires:	lxde-icon-theme
Requires:	lxde-settings-daemon >= 0.4
Requires:	mandriva-lxde-config >= 0.5
Conflicts:	mandriva-lxde-config-Free < 0.5
Conflicts:      mandriva-lxde-config-Flash < 0.5
Conflicts:      mandriva-lxde-config-One < 0.5
Conflicts:	mandriva-lxde-config-Powerpack < 0.5
Requires(post):	mandriva-theme

%description
This package provides a set of default configuration for LXDE.

%prep
%setup -q
%patch101 -p1 -b .mdv-background
%patch102 -p0 -b .mdv-mcc
%patch103 -p0 -b .mdv-panel

%build
%configure2_5x
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%{find_lang} %{name}

# we'll ship this file via mandriva-lxde-config
rm -f %buildroot%{_sysconfdir}/xdg/lxsession/LXDE/desktop.conf

# we do not need this file
rm -f %buildroot%{_datadir}/xsessions/LXDE.desktop

# instead, we use wmsession.d
install -d %buildroot%_sysconfdir/X11/wmsession.d/
cat > %buildroot%_sysconfdir/X11/wmsession.d/04LXDE << EOF
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

%files -f %{name}.lang
%defattr(-, root, root)
%config(noreplace) %{_sysconfdir}/xdg/lxsession/LXDE/autostart
%{_sysconfdir}/X11/wmsession.d/04LXDE
%{_bindir}/*
%{_datadir}/lxde
%{_datadir}/lxpanel
%{_mandir}/man1/*
