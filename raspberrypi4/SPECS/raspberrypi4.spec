%global commit_firmware_long c2c6ce8de2dcfd5a6852a32a16003f25188e52ee
#%global commit_firmware_short %(c=%{commit_firmware_long}; echo ${c:0:7})
%global commit_linux_long a75a01501330a9be188561b0e9da1da6da372eea
#%global commit_linux_short %(c=%{commit_linux_long}; echo ${c:0:7})

%define Arch arm
%define local_version v7l
%define extra_version 1

Name:           raspberrypi4
Version:        4.19.113
Release:        %{local_version}.%{extra_version}%{?dist}
Summary:        Specific kernel and bootcode for Raspberry Pi

License:        GPLv2
URL:            https://github.com/raspberrypi/linux
Source0:        https://github.com/raspberrypi/linux/archive/%{commit_linux_long}.tar.gz
Source1:        https://github.com/raspberrypi/firmware/archive/%{commit_firmware_long}.tar.gz
BuildRequires: kmod, patch, bash, sh-utils, tar
BuildRequires: bzip2, xz, findutils, gzip, m4, perl, perl-Carp, make, diffutils, gawk
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc
BuildRequires: net-tools, hostname, bc
BuildRequires: elfutils-devel zlib-devel binutils-devel newt-devel python-devel perl(ExtUtils::Embed) bison flex xz-devel
BuildRequires: audit-libs-devel
BuildRequires: pciutils-devel gettext ncurses-devel
BuildRequires: openssl-devel

# Compile with SELinux but disable per default
Patch0:         bcm2711_selinux_config.patch

%description
Specific kernel and bootcode for Raspberry Pi

%package kernel
Group:          System Environment/Kernel
Summary:        The Linux kernel
Provides:       kernel = %{version}-%{release}
Requires:	coreutils
#Requires:	dracut

%description kernel
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.


%package kernel-devel
Group:          System Environment/Kernel
Summary:        Development package for building kernel modules to match the kernel
Provides:       kernel-devel = %{version}-%{release}

%description kernel-devel
This package provides kernel headers and makefiles sufficient to build modules
against the kernel package.


%package firmware
Summary:        GPU firmware for the Raspberry Pi computer
License:        Redistributable, with restrictions; see LICENSE.broadcom
Obsoletes:      grub, grubby, efibootmgr

%description firmware
This package contains the GPU firmware for the Raspberry Pi BCM2835 SOC
including the kernel bootloader.


%prep
%setup -q -n linux-%{commit_linux_long}
%patch0 -p1
perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}/" Makefile
perl -p -i -e "s/^CONFIG_LOCALVERSION=.*/CONFIG_LOCALVERSION=/" arch/%{Arch}/configs/bcm2711_defconfig

%build
export KERNEL=kernel7l
make bcm2711_defconfig
make %{?_smp_mflags} zImage modules dtbs

%install
# kernel
mkdir -p %{buildroot}/boot/overlays/
mkdir -p %{buildroot}/usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays
cp -p -v COPYING %{buildroot}/boot/COPYING.linux-4.19
cp -p -v arch/%{Arch}/boot/dts/*.dtb %{buildroot}/usr/share/%{name}-kernel/%{version}-%{release}/boot
cp -p -v arch/%{Arch}/boot/dts/overlays/*.dtb* %{buildroot}/usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays
cp -p -v arch/%{Arch}/boot/dts/overlays/README %{buildroot}/usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays
#scripts/mkknlimg arch/%{Arch}/boot/zImage %{buildroot}/boot/kernel-%{version}-%{release}.img
cp -p -v arch/%{Arch}/boot/zImage %{buildroot}/boot/kernel-%{version}-%{release}.img
make INSTALL_MOD_PATH=%{buildroot} modules_install

# kernel-devel
DevelDir=/usr/src/kernels/%{version}-%{release}
mkdir -p %{buildroot}$DevelDir
# first copy everything
cp -p -v Module.symvers System.map %{buildroot}$DevelDir
cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` %{buildroot}$DevelDir
# then drop all but the needed Makefiles/Kconfig files
rm -rf %{buildroot}$DevelDir/Documentation
rm -rf %{buildroot}$DevelDir/scripts
rm -rf %{buildroot}$DevelDir/include
cp .config %{buildroot}$DevelDir
cp -a scripts %{buildroot}$DevelDir
cp -a include %{buildroot}$DevelDir

if [ -d arch/%{Arch}/scripts ]; then
  cp -a arch/%{Arch}/scripts %{buildroot}$DevelDir/arch/%{_arch} || :
fi
if [ -f arch/%{Arch}/*lds ]; then
  cp -a arch/%{Arch}/*lds %{buildroot}$DevelDir/arch/%{_arch}/ || :
fi
rm -f %{buildroot}$DevelDir/scripts/*.o
rm -f %{buildroot}$DevelDir/scripts/*/*.o
cp -a --parents arch/%{Arch}/include %{buildroot}$DevelDir
# include the machine specific headers for ARM variants, if available.
if [ -d arch/%{Arch}/mach-bcm2711/include ]; then
  cp -a --parents arch/%{Arch}/mach-bcm2711/include %{buildroot}$DevelDir
