Summary:	libhome - a configurable getpwnam(3) emulator
Summary(pl.UTF-8):	libhome - konfigurowalny emulator funkcji getpwnam(3)
Name:		libhome
Version:	0.10.2
Release:	8
License:	LGPL v2+
Group:		Libraries
Source0:	https://downloads.sourceforge.net/pll/%{name}-%{version}.tar.gz
# Source0-md5:	f7129ae34d3c44d38ac785e7a1f7d509
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-db53.patch
URL:		https://pll.sourceforge.net/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	db-devel >= 4
BuildRequires:	groff
BuildRequires:	libtool
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel >= 2.4.6
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
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libhome
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	db-devel >= 4
Requires:	mysql-devel
Requires:	openldap-devel >= 2.4.6
Requires:	pam-devel
Requires:	postgresql-devel

%description devel
Header files for libhome library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libhome.

%package static
Summary:	Static libhome library
Summary(pl.UTF-8):	Statyczna biblioteka libhome
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libhome library.

%description static -l pl.UTF-8
Statyczna biblioteka libhome.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
# no automake call needed, automake is not in use here
%configure \
	--with-db4=%{_includedir} \
	--with-ldap \
	--with-mysql \
	--with-pgsql \
	--with-pam \
	--with-proxy

%{__make} \
	CFLAGS="%{rpmcflags}"

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
%attr(755,root,root) %{_bindir}/home_finger
%attr(755,root,root) %{_bindir}/home_su
%attr(755,root,root) %{_bindir}/libhome.sh
%attr(755,root,root) %{_sbindir}/home_proxy
%attr(755,root,root) %{_libdir}/libhome.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhome.so.1
%attr(755,root,root) %{_libdir}/libnss_home_proxy.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnss_home_proxy.so.2
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/home.conf
%{_mandir}/man5/home.conf.5*
%{_mandir}/man8/home_proxy.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhome.so
%attr(755,root,root) %{_libdir}/libnss_home_proxy.so
%{_libdir}/libhome.la
%{_libdir}/libnss_home_proxy.la
%{_includedir}/home

%files static
%defattr(644,root,root,755)
%{_libdir}/libhome.a
%{_libdir}/libnss_home_proxy.a
