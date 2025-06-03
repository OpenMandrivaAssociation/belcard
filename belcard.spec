%define major 1
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

# exclude unwanted cmake requires
%global __provides_exclude_from ^%{_datadir}/cmake/.*/Find.*cmake$

%bcond strict			1
%bcond unit_tests		1
%bcond unit_tests_install	0
%bcond tests			1

Summary:	C++ library to manipulate vCard standard format
Name:		belcard
Version:	5.4.20
Release:	1
License:	GPLv3+
Group:		System/Libraries
URL:		https://linphone.org/
Source0:	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
# (wally) from OpenSUSE to install pkgconfig .pc file
Patch0:		belcard-fix-pkgconfig.patch
Patch1:		belcard-5.3.6-fix-cmake-dir.patch

BuildRequires:	cmake
BuildRequires:	pkgconfig(belr)
BuildRequires:	pkgconfig(udev)
BuildRequires:	ninja

%description
Belcard is a C++ library to manipulate the vCard standard format.

%files
#%%{_bindir}/*
%{_bindir}/%{name}-folder
%{_bindir}/%{name}-parser
%{_bindir}/%{name}-unfolder
%{_datadir}/belr
%if %{with unit_tests} && %{with unit_tests_install}
%{_bindir}/%{name}-tester
%{_datadir}/%{name}-tester/
%endif

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	C++ library to manipulate vCard standard format
Group:		System/Libraries

%description -n %{libname}
Belcard is a C++ library to manipulate the vCard standard format.

%files -n %{libname}
%{_libdir}/lib%{name}.so.*

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains development files for %{name}

%files -n %{devname}
%doc README.md
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/cmake/BelCard/

#---------------------------------------------------------------------------

%prep
%autosetup -p1

sed -i -e 's,\r$,,' CMakeLists.txt

# Fix version
sed -i -e '/BELCARD/s/\(VERSION\)\s\+[0-9]\(\.[0-9]\)\+/\1 %{version}/' CMakeLists.txt

%build
%cmake \
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DENABLE_UNIT_TESTS:BOOL=%{?with_unit_tests:ON}%{?!with_unit_tests:OFF} \
	-DENABLE_TESTS:BOOL=%{?with_tests:ON}%{?!with_tests:OFF} \
	-G Ninja
%ninja_build

%install
%ninja_install -C build

# don't install unit tester
%if %{with unit_tests} && ! %{with unit_tests_install}
rm -f  %{buildroot}%{_bindir}/%{name}-tester
rm -fr %{buildroot}%{_datadir}/%{name}-tester/
%endif

%check
%if %{with unit_tests}
pushd build
ctest
popd
%endif

