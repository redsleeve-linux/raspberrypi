Name:           raspberrypi-config
Version:        0.8
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
%config /etc/sysctl.d/raspi.conf
%config /etc/yum.repos.d/raspberry.repo

%pre
if [ $1 -gt 1 ] ; then
  if [ -f /etc/fstab ] ; then 
    cp -a /etc/fstab /etc/fstab-backup
  fi
  if [ -f /etc/sysconfig/network-scripts/ifcfg-eth0 ] ; then 
    cp -a /etc/sysconfig/network-scripts/ifcfg-eth0 /etc/sysconfig/network-scripts/ifcfg-eth0-backup
  fi
fi

%posttrans
if [ -f /etc/fstab-backup ] ; then
  mv /etc/fstab-backup /etc/fstab
fi
if [ -f /etc/sysconfig/network-scripts/ifcfg-eth0-backup ] ; then
  mv /etc/sysconfig/network-scripts/ifcfg-eth0-backup /etc/sysconfig/network-scripts/ifcfg-eth0
fi


%changelog
* Sun Oct 02 2016 Jacco Ligthart <jacco@redsleeve.org> - 0.8
- fixed keyname in repofile

* Sat Sep 24 2016 Jacco Ligthart <jacco@redsleeve.org> - 0.7
- added scripts to NOT delete ifcfg-eth0 and fstab on update

* Sat Sep 24 2016 Jacco Ligthart <jacco@redsleeve.org> - 0.6
- removed fstab and ifcfg-eth0, now part of rfb imgae build process
- adjusted repo file for new repo layout
- updated config.txt to upstream
- removed the rng module load and the blacklist, not necessary with the new kernel

* Tue May 19 2015 Jacco Ligthart <jacco@redsleeve.org> - 0.5
- added module load for bcm2708-rng to enable better randomness

* Sun May 10 2015 Jacco Ligthart <jacco@redsleeve.org> - 0.4
- added repo file

* Tue Jan 27 2015 Jacco Ligthart <jacco@redsleeve.org> - 0.3
- updated for rsel7

* Sat Dec 20 2014 Jacco Ligthart <jacco@redsleeve.org> - 0.2
- added plymouth.modules to get rid of a harmless error message at system boot

* Fri Sep 26 2014 Jacco Ligthart <jacco@redsleeve.org> - 0.1
- initial version
