%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	C++ library to manipulate vCard standard format
Name:		belcard
Version:	4.4.34
Release:	1
License:	GPLv3+
Group:		System/Libraries
URL:		https://linphone.org/
Source0:	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
# (wally) from OpenSUSE to install pkgconfig .pc file
Patch0:		belcard-fix-pkgconfig.patch
Patch1:		belcard-fix-cmake-dir.patch

BuildRequires:	cmake
BuildRequires:	pkgconfig(belr)
BuildRequires:	pkgconfig(udev)
BuildRequires:	bctoolbox-static-devel
BuildRequires:  ninja

%description
Belcard is a C++ library to manipulate the vCard standard format.

%files
%{_bindir}/*
%{_datadir}/belr

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	C++ library to manipulate vCard standard format
Group:		System/Libraries

%description -n %{libname}
Belcard is a C++ library to manipulate the vCard standard format.

%files -n %{libname}
%{_libdir}/lib%{name}.so.*

#---------------------------------------------------------------------------

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains development files for %{name}

%files -n %{develname}
%doc README.md
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/?elcard/
%{_libdir}/pkgconfig/%{name}.pc

#---------------------------------------------------------------------------

%prep
%autosetup -p1

sed -i -e 's,\r$,,' CMakeLists.txt

# Fix version
sed -i -e '/BELCARD/s/\(VERSION\)\s\+[0-9]\(\.[0-9]\)\+/\1 %{version}/' CMakeLists.txt

%build
%cmake \
  -DENABLE_STATIC:BOOL=NO \
  -DENABLE_STRICT:BOOL=NO \
  -DENABLE_UNIT_TESTS=NO \
  -DENABLE_UNIT_TESTS:BOOL=OFF \
  -G Ninja

%ninja_build

%install
%ninja_install -C build

find %{buildroot} -name "*.la" -delete
