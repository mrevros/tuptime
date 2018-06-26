Name:		tuptime
Version:	3.3.3
Release:	1%{?dist}
Summary:	Report historical system running time

License:	GPLv2+
BuildArch:	noarch
URL:		https://github.com/rfrail3/tuptime/
Source0:	https://github.com/rfrail3/tuptime/archive/%{version}.tar.gz

%{?systemd_requires}
# Conditional requirements based on distribution release
%if (0%{?fedora} && 0%{?fedora} > 18) || (0%{?rhel} && 0%{?rhel} > 7) || (0%{?suse_version} && 0%{?suse_version} > 1210)
BuildRequires:  python3-devel
Requires:       python3
%else
# Require EPEL
BuildRequires:  python34-devel
Requires:       python34
%endif
BuildRequires:  sed
Requires:       systemd
Requires(pre):  shadow-utils



%description
Tuptime track and report historical and statistical running time of the
 system, keeping the uptime and downtime between shutdowns.

%prep
%setup -q
# Fix python shebang
sed -i '1s=^#!/usr/bin/\(python\|env python\)[23]\?=#!%{__python3}=' src/tuptime

%pre
getent group tuptime >/dev/null || groupadd -r tuptime
getent passwd tuptime >/dev/null || useradd --system --gid tuptime --home-dir "/var/lib/tuptime" --shell '/sbin/nologin' --comment 'Tuptime execution user' tuptime > /dev/null


%build
exit 0

%install
install -d %{buildroot}%{_bindir}/
install -d %{buildroot}%{_unitdir}/
install -d %{buildroot}%{_mandir}/man1/
install -d %{buildroot}%{_sharedstatedir}/tuptime/
install -d %{buildroot}%{_docdir}/tuptime/
cp -R %{_topdir}/BUILD/%{name}-%{version}/src/tuptime %{buildroot}%{_bindir}/
cp -R %{_topdir}/BUILD/%{name}-%{version}/src/systemd/tuptime.service %{buildroot}%{_unitdir}/
cp -R %{_topdir}/BUILD/%{name}-%{version}/src/systemd/tuptime.timer %{buildroot}%{_unitdir}/
cp -R %{_topdir}/BUILD/%{name}-%{version}/src/man/tuptime.1 %{buildroot}%{_mandir}/man1/
cp -R %{_topdir}/BUILD/%{name}-%{version}/tuptime-manual.txt %{buildroot}%{_docdir}/tuptime/
cp -R %{_topdir}/BUILD/%{name}-%{version}/CHANGELOG %{buildroot}%{_docdir}/tuptime/

%post
su -s /bin/sh tuptime -c "(umask 0022 && /usr/bin/tuptime -x)"
%systemd_post tuptime.service
%systemd_post tuptime.timer

%preun
%systemd_user_preun %{name}.service
%systemd_user_preun %{name}.timer

%postun
%systemd_postun_with_restart tuptime.service
%systemd_postun_with_restart tuptime.timer

%files
%defattr(-,root,root)
%{_unitdir}/tuptime.service
%{_unitdir}/tuptime.timer
%attr(0755, root, root) %{_bindir}/tuptime
%dir %attr(0755, tuptime, tuptime) %{_sharedstatedir}/tuptime/
%docdir %{_docdir}/tuptime/
%{_docdir}/tuptime/tuptime-manual.txt
%{_docdir}/tuptime/CHANGELOG
%{_mandir}/man1/tuptime.1.gz

%changelog
* Sun Jun 24 2018 Ricardo Fraile <rfraile@rfraile.eu> 3.3.3-1
- Initial RPM release
- More info: %{_docdir}/CHANGELOG