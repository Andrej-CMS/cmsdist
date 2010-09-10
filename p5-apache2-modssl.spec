### RPM external p5-apache2-modssl 0.07
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define downloadn Apache2-ModSSL
Source: http://search.cpan.org/CPAN/authors/id/O/OP/OPI/%downloadn-%realversion.tar.gz
Requires: mod_perl2

%prep
%setup -n %downloadn-%realversion

%build
export LC_ALL=C
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make PASTHRU_INC=-I$MOD_PERL2_ROOT/include
