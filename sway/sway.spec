
Name:           sway
Version:        1.4
Release:        1%{?dist}
Summary:        i3-compatible window manager for Wayland
License:        MIT
URL:            https://github.com/swaywm/sway
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  asciidoc
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  meson
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(json-c) >= 0.13
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.14
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(libevdev)
BuildRequires:  pkgconfig(libsystemd) >= 239
BuildRequires:  wlroots-devel >= 0.10
BuildRequires:  wayland-devel
BuildRequires:  scdoc >= 1.9.2
Requires:       swaybg
# Dmenu is the default launcher in sway
Requires:       dmenu
Requires:       libinput >= 1.6.0
# By default the Fedora background is used
Recommends:     f%{fedora}-backgrounds-base
# dmenu (as well as rxvt and many others) requires XWayland on Sway
Requires:       xorg-x11-server-Xwayland
# Sway binds the terminal shortcut to one specific terminal. In our case urxvtc-ml
Recommends:     rxvt-unicode-256color-ml
# grim is a recommended way to take screenshots on sway 1.0+
Recommends:     grim

%description
Sway is a tiling window manager supporting Wayland compositor protocol and i3-compatible configuration.

%prep
%autosetup -n %{name}-%{version}%{?versrc_tail}
mkdir %{_target_platform}

%build
%meson -Dwerror=false -Dfish-completions=false
%meson_build

%install
%meson_install
# Set default terminal to urxvt256c-ml
sed -i 's/^set $term urxvt$/set \$term urxvt256c-ml/' %{buildroot}%{_sysconfdir}/sway/config
# Set Fedora background as default background
sed -i "s|^output \* bg .*|output * bg /usr/share/backgrounds/f%{fedora}/default/normalish/f%{fedora}.png fill|" %{buildroot}%{_sysconfdir}/sway/config


%files
%license LICENSE
%doc README.md
%dir %{_sysconfdir}/sway
%config(noreplace) %{_sysconfdir}/sway/config
%dir %{_sysconfdir}/sway/security.d
%config(noreplace) %{_sysconfdir}/sway/security.d/00-defaults
%{_mandir}/man1/sway*.1*
%{_mandir}/man5/sway*.5*
%{_mandir}/man7/sway*.7*
%caps(cap_sys_ptrace,cap_sys_tty_config=eip) %{_bindir}/sway
%{_bindir}/swaybar
%{_bindir}/swaymsg
%{_bindir}/swaynag
%{_datadir}/wayland-sessions/sway.desktop
%{_datadir}/bash-completion/completions/sway*
%exclude %{_datadir}/fish/vendor_completions.d/sway*
%{_datadir}/zsh/site-functions/_sway*
%{_datadir}/backgrounds/sway/*.png

%changelog
* Thu Jan 30 2020 João Pinto <jpinto@barcodeu.com> 1.4-1
- Initial RPM release