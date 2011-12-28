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

%{name}.caches name service lookups; it can dramatically improve
performance with NIS+, and may help with DNS as well.

%prep
%setup -qcT
cp -p %{SOURCE0} %{name}.c
sed -ne '/Description:/,/\*\*\*/p' %{name}.c > README

%build
%{__cc} -o %{name}.o %{rpmcflags} %{rpmcppflags} -Wall -Wunused-parameter -Os %{name}.c
%{__cc} -o %{name} %{rpmldflags} -fomit-frame-pointer -Wl,--sort-section -Wl,alignment -Wl,--sort-common -Os %{name}.o

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -p %{name} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%{_sbindir}/%{name}
