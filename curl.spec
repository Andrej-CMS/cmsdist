### RPM external curl 7.21.6
Source: http://curl.haxx.se/download/%n-%realversion.tar.gz
Provides: libcurl.so.3()(64bit) 
Requires: openssl
Requires: zlib
   
%prep
%setup -n %n-%{realversion}

%build
export OPENSSL_ROOT
export ZLIB_ROOT
./configure --prefix=%i --disable-static --without-libidn --disable-ldap --with-ssl=${OPENSSL_ROOT} --with-zlib=${ZLIB_ROOT}
# This should change link from "-lz" to "-lrt -lz", needed by gold linker
# This is a fairly ugly way to do it, however.
perl -p -i -e "s!\(LIBS\)!(LIBCURL_LIBS)!" src/Makefile
make %makeprocesses

%install
make install
case %cmsos in 
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

ln -s libcurl.$SONAME %i/lib/libcurl.$SONAME.3
# Trick to get our version of curl pick up our version of its associated shared
# library (which is different from the one coming from the system!).
case %cmsos in
  osx*)
install_name_tool -id %i/lib/libcurl-cms.dylib -change %i/lib/libcurl.4.dylib %i/lib/libcurl-cms.dylib  %i/lib/libcurl.4.dylib
install_name_tool -change %i/lib/libcurl.4.dylib %i/lib/libcurl-cms.dylib %i/bin/curl
ln -s libcurl.4.dylib %i/lib/libcurl-cms.dylib
  ;;
esac

# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
# which we neither need nor use at this time.
rm -rf %i/lib/pkgconfig

# Strip libraries, we are not going to debug them.
find %i/lib -type f -perm -a+x -exec strip {} \;

# Don't need archive libraries.
rm -f %i/lib/*.{l,}a

# Read documentation online.
rm -rf %i/share

%post
%{relocateConfig}bin/curl-config
