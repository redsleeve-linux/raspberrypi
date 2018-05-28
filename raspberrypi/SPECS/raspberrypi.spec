%global commit_firmware_long  6a3ac305d65cff090d1a8d4444d12d5c81989ab9
%global commit_firmware_short %(c=%{commit_firmware_long}; echo ${c:0:7})
%global commit_linux_long ec05b1a7860dbeee7d3fc3390c4d2ba8ddaeb8a9
%global commit_linux_short %(c=%{commit_linux_long}; echo ${c:0:7})

%define Arch arm
%define extra_version 1

Name:           raspberrypi
Version:        4.14.42
Release:        %{extra_version}%{?dist}
Summary:        Specific kernel and bootcode for Raspberry Pi

License:        GPLv2
URL:            https://github.com/raspberrypi/linux
Source0:        https://github.com/raspberrypi/linux/tarball/%{commit_linux_long}
Source1:        https://github.com/raspberrypi/firmware/tarball/%{commit_firmware_long}
BuildRequires: kmod, patch, bash, sh-utils, tar
BuildRequires: bzip2, xz, findutils, gzip, m4, perl, perl-Carp, make, diffutils, gawk
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc
BuildRequires: net-tools, hostname, bc
BuildRequires: elfutils-devel zlib-devel binutils-devel newt-devel python-devel perl(ExtUtils::Embed) bison flex xz-devel
BuildRequires: audit-libs-devel
BuildRequires: pciutils-devel gettext ncurses-devel

# Compile with SELinux but disable per default
Patch0:         bcmrpi_selinux_config.patch

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


#%package kernel-firmware
#Group:          Development/System
#Summary:        Firmware files used by the Linux kernel
#Provides:       kernel-firmware = %{version}-%{release}

#%description kernel-firmware
#Kernel-firmware includes firmware files required for some devices to
#operate.


%package firmware
Summary:        GPU firmware for the Raspberry Pi computer
License:        Redistributable, with restrictions; see LICENSE.broadcom
Obsoletes:      grub, grubby, efibootmgr

%description firmware
This package contains the GPU firmware for the Raspberry Pi BCM2835 SOC
including the kernel bootloader.


%prep
%setup -q -n raspberrypi-linux-%{commit_linux_short}
%patch0 -p1
perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{release}/" Makefile

%build
export KERNEL=kernel
make bcmrpi_defconfig
make %{?_smp_mflags} zImage modules dtbs

%install
# kernel
mkdir -p %{buildroot}/boot/overlays/
mkdir -p %{buildroot}/usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays
cp -p -v COPYING %{buildroot}/boot/COPYING.linux
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
if [ -d arch/%{Arch}/mach-bcm2708/include ]; then
  cp -a --parents arch/%{Arch}/mach-bcm2708/include %{buildroot}$DevelDir
fi
cp include/generated/uapi/linux/version.h %{buildroot}$DevelDir/include/linux
touch -r %{buildroot}$DevelDir/Makefile %{buildroot}$DevelDir/include/linux/version.h
ln -T -s $DevelDir %{buildroot}/lib/modules/%{version}-%{release}/build --force
ln -T -s build %{buildroot}/lib/modules/%{version}-%{release}/source --force

# kernel-firmware
#rm .config
#make INSTALL_FW_PATH=%{buildroot}/lib/firmware firmware_install

# firmware
#   precompiled GPU firmware and bootloader
pushd %{buildroot}
tar -xf %{_sourcedir}/%{commit_firmware_long} \
    raspberrypi-firmware-%{commit_firmware_short}/boot/start* \
    raspberrypi-firmware-%{commit_firmware_short}/boot/fixup* \
    raspberrypi-firmware-%{commit_firmware_short}/boot/LICENCE.broadcom \
    raspberrypi-firmware-%{commit_firmware_short}/boot/bootcode.bin \
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
%doc /boot/COPYING.linux


