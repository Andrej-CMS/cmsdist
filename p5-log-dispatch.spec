### RPM external p5-log-dispatch 2.21
## INITENV +PATH PERL5LIB %i/lib/site_perl/%perlversion
# a comment to build from scratch increase this number 15
%define perlversion %(perl -e 'printf "%%vd", $^V')
%define perlarch %(perl -MConfig -e 'print $Config{archname}')
%define downloadn Log-Dispatch

Source: http://search.cpan.org/CPAN/authors/id/D/DR/DROLSKY/%{downloadn}-%{realversion}.tar.gz
Requires: p5-params-validate

# Provided by system perl
Provides:  perl(MIME::Lite)
Provides:  perl(Mail::Send)

# Fake provides for (hopefully) unneeded optional backends
Provides:  perl(Mail::Sender)
Provides:  perl(Mail::Sendmail)

%prep
%setup -n %downloadn-%realversion
%build
LC_ALL=C; export LC_ALL
perl Makefile.PL PREFIX=%i LIB=%i/lib/site_perl/%perlversion
make
#
