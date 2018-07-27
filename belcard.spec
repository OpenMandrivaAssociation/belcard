%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	C++ library to manipulate vCard standard format
Name:		belcard
Version:	1.0.2
Release:	1
License:	GPLv3+
Group:		System/Libraries
URL:		https://linphone.org/
Source0:	https://linphone.org/releases/sources/belcard/belcard-%{version}.tar.gz
Source1:	https://linphone.org/releases/sources/belcard/belcard-%{version}.tar.gz.md5
# (wally) from OpenSUSE to install pkgconfig .pc file
Patch0:		belcard-fix-pkgconfig.patch
# (wally) alow overriding cmake config file location from cmd line
Patch1:         belcard-1.0.2-cmake-config-location.patch
BuildRequires:	cmake
BuildRequires:	pkgconfig(belr)
BuildRequires:	pkgconfig(udev)

%description
Belcard is a C++ library to manipulate the vCard standard format.

%package -n	%{libname}
Summary:	C++ library to manipulate vCard standard format
Group:		System/Libraries

%description -n	%{libname}
Belcard is a C++ library to manipulate the vCard standard format.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
This package contains development files for %{name}

%prep
%setup -qn %{name}-%{version}-0
sed -i -e 's,\r$,,' CMakeLists.txt
%apply_patches

%build
%cmake \
  -DENABLE_STATIC:BOOL=NO \
  -DENABLE_STRICT:BOOL=NO \
  -DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/Belcard
%make

%install
%makeinstall_std -C build

find %{buildroot} -name "*.la" -delete

%files
%doc README.md COPYING
%{_bindir}/*

%files -n %{libname}
%doc AUTHORS NEWS README.md COPYING
%{_libdir}/lib%{name}.so.*

%files -n %{develname}
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/Belcard/
%{_libdir}/pkgconfig/%{name}.pc