%post kernel
cp /boot/kernel-%{version}-%{release}.img /boot/kernel.img
cp /usr/share/%{name}-kernel/%{version}-%{release}/boot/*.dtb /boot/
cp /usr/share/%{name}-kernel/%{version}-%{release}/boot/overlays/*.dtb* /boot/overlays/
#/usr/sbin/dracut /boot/initramfs-%{version}-%{release}.img %{version}-%{release}

%postun kernel
cp $(ls -1 /boot/kernel-*-*|tail -1) /boot/kernel.img
cp $(ls -1d /usr/share/%{name}-kernel/*-*/|tail -1)/boot/*.dtb /boot/
cp $(ls -1d /usr/share/%{name}-kernel/*-*/|tail -1)/boot/overlays/*.dtb* /boot/overlays/


%files kernel-devel
%defattr(-,root,root)
/usr/src/kernels/%{version}-%{release}


#%files kernel-firmware
#%defattr(-,root,root)
#/lib/firmware/*


%files firmware
%defattr(-,root,root,-)
/boot/bootcode.bin
/boot/fixup*
/boot/start*
%doc /boot/LICENCE.broadcom

%changelog
* Thu May 24 2018 Jacco Ligthart <jacco@redsleeve.org> - 4.14.42-1.el7
- update to version 4.14.42
- stop makeing the kernel-firmware subpackage

* Wed Feb 28 2018 Jacco Ligthart <jacco@redsleeve.org> - 4.9.80-1.el7
- update to version 4.9.80, probably the last in the 4.9 series

* Sat Jan 27 2018 Jacco Ligthart <jacco@redsleeve.org> - 4.9.78-1.el7
- update to version 4.9.78

* Sun Dec 17 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.69-v7.1.el7
- update to version 4.9.69

* Mon Nov 27 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.65-v7.1.el7
- update to version 4.9.65

* Sun Oct 29 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.59-v7.1.el7
- update to version 4.9.59

* Mon Oct 02 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.52-v7.1.el7
- update to version 4.9.52

* Thu Aug 17 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.43-v7.1.el7
- update to version 4.9.43

* Sat Jul 22 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.39-v7.1.el7
- update to version 4.9.39

* Sat Jul 01 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.35-v7.1.el7
- update to version 4.9.35

* Mon Jun 19 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.33-v7.1.el7
- update to version 4.9.33

* Mon Jun 05 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.30-v7.1.el7
- update to version 4.9.30

* Fri May 12 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.27-v7.1.el7
- update to version 4.9.27

* Wed Apr 19 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.23-v7.1.el7
- update to version 4.9.23

* Thu Mar 30 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.19-v7.1.el7
- update to version 4.9.19

* Wed Mar 15 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.14-v7.1.el7
- update tp version 4.9.14

* Mon Mar 06 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.13-v7.2.el7
- updated to support the pi zero W

* Mon Feb 27 2017 Jacco Ligthart <jacco@redsleeve.org> - 4.9.13-v7.1.el7
- update to version 4.9.13

* Sat Dec 24 2016 Jacco Ligthart <jacco@redsleeve.org> - 4.4.39-v7.1.el7
- update to version 4.4.39

* Wed Nov 16 2016 Jacco Ligthart <jacco@redsleeve.org> - 4.4.32-v7.1.el7
- update to version 4.4.32

* Fri Oct 21 2016 Jacco Ligthart <jacco@redsleeve.org> - 4.4.26-v7.1.el7
- update to version 4.4.26 which includes a fix for CVE-2016-5195

* Tue Sep 27 2016 Jacco Ligthart <jacco@redsleeve.org> - 4.4.21-v7.3.el7
- changed versioning scheme, added EXTRAVERSION to makefile
- lost dificult linking in /lib/modules
- added all dirs under /usr/share/%{name}-kernel/ to the %files

* Sat Sep 24 2016 Jacco Ligthart <jacco@redsleeve.org> - 4.4.21-2
- removed dracut I don't see why we need a initramfs
- removed -b0 from %setup, the source was extracted twice

* Sat Sep 24 2016 Jacco Ligthart <jacco@redsleeve.org> - 4.4.21-1
- adjusted for raspberry pi model 1

* Sat Sep 24 2016 Jacco Ligthart <jacco@redsleeve.org> - 4.4.21-v7.1
- updated to 4.4.21
- moved the Requires: to the kernel subpackage
- added /boot/overlays to the %files

* Mon Jul 11 2016 Fabian Arrotin <arrfab@centos.org> - 4.4.14-2
- Fixed the dracut call for %{release}

* Thu Jul 7 2016 Fabian Arrotin <arrfab@centos.org>
- upgrade to kernel 4.4.14
- Moved some *dtb* files to /usr/share/raspberrypi2-kernel/boot/ 
- Using %post to put those in /boot/*
- generating initramfs in %post

* Fri Jun 17 2016 Johnny Hughes <johnny@centos.org>
- upgrade to kernel 4.4.13
- modified to copy *.dtb* to /boot/overlays/

* Sun Mar 13 2016 Fabian Arrotin <arrfab@centos.org>
- Added kmod/libselinux as BuildRequires (for the depmod part)
- Added audit support in the bcm2709_selinux_config.patch

* Fri Mar 11 2016 Henrik Andersson <henrik.4e@gmail.com>
- updated to 4.1.19
- build kernel from source instead of using binaries from firmware
- use only GPU firmware and bootloader from firmware

* Mon Jan 25 2016 Fabian Arrotin <arrfab@centos.org>
- updated to 4.1.16
- contains the patch fro CVE-2016-0728

* Thu Jan 21 2016 Fabian Arrotin <arrfab@centos.org>
- updated to 4.1.15

* Thu Nov 26 2015 Fabian Arrotin <arrfab@centos.org> 
- Added %{?dist} rpm macro in the name

* Sat Oct 24 2015 Jacco Ligthart <jacco@redsleeve.org>
- updated to 4.1.11

* Fri Sep 04 2015 Jacco Ligthart <jacco@redsleeve.org>
- updated to 4.1.6

* Fri Jun 26 2015 Jacco Ligthart <jacco@redsleeve.org>
- updated to 4.0.6

* Sun May 10 2015 Jacco Ligthart <jacco@redsleeve.org>
- updated to 3.18.13

* Sun Mar 29 2015 Jacco Ligthart <jacco@redsleeve.org>
- updated to 3.18.10
- fixed a bcm2708 vs. bcm2709 issue with include dirs

* Sat Mar 14 2015 Jacco Ligthart <jacco@redsleeve.org>
- updated to 3.18.9

* Fri Feb 20 2015 Jacco Ligthart <jacco@redsleeve.org>
- converted for raspberrypi model2 (kernel7 / version *-v7+ )

* Fri Feb 20 2015 Jacco Ligthart <jacco@redsleeve.org>
- update to version 3.18 (coming from 3.12)
- require coreutils
