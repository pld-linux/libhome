Summary:	libhome - a configurable getpwnam(3) emulator
Summary(pl):	libhome - konfigurowalny emulator funkcji getpwnam(3)
Name:		libhome
Version:	0.8.1
Release:	0.1
License:	LGPL v2+
Group:		Libraries
Source0:	http://dl.sourceforge.net/pll/%{name}-%{version}.tar.gz
# Source0-md5:	44f06ff97b594741f0558efb51960d29
Patch0:		%{name}-DESTDIR.patch
URL:		http://pll.sourceforge.net/
BuildRequires:	automake
BuildRequires:	mysql-devel
BuildRequires:	openldap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
It supports MySQL, Open LDAP or system /etc/passwd frontend.

It's intended to replace getpwnam within system daemons who need user
authentification or identification when the users are listed on
foreign servers.

%description -l pl
Biblioteka obs³uguje MySQL, Open LDAP lub plik /etc/passwd.

Jej zadaniem jest zamiana wywo³ania getpwnam w demonach systemowych,
które potrzebuj± uwierzytelnienia lub identyfikacji u¿ytkownika w
oparciu o dane z obcych serwerów.

%package devel
Summary:	Header files for libhome library
Summary(pl):	Pliki nag³ówkowe biblioteki libhome
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libhome library.

%description devel -l pl
Pliki nag³ówkowe biblioteki libhome.

%package static
Summary:	Static libhome library
Summary(pl):	Statyczna biblioteka libhome
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libhome library.

%description static -l pl
Statyczna biblioteka libhome.

%prep
%setup -q
%patch0 -p1 -b .orig

%build
cp -f /usr/share/automake/config.* .
%configure \
	--with-ldap \
	--with-mysql
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	bindir=$RPM_BUILD_ROOT%{_bindir} \
	libdir=$RPM_BUILD_ROOT%{_libdir} \
	includedir=$RPM_BUILD_ROOT%{_includedir} \
	mandir=$RPM_BUILD_ROOT%{_mandir}

install home.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(755,root,root) %{_bindir}/home_finger
%attr(755,root,root) %{_bindir}/libhome.sh
%attr(755,root,root) %{_libdir}/libhome.so.*.*.*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/home.conf
%{_mandir}/man5/home.conf.5*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhome.so
%{_libdir}/libhome.la
%{_includedir}/home

%files static
%defattr(644,root,root,755)
%{_libdir}/libhome.a
