### RPM external p5-text-glob 0.06
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
# a comment to build from scratch increase this number 15
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn Text-Glob

Source: http://search.cpan.org/CPAN/authors/id/R/RC/RCLAMP/%{downloadn}-%{realversion}.tar.gz
%prep
%setup -n %downloadn-%realversion
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
