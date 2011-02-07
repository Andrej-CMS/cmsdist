### RPM external openldap 2.3.39
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) true ;; esac
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

mkdir -p sasl2lib
ln -s /usr/lib/libsasl2.so.2.0.19 sasl2lib/libsasl2.so

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

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<Client>
 <Environment name=OPENLDAP_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$OPENLDAP_BASE/lib"></Environment>
</Client>
<use name=openssl>
<use name=db4>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n

