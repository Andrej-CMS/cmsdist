### RPM external p5-version 0.91
## INITENV +PATH PERL5LIB %i/lib/perl5
%define downloadn version
Source: http://search.cpan.org/CPAN/authors/id/J/JP/JPEACOCK/%{downloadn}-%{realversion}.tar.gz
Requires: p5-extutils-makemaker

%prep
%setup -n %downloadn-%{realversion}

%build
LC_ALL=C; export LC_ALL
perl Makefile.PL INSTALL_BASE=%i
make

%install
make install
rm -rf %i/man
