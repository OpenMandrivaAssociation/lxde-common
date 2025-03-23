# git snapshot
#global snapshot 1
%if 0%{?snapshot}
	%global commit		8f960208e67ce64b4df0185b2c6c4da20dc0d24d
	%global commitdate	20240816
	%global shortcommit	%(c=%{commit}; echo ${c:0:7})
%endif

Summary:	A set of default configuration for LXDE
Name:		lxde-common
Version:	0.99.3
Release:	1
Group:		Graphical desktop/Other
License:	GPLv2+
Url:		https://lxde.sourceforge.net/
#Source0:	http://sourceforge.net/project/lxde/%{name}-%{version}.tar.xz
Source0:	https://github.com/lxde/%{name}/archive/%{?snapshot:%{commit}}%{!?snapshot:%{version}}/%{name}-%{?snapshot:%{commit}}%{!?snapshot:%{version}}.tar.gz
Source10:	libfm.conf.custom
# OpenMandriva customizations
Patch100:	lxde-common-0.99.2-openmandriva-autostart.patch
Patch101:	lxde-common-0.99.2-openmandriva-lxsession.patch
Patch102:	lxde-common-0.99.3-openmandriva-pcmanfm.patch
Patch103:	lxde-common-0.99.3-openmandriva-lxpanel.patch
Patch104:	lxde-common-0.99.2-openmandriva-theme.patch
Patch105:	lxde-common-0.99.2-openmandriva-logout.patch

BuildRequires:  intltool
BuildRequires:	docbook-style-xsl
BuildRequires:	xsltproc
BuildRequires:  gettext-devel
BuildRequires:  gettext
BuildRequires:  glib-gettextize
#Requires:	smproxy
Requires:	openbox
Requires:	lxpanel
Requires:	lxsession
Requires:	pcmanfm
Requires:	lxterminal
Requires:	lxde-icon-theme

Recommends:	xscreensaver

BuildArch:	noarch

%description
This package provides a set of default configuration for LXDE.

%files
%config(noreplace) %{_sysconfdir}/xdg/lxsession/LXDE/autostart
%config(noreplace) %{_sysconfdir}/xdg/pcmanfm/LXDE/pcmanfm.conf
%{_sysconfdir}/X11/wmsession.d/04LXDE
%{_sysconfdir}/xdg/lxpanel/LXDE/config
%config(noreplace) %{_sysconfdir}/xdg/lxsession/LXDE/desktop.conf
%config(noreplace) %{_sysconfdir}/xdg/lxpanel/LXDE/panels/panel
%{_sysconfdir}/xdg/openbox/LXDE/menu.xml
%{_sysconfdir}/xdg/openbox/LXDE/rc.xml
%{_datadir}/xsessions/LXDE.desktop
%{_bindir}/*
%{_datadir}/applications/lxde-logout.desktop
%{_datadir}/applications/lxde-screenlock.desktop
%{_datadir}/lxde
#{_datadir}/lxpanel
%{_mandir}/man1/*

%dir	%{_sysconfdir}/xdg/lxsession/libfm
%config(noreplace) %{_sysconfdir}/xdg/lxsession/libfm/libfm.conf

#---------------------------------------------------------------------------

%prep
%autosetup -p1 -n %{name}-%{?snapshot:%{commit}}%{!?snapshot:%{version}}

%build
./autogen.sh
%configure \
	--enable-man \
	%{nil}
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

# install this one manually, this provides the logout button on lxpanel
install -m644 -D lxde-logout.desktop.in %{buildroot}%{_datadir}/applications/lxde-logout.desktop

#install custom libfm.conf to set default terminal
mkdir -p %{buildroot}%{_sysconfdir}/xdg/lxsession/libfm
install -cpm 0644 %{SOURCE10} %{buildroot}%{_sysconfdir}/xdg/lxsession/libfm/libfm.conf

