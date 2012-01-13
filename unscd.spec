Summary:	Single threaded NSCD implementation
Name:		unscd
Version:	0.48
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://busybox.net/~vda/unscd/nscd-%{version}.c
# Source0-md5:	d0e2ea863aa4f6724901c8fec24022b9
Source1:	nscd.init
Source2:	nscd.sysconfig
Source3:	nscd.logrotate
Source4:	nscd.conf
URL:		http://busybox.net/~vda/unscd/
Provides:	group(nscd)
Requires(post):	fileutils
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts >= 0.2.0
Provides:	user(nscd)
Obsoletes:	nscd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Single threaded NSCD (Name Service Caching Daemon) implementation.

nscd caches name service lookups; it can dramatically improve
performance with NIS+, and may help with DNS as well.

%prep
%setup -qcT
sed -ne '/Description:/,/\*\*\*/p' %{SOURCE0} > README

%build
%{__cc} -o nscd %{rpmcflags} -Os %{rpmcppflags} %{rpmldflags} -Wall -Wunused-parameter -Wl,--sort-section -Wl,alignment -Wl,--sort-common %{SOURCE0}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},/var/log,/var/run/nscd,/etc/{logrotate.d,rc.d/init.d,sysconfig}}
install -p nscd $RPM_BUILD_ROOT%{_sbindir}
install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/nscd
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/nscd
cp -a %{SOURCE3} $RPM_BUILD_ROOT/etc/logrotate.d/nscd
cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}
: > $RPM_BUILD_ROOT/var/log/nscd

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -P nscd -g 144 -r nscd
%useradd -P nscd -u 144 -r -d /tmp -s /bin/false -c "Name Service Cache Daemon" -g nscd nscd

%post
if [ ! -f /var/log/nscd ]; then
	umask 027
	touch /var/log/nscd
	chown root:root /var/log/nscd
	chmod 640 /var/log/nscd
fi
/sbin/chkconfig --add nscd
%service nscd restart "Name Service Cache Daemon"

%preun
if [ "$1" = "0" ]; then
	%service nscd stop
	/sbin/chkconfig --del nscd
fi

%postun
if [ "$1" = "0" ]; then
	%userremove nscd
	%groupremove nscd
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/nscd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nscd.conf
%attr(754,root,root) /etc/rc.d/init.d/nscd
%attr(755,root,root) %{_sbindir}/nscd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/nscd
%attr(640,root,root) %ghost /var/log/nscd
%dir /var/run/nscd
