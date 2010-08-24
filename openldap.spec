### RPM external openldap 2.3.39
## INITENV +PATH LD_LIBRARY_PATH %i/lib
Source: ftp://ftp.openldap.org/pub/OpenLDAP/openldap-stable/openldap-stable-20071118.tgz
Patch0: openldap-2.3.39-gcc44
Requires: openssl db4 
#cyrus-sasl
Provides: libsasl2.so.2 libsasl2.so.2()(64bit)

#http://www.openssl.org/source/%n-%realversion.tar.gz

%prep
%setup -q -n %n-%{realversion}
pwd
%patch0 -p1

%build

pwd

# Fix missing sasl2 library link on 64-bit SLC4: 
case %cmsplatf in
   slc*)
	mkdir -p sasl2lib
	ln -s /usr/lib/libsasl2.so.2.0.19 sasl2lib/libsasl2.so
   ;;
esac

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
which cc
which gcc

./configure --prefix=%i --with-cyrus-sasl --with-tls
make depend
make
%install
make install
