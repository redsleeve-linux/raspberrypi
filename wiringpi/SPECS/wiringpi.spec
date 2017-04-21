# Actually the date is the packaging date not the commit date
%global commit_date  20170421
%global commit_short 96344ff
%global commit_long  96344ff7125182989f98d3be8d111952a8f74e15

Name:           wiringpi
Version:        2.44
Release:        0.%{commit_date}git%{commit_short}.redsleeve
Summary:        WiringPi is a Wiring library written in C and should be usable from C++.

License:        GPLv3
URL:            https://git.drogon.net/?p=wiringPi
#Source0:       https://git.drogon.net/?p=wiringPi;a=snapshot;h=%{commit_short};sf=tgz 
Source0:        wiringPi-%{commit_short}.tar.gz
#Patch0:         wiringpi_make_fix.patch
#ExclusiveArch:  armv5tel

%description
WiringPi is a Wiring library written in C and should be usable from C++.

%prep
%setup -qn wiringPi-%{commit_short}
sed -i 's/^PREFIX=\/local/PREFIX=/' wiringPi/Makefile
sed -i 's/^PREFIX=\/local/PREFIX=/' devLib/Makefile
sed -i 's/^INCLUDE\t=\ -I./INCLUDE\t=\ -I.\ -I..\/wiringPi/' devLib/Makefile
sed -i 's/^PREFIX=\/local/PREFIX=/' gpio/Makefile
sed -i 's/^INCLUDE\t=\ -I.*/INCLUDE\t=\ -I.\ -I..\/wiringPi\ -I..\/devLib/' gpio/Makefile
sed -i 's/^LDFLAGS\t=\ -L.*/LDFLAGS\t=\ -L.\ -L..\/wiringPi\ -L..\/devLib/' gpio/Makefile
#%patch0 -p0

%build
#./build
cd wiringPi
make
ldconfig -n .
cd ../devLib
make
ldconfig -n .
cd ../gpio
make
cd ..

%install
rm -rf %{buildroot}

echo "[Install]"
install -m 0755 -d %{buildroot}%{_libdir}
install -m 0755 -d %{buildroot}%{_includedir}
install -m 0644 devLib/*.h %{buildroot}%{_includedir}
install -m 0755 devLib/libwiringPiDev.so.2.* %{buildroot}%{_libdir}
install -m 0644 wiringPi/*.h %{buildroot}%{_includedir}
install -m 0755 wiringPi/libwiringPi.so.2.* %{buildroot}%{_libdir}
echo "[GPIO Install]"
install -m 0755 -d %{buildroot}%{_bindir}
install -m 4755 gpio/gpio %{buildroot}%{_bindir}
install -m 0755 -d  %{buildroot}/usr/man/man1/
install -m 0644 gpio/gpio.1  %{buildroot}/usr/man/man1/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%_oldincludedir
%{_libdir}/lib*

%doc /usr/man/man1/*
%doc examples pins/pins.pdf

%changelog
* Fri Apr 21 2017 Jacco Ligthart <jacco@redsleeve.org> - 2.44-0
- updated to version 2.44 to support Pi Zero-W

* Mon Feb 27 2017 Jacco Ligthart <jacco@redsleeve.org> - 2.40-0
- updated to version 2.4 to support kernels 4.8+

* Sun Jun 07 2015 Jacco Ligthart <jacco@redsleeve.org> - 2.25-0
- Build for 2.25

* Wed Mar 18 2014 George Machitidze <giomac@gmail.com> - 2.3-0
- Build for 2.3

* Mon May 13 2013 Chris Tyler <chris@tylers.info> - 1-3.20130207git98bcd20.rpfr18
- Added scriptlets

* Fri Nov 16 2012 Andrew Greene <andrew.greene@senecacollege.ca> - 1-1
- Updated packaged version and release tags for rpfr18

* Wed Sep 17 2012 Andrew Greene <andrew.greene@senecacollege.ca> - 1.0-4
- Package updated to include new files gerthboard.h, piNes.h and wiringSerial.h

* Thu Jul 12 2012 Andrew Greene <andrew.greene@senecacollege.ca> - 1.0-3
- changed the rpm name of from raspberrypi-wiringpi to wiringpi

* Thu Jul 12 2012 Andrew Greene <andrew.greene@senecacollege.ca> - 1.0-2
- fixed the missing file lcd.h with the correct path for the examples make

* Wed Jul 11 2012 Andrew Greene <agreene@learn.senecac.on.ca> - 1.0-1
- basic install instructions copied some files to /usr/bin and /usr/lib
- added a quick hack to fix the examples make error lcd.h file not in the right location
