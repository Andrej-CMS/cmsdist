### RPM external p5-crypt-blowfish 2.12
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perl /usr/bin/env perl
%if "%(echo %cmsplatf | cut -f1 -d_ | sed -e 's|\([A-Za-z]*\)[0-9]*|\1|')" == "osx"
%define perl /usr/bin/perl
%endif

%define perlversion %(%perl -e 'printf "%%vd", $^V')
%define perlarch %(%perl -MConfig -e 'print $Config{archname}')
%define downloadn Crypt-Blowfish

Source:  http://search.cpan.org/CPAN/authors/id/D/DP/DPARIS/%{downloadn}-%{realversion}.tar.gz

%prep
%setup -n %downloadn-%realversion
%build
LC_ALL=C; export LC_ALL
%perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
make install

%install
