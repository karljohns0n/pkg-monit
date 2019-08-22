%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7)

Name:					monit
Version:				5.25.2
Release:				1%{?dist}
Summary:				Process monitor and restart utility

Group:					Utilities/Console
License:				GPLv3+
URL:					http://mmonit.com/monit/
Source0:				http://mmonit.com/monit/dist/%{name}-%{version}.tar.gz
Source2:				monitrc
Source3:				monit.el6.logrotate
Source4:				monit.el7.logrotate
Source5:    		    monit.service
Source6:				services-el6-conf
Source7:				services-el7-conf

BuildRoot:				%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:			openssl-devel

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
install -p -D -m0600 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/monitrc
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log
install -m0600 /dev/null $RPM_BUILD_ROOT%{_localstatedir}/log/monit

%if %{use_systemd}
	mkdir -p ${RPM_BUILD_ROOT}%{_unitdir}
	install -m0644 %{SOURCE5} ${RPM_BUILD_ROOT}%{_unitdir}/monit.service
	install -p -D -m0644 %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/monit.d/services-exemple
%else
	install -p -D -m0755 system/startup/rc.monit $RPM_BUILD_ROOT%{_initrddir}/monit
	install -p -D -m0644 %{SOURCE6} $RPM_BUILD_ROOT%{_sysconfdir}/monit.d/services-exemple
%endif

%if %{use_systemd}
	install -p -D -m0644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/monit
%else
	install -p -D -m0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/monit
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
%doc COPYING README CHANGES
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