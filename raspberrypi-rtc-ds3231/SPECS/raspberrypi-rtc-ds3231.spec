Name:           raspberrypi-rtc-ds3231
Version:        0.4
Release:        2%{?dist}
Summary:        Simple service to start the DS3231 RTC at boot on a Pi
BuildArch:      noarch

License:        GPL
URL:            n/a
Source0:        i2c-rtc.service
Source1:        55-i2c-rtc.rules

#BuildRequires:  
#Requires:       

%description
Simple service to start the DS3231 RTC at boot on a Pi

#%prep
#%setup -q


#build
#configure
#/ make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
#%make_install
mkdir -p %{buildroot}/usr/lib/systemd/system/
cp %{SOURCE0} %{buildroot}/usr/lib/systemd/system/
mkdir -p %{buildroot}/etc/udev/rules.d/
cp %{SOURCE1} %{buildroot}/etc/udev/rules.d/

%files
/usr/lib/systemd/system/i2c-rtc.service
/etc/udev/rules.d/55-i2c-rtc.rules
%doc

%preun
case "$1" in
  0)
    # This is an un-installation.
    perl -p -i -e "s/^dtoverlay=i2c-rtc,ds3231//" /boot/config.txt
    systemctl disable i2c-rtc
  ;;
  1)
    # This is an upgrade.
    # Do nothing.
    :
  ;;
esac

%post
case "$1" in
  1)
    # This is an initial install.
    echo "dtoverlay=i2c-rtc,ds3231" >> /boot/config.txt
    systemctl enable i2c-rtc
  ;;
  2)
    # This is an upgrade.
    # Do nothing.
    :
  ;;
esac

%changelog
* Mon Jun 05 2017 Jacco Ligthart <jacco@redsleeve.org> - 0.4.2
- change the preun/post scripts to detect upgrades

* Mon Jun 05 2017 Jacco Ligthart <jacco@redsleeve.org> - 0.4
- added ENV{SYSTEMD_WANTS} to the udev rules file

* Wed Sep 28 2016 Jacco Ligthart <jacco@redsleeve.org> - 0.3
- changed for the new kernel overlay things

* Tue Jan 27 2015 Jacco Ligthart <jacco@redsleeve.org> - 0.2
- modified for rsel7 method of module load on boot

* Mon Aug 18 2014 Jacco Ligthart <jacco@redsleeve.org> - 0.1
- initial version
