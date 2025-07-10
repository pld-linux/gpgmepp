#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	GpgMEpp - C++ interface for GPGME library
Summary(pl.UTF-8):	GpgMEpp - interfejs C++ do biblioteki GPGME
Name:		gpgmepp
Version:	2.0.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
Source0:	https://www.gnupg.org/ftp/gcrypt/gpgmepp/%{name}-%{version}.tar.xz
# Source0-md5:	c27f2285fe9fac54b5d1ca22e00b4594
URL:		https://www.gnupg.org/related_software/gpgme/
BuildRequires:	cmake >= 3.16
BuildRequires:	gpgme-devel >= 1:2.0.0
BuildRequires:	libgpg-error-devel >= 1.47
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	gpgme >= 1:2.0.0
Requires:	libgpg-error >= 1.47
Obsoletes:	gpgme-c++ < 1:2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GpgMEpp is a C++ wrapper (or C++ bindings) for the GnuPG project's
gpgme (GnuPG Made Easy). It's based on KF5gpgmepp library.

%description -l pl.UTF-8
GpgMEpp to interfejs C++ (wiązania C++) do biblioteki gpgme (GnuPG
Made Easy) z projektu GnuPG. Jest oparty na bibliotece KF5gpgme.pp.

%package devel
Summary:	Header files for GpgMEpp library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GpgMEpp
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gpgme-devel >= 1:2.0.0
Requires:	libgpg-error-devel >= 1.47
Requires:	libstdc++-devel >= 6:7
Obsoletes:	gpgme-c++-devel < 1:2
Conflicts:	kde4-kdepimlibs-devel

%description devel
Header files for GpgMEpp library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GpgMEpp.

%package static
Summary:	Static GpgMEpp library
Summary(pl.UTF-8):	Statyczna biblioteka GpgMEpp
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Obsoletes:	gpgme-c++-static < 1:2

%description static
Static GpgMEpp library.

%description static -l pl.UTF-8
Statyczna biblioteka GpgMEpp.

%prep
%setup -q

%build
%cmake -B build \
	-DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	%{?with_static_libs:-DENABLE_STATIC=ON}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libgpgmepp.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgpgmepp.so.7

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgpgmepp.so
%{_includedir}/gpgme++
%{_libdir}/cmake/Gpgmepp
%{_pkgconfigdir}/gpgmepp.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgpgmepp.a
%endif
