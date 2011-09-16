### RPM external p5-compress-zlib 1.34
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn Compress-Zlib
Source: http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/%{downloadn}-%{realversion}.tar.gz
Requires: zlib p5-extutils-makemaker

%prep
%setup -n %downloadn-%realversion

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i INCLUDE=$ZLIB_ROOT/include
make

%install
make install
rm -rf %i/man
