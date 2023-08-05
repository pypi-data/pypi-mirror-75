Name: libqcow
Version: 20200729
Release: 1
Summary: Library to access the QEMU Copy-On-Write (QCOW) image file format
Group: System Environment/Libraries
License: LGPL
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libqcow
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:         openssl      zlib
BuildRequires: gcc         openssl-devel      zlib-devel

%description -n libqcow
Library to access the QEMU Copy-On-Write (QCOW) image file format

%package -n libqcow-static
Summary: Library to access the QEMU Copy-On-Write (QCOW) image file format
Group: Development/Libraries
Requires: libqcow = %{version}-%{release}

%description -n libqcow-static
Static library version of libqcow.

%package -n libqcow-devel
Summary: Header files and libraries for developing applications for libqcow
Group: Development/Libraries
Requires: libqcow = %{version}-%{release}

%description -n libqcow-devel
Header files and libraries for developing applications for libqcow.

%package -n libqcow-python2
Obsoletes: libqcow-python < %{version}
Provides: libqcow-python = %{version}
Summary: Python 2 bindings for libqcow
Group: System Environment/Libraries
Requires: libqcow = %{version}-%{release} python2
BuildRequires: python2-devel

%description -n libqcow-python2
Python 2 bindings for libqcow

%package -n libqcow-python3
Summary: Python 3 bindings for libqcow
Group: System Environment/Libraries
Requires: libqcow = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libqcow-python3
Python 3 bindings for libqcow

%package -n libqcow-tools
Summary: Several tools for reading QEMU Copy-On-Write (QCOW) image files
Group: Applications/System
Requires: libqcow = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libqcow-tools
Several tools for reading QEMU Copy-On-Write (QCOW) image files

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

%files -n libqcow
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libqcow-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libqcow-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/libqcow.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libqcow-python2
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python2*/site-packages/*.a
%{_libdir}/python2*/site-packages/*.la
%{_libdir}/python2*/site-packages/*.so

%files -n libqcow-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.la
%{_libdir}/python3*/site-packages/*.so

%files -n libqcow-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Wed Jul 29 2020 Joachim Metz <joachim.metz@gmail.com> 20200729-1
- Auto-generated

