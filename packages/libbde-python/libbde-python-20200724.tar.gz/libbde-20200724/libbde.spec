Name: libbde
Version: 20200724
Release: 1
Summary: Library to access the BitLocker Drive Encryption (BDE) format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libbde
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:         openssl         
BuildRequires: gcc         openssl-devel         

%description -n libbde
Library to access the BitLocker Drive Encryption (BDE) format

%package -n libbde-static
Summary: Library to access the BitLocker Drive Encryption (BDE) format
Group: Development/Libraries
Requires: libbde = %{version}-%{release}

%description -n libbde-static
Static library version of libbde.

%package -n libbde-devel
Summary: Header files and libraries for developing applications for libbde
Group: Development/Libraries
Requires: libbde = %{version}-%{release}

%description -n libbde-devel
Header files and libraries for developing applications for libbde.

%package -n libbde-python2
Obsoletes: libbde-python < %{version}
Provides: libbde-python = %{version}
Summary: Python 2 bindings for libbde
Group: System Environment/Libraries
Requires: libbde = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libbde-python2
Python 2 bindings for libbde

%package -n libbde-python3
Summary: Python 3 bindings for libbde
Group: System Environment/Libraries
Requires: libbde = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libbde-python3
Python 3 bindings for libbde

%package -n libbde-tools
Summary: Several tools for reading BitLocker Drive Encryption volumes
Group: Applications/System
Requires: libbde = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libbde-tools
Several tools for reading BitLocker Drive Encryption volumes

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python2 --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libbde
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libbde-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libbde-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libbde.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libbde-python2
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libbde-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n libbde-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Wed Jul 29 2020 Joachim Metz <joachim.metz@gmail.com> 20200724-1
- Auto-generated