fi
cp include/generated/uapi/linux/version.h %{buildroot}$DevelDir/include/linux
touch -r %{buildroot}$DevelDir/Makefile %{buildroot}$DevelDir/include/linux/version.h
ln -T -s $DevelDir %{buildroot}/lib/modules/%{version}-%{release}/build --force
ln -T -s build %{buildroot}/lib/modules/%{version}-%{release}/source --force

pushd %{buildroot}
tar -xf %{_sourcedir}/%{commit_firmware_long}.tar.gz \
    firmware-%{commit_firmware_long}/boot/start4* \
    firmware-%{commit_firmware_long}/boot/fixup4* \
    firmware-%{commit_firmware_long}/boot/LICENCE.broadcom \
    firmware-%{commit_firmware_long}/boot/bootcode.bin \
    --strip-components=1
popd

%files kernel
%defattr(-,root,root,-)
/lib/modules/%{version}-%{release}
/usr/share/%{name}-kernel/%{version}-%{release}
/usr/share/%{name}-kernel/%{version}-%{release}/boot
/usr/share/%{name}-kernel/%{version}-%{release}/boot/*.dtb
/boot/overlays/
/usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays/*
%attr(0755,root,root) /boot/kernel-%{version}-%{release}.img
%doc /boot/COPYING.linux-4.19


%posttrans kernel
cp /boot/kernel-%{version}-%{release}.img /boot/kernel7l.img
cp /usr/share/%{name}-kernel/%{version}-%{release}/boot/*.dtb /boot/
cp /usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays/*.dtb* /boot/overlays/
cp /usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays/README /boot/overlays/

%postun kernel
cp $(ls -1 /boot/kernel-*-*|sort -V|tail -1) /boot/kernel7l.img
cp $(ls -1d /usr/share/%{name}-kernel/*-*/|sort -V|tail -1)/boot/*.dtb /boot/
cp $(ls -1d /usr/share/%{name}-kernel/*-*/|sort -V|tail -1)/boot/overlays/*.dtb* /boot/overlays/
cp $(ls -1d /usr/share/%{name}-kernel/*-*/|sort -V|tail -1)/boot/overlays/README /boot/overlays/


%files kernel-devel
%defattr(-,root,root)
/usr/src/kernels/%{version}-%{release}


%files firmware
%defattr(-,root,root,-)
/boot/bootcode.bin
/boot/fixup4*
/boot/start4*
%doc /boot/LICENCE.broadcom

%changelog
* Fri Apr 03 2020 Jacco Ligthart <jacco@redsleeve.org> - 4.19.113-v7l.1.el7
- update to version 4.19.113

* Sat Sep 28 2019 Jacco Ligthart <jacco@redsleeve.org> - 4.19.75-v7l.1.el7
- updated to version 4.19.75

* Fri Jul 19 2019 Jacco Ligthart <jacco@redsleeve.org> - 4.19.58-v7l.1.el7
- initial version 4.19.58 for rpi4
