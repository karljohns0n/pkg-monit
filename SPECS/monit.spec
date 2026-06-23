Name:					monit
Version:				6.0.0
Release:				1%{?dist}
Summary:				Process monitor and restart utility

License:				AGPL-3.0-or-later
URL:					http://mmonit.com/monit/
Source0:				http://mmonit.com/monit/dist/%{name}-%{version}.tar.gz
Source1:				monitrc
Source2:				monit.service
Source3:				monit.systemd.logrotate
Source4:				services.systemd.conf

BuildRequires:			openssl-devel zlib-devel
BuildRequires:			systemd
Requires(post):			systemd, systemd-sysv
Requires(preun):		systemd
Requires(postun):		systemd

%description
monit is a utility for managing and monitoring, processes, files, directories
and devices on a UNIX system. Monit conducts automatic maintenance and repair
and can execute meaningful causal actions in error situations.

%prep
%autosetup

%build
%configure --disable-static --with-ssl --without-pam
%make_build

%install
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 monit.1 %{buildroot}%{_mandir}/man1/monit.1
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -p -D -m0755 monit $RPM_BUILD_ROOT%{_bindir}/monit
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/monit.d
install -p -D -m0600 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/monitrc
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log
install -m0600 /dev/null $RPM_BUILD_ROOT%{_localstatedir}/log/monit
install -p -D -m0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/monit
install -p -D -m0644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/monit.d/services-example
mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
install -m0644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_unitdir}/monit.service


%post
%systemd_post monit.service


%preun
%systemd_preun monit.service
rm -f /root/.monit.id
rm -f /root/.monit.state


%postun
%systemd_postun_with_restart monit.service


%files
%doc COPYING CHANGES
%{_unitdir}/monit.service
%config(noreplace) %{_sysconfdir}/monitrc
%config(noreplace) %{_sysconfdir}/logrotate.d/monit
%config %ghost %{_localstatedir}/log/monit
%{_sysconfdir}/monit.d/
%{_bindir}/%{name}
%{_mandir}/man1/monit.1*

%changelog
* Tue Jun 23 2026 Karl Johnson <karljohnson.it@gmail.com> - 6.0.0-1
- Bump to Monit 6.0.0

* Thu Dec 18 2025 Karl Johnson <karljohnson.it@gmail.com> - 5.35.2-1
- Add EL10 support
- Bump to Monit 5.35.2
- Remove EL6 and EL7 support, SysVinit as well

* Tue May 9 2023 Karl Johnson <karljohnson.it@gmail.com> - 5.33.0-1
- Bump to Monit 5.33.0

* Mon Sep 19 2022 Karl Johnson <karljohnson.it@gmail.com> - 5.32.0-1
- Bump to Monit 5.32.0

* Sun Feb 20 2022 Karl Johnson <karljohnson.it@gmail.com> - 5.31.0-1
- Bump to Monit 5.31.0

* Wed Feb 2 2022 Karl Johnson <karljohnson.it@gmail.com> - 5.30.0-1
- Bump to Monit 5.30.0

* Mon Nov 15 2021 Karl Johnson <karljohnson.it@gmail.com> - 5.29.0-2
- Add EL8 support

* Tue Aug 24 2021 Karl Johnson <karljohnson.it@gmail.com> - 5.29.0-1
- Bump to Monit 5.29.0

* Thu Aug 22 2019 Karl Johnson <karljohnson.it@gmail.com> - 5.26.0-1
- Bump to Monit 5.26.0

* Thu Jun 14 2018 Karl Johnson <kjohnson@aerisnetwork.com> - 5.25.2-1
- Bump to Monit 5.25.2

* Thu Aug 10 2017 Karl Johnson <kjohnson@aerisnetwork.com> - 5.23.0-1
- Bump to Monit 5.23.0

* Tue Aug 9 2016 Karl Johnson <kjohnson@aerisnetwork.com> - 5.19.0-1
- Bump to Monit 5.19.0

* Fri Jun 3 2016 Karl Johnson <kjohnson@aerisnetwork.com> - 5.18-1
- Bump to Monit 5.18

* Wed Feb 17 2016 Karl Johnson <kjohnson@aerisnetwork.com> - 5.16-1
- Bump to Monit 5.16

* Tue Dec 8 2015 Karl Johnson <kjohnson@aerisnetwork.com> - 5.15-1
- Bump to Monit 5.15

* Wed Mar 18 2015 Karl Johnson <kjohnson@aerisnetwork.com> - 5.12.1-1
- Bump to Monit 5.12.1 and add support for el7

* Mon Sep 29 2014 Karl Johnson <kjohnson@aerisnetwork.com> - 5.9-1
- Bump to Monit 5.9

* Wed Sep 17 2014 Karl Johnson <kjohnson@aerisnetwork.com> - 5.8.1-2
- Add logrotate configuration and few services

* Wed Jul 23 2014 Karl Johnson <kjohnson@aerisnetwork.com> - 5.8.1-1
- First Aeris release based on EPEL spec
