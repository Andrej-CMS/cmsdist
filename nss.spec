### RPM external nss 3.12.6 
Source: https://ftp.mozilla.org/pub/mozilla.org/security/nss/releases/NSS_%(echo %realversion | tr . _)_RTM/src/nss-%realversion.tar.gz
Requires: nspr zlib

%build
export NSPR_INCLUDE_DIR=$NSPR_ROOT/include/nspr 
export NSPR_LIB_DIR=$NSPR_ROOT/lib
export USE_SYSTEM_ZLIB=1
export ZLIB_LIBS="-L$ZLIB_ROOT -lz"

case %cmsplatf in
  *_amd64_*)
    export USE_64=1
  ;;
esac

make -C ./mozilla/security/coreconf
make -C ./mozilla/security/dbm
case %cmsplatf in
osx*)
  make -C ./mozilla/security/nss CC="gcc -framework Foundation -framework Carbon"
;;
*)
  make -C ./mozilla/security/nss
;;
esac

%install
case %cmsplatf in
  osx*)
    soname=dylib;;
  *)
    soname=so;;
esac

install -d %i/include/nss3
install -d %i/lib
find mozilla/dist/public/nss -name '*.h' -exec install -m 644 {} %i/include/nss3 \;
find . -path "*/mozilla/dist/*.OBJ/lib/*.$soname" -exec install -m 755 {} %i/lib \;
