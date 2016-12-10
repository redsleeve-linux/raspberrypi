Name:           raspberrypi-rtc-ds3231
Version:        0.3
Release:        1%{?dist}
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
perl -p -i -e "s/^dtoverlay=i2c-rtc,ds3231//" /boot/config.txt
systemctl disable i2c-rtc

%post
echo "dtoverlay=i2c-rtc,ds3231" >> /boot/config.txt
systemctl enable i2c-rtc

%changelog
* Wed Sep 28 2016 Jacco Ligthart <jacco@redsleeve.org> - 0.3
- changed for the new kernel overlay things

* Tue Jan 27 2015 Jacco Ligthart <jacco@redsleeve.org> - 0.2
- modified for rsel7 method of module load on boot

* Mon Aug 18 2014 Jacco Ligthart <jacco@redsleeve.org> - 0.1
- initial version
