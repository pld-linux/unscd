Summary:	Single threaded NSCD implementation
Name:		unscd
Version:	0.47
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://busybox.net/~vda/unscd/nscd-%{version}.c
# Source0-md5:	90af0b57648d2199209051f0d57ba286
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Single threaded NSCD (Name Service Caching Daemon) implementation.

nscd caches name service lookups; it can dramatically improve
performance with NIS+, and may help with DNS as well.

%prep
%setup -qcT
sed -ne '/Description:/,/\*\*\*/p' %{SOURCE0} > README

%build
%{__cc} -o %{name} %{rpmcflags} -Os %{rpmcppflags} %{rpmldflags} -Wall -Wunused-parameter -Wl,--sort-section -Wl,alignment -Wl,--sort-common %{SOURCE0}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -p %{name} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/%{name}
