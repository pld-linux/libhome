Summary:	libhome - a configurable getpwnam(3) emulator
Summary(pl):	libhome - konfigurowalny emulator funkcji getpwnam(3)
Name:		libhome
Version:	0.8.1
Release:	0.1
License:	LGPL v2
Group:		Libraries
Source0:	http://dl.sourceforge.net/pll/%{name}-%{version}.tar.gz
# Source0-md5:	44f06ff97b594741f0558efb51960d29
URL:		http://pll.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
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

%prep
%setup -q

%build
# ???
#%%{__libtoolize}
#%%{__aclocal}
#%%{__autoconf}
#%%{__autoheader}
#%%{__automake}
%configure \
	--with-ldap \
	--with-mysql
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}

# XXX: use make install
install .libs/home_finger $RPM_BUILD_ROOT%{_bindir}
install .libs/libhome.so.1.* $RPM_BUILD_ROOT%{_libdir}
cp -a .libs/libhome.so $RPM_BUILD_ROOT%{_libdir}
install home.conf $RPM_BUILD_ROOT%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS README VERSION COPYING
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/libhome.so.*.*.*
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
