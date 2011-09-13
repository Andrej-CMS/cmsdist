### RPM external zlib 1.2.3
Source: http://www.gzip.org/%n/%n-%realversion.tar.bz2

%prep
%setup -n %n-%realversion

%build
%if "%cmscompiler" == "icc"
%define cfgopts CC="icc -fPIC"
%else
%define cfgopts %nil
%endif

case %cmsplatf in
   *_gcc4[56789]* )
     CFLAGS="-fPIC -O3 -DUSE_MMAP -DUNALIGNED_OK -D_LARGEFILE64_SOURCE=1 -msse3" \
     ./configure --shared --prefix=%i
     ;;

   * )
     %cfgopts ./configure --shared --prefix=%i
     ;;
esac

make %makeprocesses

%install
make install
