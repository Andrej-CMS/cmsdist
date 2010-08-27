### RPM external openldap 2.3.39
## INITENV +PATH LD_LIBRARY_PATH %i/lib
Source: ftp://ftp.openldap.org/pub/OpenLDAP/openldap-stable/openldap-stable-20071118.tgz
Patch0: openldap-2.3.39-gcc44
Requires: openssl db4 
#cyrus-sasl
Provides: libsasl2.so.2 libsasl2.so.2()(64bit)

%prep
%setup -q -n %n-%{realversion}
%patch0 -p1

%build

#  CC          C compiler command
#  CFLAGS      C compiler flags
#  LDFLAGS     linker flags, e.g. -L<lib dir> if you have libraries in a
#              nonstandard directory <lib dir>
#  CPPFLAGS    C/C++ preprocessor flags, e.g. -I<include dir> if you have
#              headers in a nonstandard directory <include dir>
#  CPP         C preprocessor

export CPPFLAGS="-I$OPENSSL_ROOT/include -I$DB4_ROOT/include -I$CYRUS_SASL_ROOT/include"
export LDFLAGS="-L$OPENSSL_ROOT/lib -L$DB4_ROOT/lib -L$CYRUS_SASL_ROOT/lib -L%{_builddir}/%n-%{realversion}/sasl2lib"
echo $CPPFLAGS

./configure --prefix=%i --with-cyrus-sasl --with-tls
make depend
make
%install
make install
