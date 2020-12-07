Name:           vmaf
Version:        2.0.0
#As per RPM guidelines (https://docs.fedoraproject.org/en-US/packaging-guidelines/Versioning/) we use a release starting with a 0, as they're on release candidate
Release:        0.1.rc.foo.6b915e2%{?dist}
Summary:        Video Multi-Method Assessment Fusion

License:        BSD-2-Clause-Patent
URL:            https://github.com/foosoftsrl/vmaf
Source0:        %{url}/archive/6b915e2c90b39beb6555b5dcb43966a40d137baa.tar.gz

# This project relies on AVX
ExclusiveArch:  x86_64

BuildRequires:  gcc-c++
BuildRequires:  meson
BuildRequires:  devtoolset-9-gcc-c++

# Enforce our own build version for library
Requires:       libvmaf%{?_isa} = %{version}-%{release}

%description
VMAF is a perceptual video quality assessment algorithm developed by
Netflix. VMAF Development Kit (VDK) is a software package that contains
the VMAF algorithm implementation, as well as a set of tools that allows
a user to train and test a custom VMAF model. For an overview, read this
tech blog post, or this slide deck.

https://github.com/Netflix/vmaf/blob/master/resource/doc/VMAF_ICIP17.pdf

%package -n     libvmaf
Summary:        Library for %{name}
#Some repo provides it
Provides: %{name}-static = %{version}-%{release}
Obsoletes: %{name}-static < %{version}-%{release}

%description -n libvmaf
Library for %{name}.

%package -n     libvmaf-devel
Summary:        Development files for %{name}
Requires:       libvmaf%{?_isa} = %{version}-%{release}
#Some repo provides it
Provides: %{name}-devel = %{version}-%{release}
Obsoletes: %{name}-devel < %{version}-%{release}

%description -n libvmaf-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -n vmaf-6b915e2c90b39beb6555b5dcb43966a40d137baa

%build
. /opt/rh/devtoolset-9/enable
pushd libvmaf
mkdir build
cd build
meson --prefix /usr ..
ninja
popd

%install
pushd libvmaf/build
DESTDIR=%{buildroot} meson install
popd

%files
%doc FAQ.md README.md
%{_bindir}/vmaf

%files -n libvmaf
%doc CHANGELOG.md
%license LICENSE
%{_libdir}/*.so.*

%files -n libvmaf-devel
%doc CONTRIBUTING.md
#%{rpmmacrodir}/macros.%{name}
%{_includedir}/libvmaf/
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/libvmaf.pc


%changelog
* Mon Dec 07 2020 Luca Piccarreta <luca.picarreta@foosoft.it> - 2.0.0-0.1.rc.foo
- Initial SPEC file. Heavily inspired from Fedora
