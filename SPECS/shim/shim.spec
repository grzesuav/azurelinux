
%global openssl_vre 1.0.2k

%ifarch x86_64
%global efiarch x64
%endif
%ifarch aarch64
%global efiarch aa64
%endif

Name:		shim
Version:	15.8
Release:	1%{?dist}
Summary:	First-stage UEFI bootloader
License:	BSD-3-Clause
URL:		https://github.com/rhboot/shim/

ExclusiveArch:	x86_64 aarch64

BuildRequires:	pesign
BuildRequires:  shim-unsigned-%{efiarch}

%description
Initial UEFI bootloader that handles chaining to a trusted full bootloader
under secure boot environments. This package contains the version signed by
the UEFI signing service.

%package %{efiarch}
Requires:       mokutil
Provides:       shim-signed-%{efiarch}
Provides:       shim = %{version}-%{release}
Provides:       shim-signed = %{version}-%{release}
Obsoletes:      shim < %{version}-%{release}
Obsoletes:      shim-signed < %{version}-%{release}
#Conflicts:      grub2-efi-binary < ...
#Recommends:     grub2-efi-binary >= ...
Provides:	bundled(openssl) = %{openssl_vre}

%prep
cd %{_builddir}
rm -rf shim-%{version}
mkdir shim-%{version}

%build
cd shim-%{version}
%define_build -a %{efi_arch} -A %{efi_arch_upper} -i %{shimefi} -b no -c %{is_signed} -d %{shimdir}

%install
rm -rf $RPM_BUILD_ROOT
cd shim-%{version}
install -D -d -m 0755 $RPM_BUILD_ROOT/boot/
install -D -d -m 0700 $RPM_BUILD_ROOT%{efi_esp_root}/
install -D -d -m 0700 $RPM_BUILD_ROOT%{efi_esp_efi}/
install -D -d -m 0700 $RPM_BUILD_ROOT%{efi_esp_dir}/
install -D -d -m 0700 $RPM_BUILD_ROOT%{efi_esp_boot}/

%do_install -a %{efi_arch} -A %{efi_arch_upper} -b %{bootcsv}

install -D -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/dnf/protected.d/
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/dnf/protected.d/

( cd $RPM_BUILD_ROOT ; find .%{efi_esp_root} -type f ) \
  | sed -e 's/\./\^/' -e 's,^\\\./,.*/,' -e 's,$,$,' > %{__brp_mangle_shebangs_exclude_from_file}

%define_files -a %{efi_arch} -A %{efi_arch_upper}
%{_sysconfdir}/dnf/protected.d/shim.conf

%changelog
* Tue Feb 08 2022 Chris Co <chrco@microsoft.com> - 15.4-2
- Update signed shim binary to newer one associated with 15.4-2 unsigned build.
- License verified

* Fri Apr 16 2021 Chris Co <chrco@microsoft.com> - 15.4-1
- Original version for CBL-Mariner.
