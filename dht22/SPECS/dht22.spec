# Actually the date is the packaging date not the commit date
%global commit_date  20150912
%global commit_short b712ad2
%global commit_long  b712ad2d769a9d8bbeed79169b34a277306061cd

Name:		dht22
Version:	0.1
Release:	1.%{commit_date}git%{commit_short}
Summary:	Driver for DHT22/AM2302 Temperature and humidity sensors on Raspberry Pi.

License:	Public domain. Do what you want. No warranties.
URL:		https://github.com/technion/lol_dht22
Source0:	https://github.com/technion/lol_dht22/tarball/%{commit_long} 

Patch0:		dht22_build.patch
Patch1:		dht22_jacco.patch

BuildRequires:	wiringpi, automake, autoconf
Requires:	wiringpi

%description
Driver for DHT22/AM2302 Temperature and humidity sensors on 
Raspberry Pi.

%prep
%setup -q -n technion-lol_dht22-%{commit_short}
%patch0 -p1
%patch1 -p1

%build
./missing --run aclocal
./missing --run automake
autoconf
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*


%changelog
* Sun Sep 13 2015 Jacco Ligthart <jacco@redsleeve.org> 0.1-1.20150912gitb712ad2
- initial release
