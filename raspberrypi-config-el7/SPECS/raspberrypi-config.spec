Name:           raspberrypi-config
Version:        0.3
Release:        1%{?dist}
Summary:        specific configuration of Redsleeve Linux on the Raspberry Pi
BuildArch:      noarch

License:        GPL
URL:            n/a
Source0:        %{name}-%{version}.tar.gz

#BuildRequires:  
#Requires:       

%description
Specific configuration of Redsleeve Linux on the Raspberry Pi


%prep
%setup -q


#build
#configure
#/ make %{?_smp_mflags}


%install
#%make_install
cp -r boot etc %{buildroot}


%files
%defattr(-,root,root)
%config /boot/config.txt
%config /boot/cmdline.txt
%config /etc/sysconfig/network
%config /etc/sysconfig/network-scripts/ifcfg-eth0
%config /etc/fstab
%config /etc/modprobe.d/raspi-blacklist.conf
%config /etc/sysctl.d/raspi.conf


%changelog
* Tue Jan 27 2015 Jacco Ligthart <jacco@redsleeve.org> - 0.3
- updated for rsel7

* Sat Dec 20 2014 Jacco Ligthart <jacco@redsleeve.org> - 0.2
- added plymouth.modules to get rid of a harmless error message at system boot

* Mon Sep 26 2014 Jacco Ligthart <jacco@redsleeve.org> - 0.1
- initial version
