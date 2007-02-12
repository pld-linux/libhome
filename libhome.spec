Summary:	libhome - a configurable getpwnam(3) emulator
Summary(pl.UTF-8):   libhome - konfigurowalny emulator funkcji getpwnam(3)
Name:		libhome
Version:	0.10.1
Release:	3
License:	LGPL v2+
Group:		Libraries
Source0:	http://dl.sourceforge.net/pll/%{name}-%{version}.tar.gz
# Source0-md5:	fe0b4e581c62bc64eb13295eb7f2b0e5
Patch0:		%{name}-DESTDIR.patch
URL:		http://pll.sourceforge.net/
BuildRequires:	automake
BuildRequires:	groff
BuildRequires:	db-devel
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	postgresql-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
It supports MySQL, Open LDAP or system /etc/passwd frontend.

It's intended to replace getpwnam within system daemons who need user
authentification or identification when the users are listed on
foreign servers.

%description -l pl.UTF-8
Biblioteka obsługuje MySQL, Open LDAP lub plik /etc/passwd.

Jej zadaniem jest zamiana wywołania getpwnam w demonach systemowych,
które potrzebują uwierzytelnienia lub identyfikacji użytkownika w
oparciu o dane z obcych serwerów.

%package devel
Summary:	Header files for libhome library
Summary(pl.UTF-8):   Pliki nagłówkowe biblioteki libhome
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	db-devel
Requires:	mysql-devel
Requires:	openldap-devel
Requires:	pam-devel
Requires:	postgresql-devel

%description devel
Header files for libhome library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libhome.

%package static
Summary:	Static libhome library
Summary(pl.UTF-8):   Statyczna biblioteka libhome
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libhome library.

%description static -l pl.UTF-8
Statyczna biblioteka libhome.

%prep
%setup -q
%patch0 -p1 -b .orig

%build
cp -f /usr/share/automake/config.* .
%configure \
	--with-db4=%{_includedir} \
	--with-ldap \
	--with-mysql \
	--with-pgsql \
	--with-pam
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	bindir=%{_bindir} \
	libdir=%{_libdir} \
	includedir=%{_includedir} \
	mandir=%{_mandir}

install home.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_bindir}/home_*
%attr(755,root,root) %{_sbindir}/home_*
%attr(755,root,root) %{_bindir}/libhome.sh
%attr(755,root,root) %{_libdir}/lib*home*.so.*.*.*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/home.conf
%{_mandir}/man5/home.conf.5*
%{_mandir}/man8/home_proxy.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*home*.so
%{_libdir}/lib*home*.la
%{_includedir}/home

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*home*.a
