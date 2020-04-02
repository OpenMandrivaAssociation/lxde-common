%define git git20110808
# define Epoch only to revert from 0.5.5.1 to 0.5.5 git

Summary:	A set of default configuration for LXDE
Name:		lxde-common
Epoch:		1
Version:	0.99.2
Release:	2
License:	GPLv2+
Group:		Graphical desktop/Other
Url:		http://lxde.sourceforge.net/
Source0:	http://sourceforge.net/project/lxde/%{name}-%{version}.tar.xz
# Mandriva customization patch
#Patch101:	lxde-common-0.5.5-pcmanfm.conf.patch
Patch102:	lxde-common-0.5.5-add-mcc-to-panel.patch
#Patch103:	lxde-common-0.5.5-lxpanel-customization.patch
Patch106:	lxde-common-0.5.5-autostart.patch
#Patch109:	lxde-common-0.5.5-config.patch

BuildArch:	noarch
BuildRequires:  intltool
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:  gettext-devel
BuildRequires:  gettext
BuildRequires:  glib-gettextize
#Requires:	smproxy
Requires:	openbox
Requires:	lxpanel >= 0.5.9
Requires:	lxsession >= 0.4.1
Requires:	pcmanfm >= 0.9.10
Requires:	lxterminal
Requires:	lxde-icon-theme
# Disable it for now (until prepare new one config)
#Requires:	mandriva-lxde-config >= 0.5
#Requires(post):	mandriva-theme
Recommends:	xscreensaver
Conflicts:	mandriva-lxde-config-Free < 0.5
Conflicts:	mandriva-lxde-config-Flash < 0.5
Conflicts:	mandriva-lxde-config-One < 0.5
Conflicts:	mandriva-lxde-config-Powerpack < 0.5

%description
This package provides a set of default configuration for LXDE.

%prep
%setup -q
#patch101 -p0 -b .pcmanfm_conf
%patch102 -p0 -b .mdv-mcc
#patch103 -p1 -b .mdv-panel
%patch106 -p0 -b .autostart
#patch109 -p0 -b .config

%build
#./autogen.sh
%configure --enable-man
%make_build

%install
%make_install

# we'll ship these files via mandriva-lxde-config
#rm -f %{buildroot}%{_sysconfdir}/xdg/lxsession/LXDE/desktop.conf %{buildroot}%{_datadir}/lxde/openbox/rc.xml

# we do not need this file
#rm -f %{buildroot}%{_datadir}/xsessions/LXDE.desktop

# instead, we use wmsession.d
install -d %{buildroot}%{_sysconfdir}/X11/wmsession.d/
cat > %{buildroot}%{_sysconfdir}/X11/wmsession.d/04LXDE << EOF
NAME=LXDE
DESC=Lightweight X11 Desktops Environment
EXEC=/usr/bin/startlxde
SCRIPT:
exec /usr/bin/startlxde
EOF

# install this one manually, this provides the logout button on lxpanel:
install -m644 -D lxde-logout.desktop.in %{buildroot}%{_datadir}/applications/lxde-logout.desktop

%files
%config %{_sysconfdir}/xdg/lxsession/LXDE/autostart
%config %{_sysconfdir}/xdg/pcmanfm/LXDE/pcmanfm.conf
%{_sysconfdir}/X11/wmsession.d/04LXDE
%{_sysconfdir}/xdg/lxpanel/LXDE/config
%{_sysconfdir}/xdg/lxpanel/LXDE/panels/panel
%{_sysconfdir}/xdg/openbox/LXDE/menu.xml
%{_sysconfdir}/xdg/openbox/LXDE/rc.xml
%{_bindir}/*
%{_datadir}/applications/lxde-logout.desktop
%{_datadir}/applications/lxde-screenlock.desktop
%{_datadir}/lxde
#{_datadir}/lxpanel
%{_mandir}/man1/*

