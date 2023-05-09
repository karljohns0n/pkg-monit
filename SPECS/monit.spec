%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

Name:					monit
Version:				5.33.0
Release:				1%{?dist}
Summary:				Process monitor and restart utility

Group:					Utilities/Console
License:				GPLv3+
URL:					http://mmonit.com/monit/
Source0:				http://mmonit.com/monit/dist/%{name}-%{version}.tar.gz
Source1:				monitrc
%if %{use_systemd}
Source2:				monit.service
Source3:				monit.systemd.logrotate
Source4:				services.systemd.conf
%else
Source3:				monit.rc.logrotate
Source4:				services.rc.conf
%endif


BuildRoot:				%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:			openssl-devel zlib-devel

%if %{use_systemd}
BuildRequires:			systemd
Requires(post):			systemd, systemd-sysv
Requires(preun):		systemd
Requires(postun):		systemd
%else
Requires(post):			chkconfig
Requires(preun):		chkconfig, initscripts
Requires(postun):		initscripts
%endif

%description
monit is a utility for managing and monitoring, processes, files, directories
and devices on a UNIX system. Monit conducts automatic maintenance and repair
and can execute meaningful causal actions in error situations.

%prep
%setup -q

%build
%configure --disable-static --with-ssl --without-pam
make %{?_smp_mflags}

%install
if [ -d %{buildroot} ] ; then
	rm -rf %{buildroot}
fi


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

%if %{use_systemd}
	mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
	install -m0644 %{SOURCE2} ${RPM_BUILD_ROOT}%{_unitdir}/monit.service
	
%else
	install -p -D -m0755 system/startup/rc.monit $RPM_BUILD_ROOT%{_initrddir}/monit
%endif


%clean
if [ -d %{buildroot} ] ; then
	rm -rf %{buildroot}
fi


%post
%if %{use_systemd}
	%systemd_post monit.service
%else
if [ $1 -eq 1 ]; then
	/sbin/chkconfig --add monit
fi
%endif


%preun
%if %{use_systemd}
	%systemd_preun monit.service
%else
	if [ $1 = 0 ]; then
		/sbin/service monit stop >/dev/null 2>&1
		/sbin/chkconfig --del monit
	fi
%endif
rm -f /root/.monit.id
rm -f /root/.monit.state


%postun
%if %{use_systemd}
	%systemd_postun_with_restart monit.service
%else
	if [ "$1" -ge "1" ]; then
		/sbin/service monit condrestart >/dev/null 2>&1 || :
	fi
%endif


%files
%defattr(-,root,root,-)
%doc COPYING CHANGES
%if %{use_systemd}
	%{_unitdir}/monit.service
%else
	%{_initrddir}/monit
%endif
%config(noreplace) %{_sysconfdir}/monitrc
%config(noreplace) %{_sysconfdir}/logrotate.d/monit
%config %ghost %{_localstatedir}/log/monit
%{_sysconfdir}/monit.d/
%{_bindir}/%{name}
%{_mandir}/man1/monit.1*

%changelog
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