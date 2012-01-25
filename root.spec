### RPM lcg root 5.30.02
## INITENV +PATH PYTHONPATH %i/lib/python
## INITENV SET ROOTSYS %i  
#Source: ftp://root.cern.ch/%n/%{n}_v%{realversion}.source.tar.gz
%define svntag %(echo %realversion | tr . -)
Source: svn://root.cern.ch/svn/root/tags/v%{svntag}/?scheme=http&strategy=export&module=%n-%{realversion}&output=/%n-%{realversion}.tgz
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)
%define ismac %(case %cmsplatf in (osx*) echo true;; (*) echo false;; esac)

Patch0: root-5.28-00d-externals
Patch1: root-5.28-00d-CINT-maxlongline-maxtypedef
Patch2: root-5.28-00d-roofit-silence-static-printout
Patch3: root-5.28-00d-linker-gnu-hash-style
#Patch4: root-5.28-00d-TBranchElement-dropped-data-member
#Patch5: root-5.30-00-TSchemaRuleProcessor-nested-space
#Patch5: root-5.28-00d-r37582-tmva
#Patch6: root-5.28-00d-TTreeCache-r37919
#Patch7: root-5.28-00d-r38248-r38259-r38264-r38265-r38267
#Patch8: root-5.28-00d-fireworks1
#Patch9: root-5.28-00d-r39155
#Patch10: root-5.28-00d-r39525
#Patch11: root-5.28-00d-r39657
#Patch12: root-5.28-00d-r39759
#Patch13: root-5.28-00d-fix-tsystem-load-macosx
Patch14: root-5.30.02-detect-arch
#Patch15: root-5.30.02-fix-isnan
Patch16: root-5.30.02-fix-gcc46
Patch17: root-5.30.02-r41453
Patch18: root-5.30.02-r41523
Patch19: root-5.30.02-fix-isnan-again
Patch20: root-5.30.02-r41402
 
%define cpu %(echo %cmsplatf | cut -d_ -f2)

Requires: gccxml gsl libjpg libpng libtiff libungif libxml2 pcre python fftw3 xz xrootd

%if "%ismac" != "true"
Requires: castor dcap
%endif

%if "%online" != "true"
Requires: openssl zlib
%endif

%define keep_archives true
%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%if "%(case %cmsplatf in (osx*) echo true ;; (*) echo false ;; esac)" == "true"
Requires: freetype
%endif

%prep
%setup -n root-%realversion
%patch0 -p1
%patch1 -p1
%patch2 -p1
# patch3 is OS version dependent, see below
# patch4 -p1
# patch5 -p2
# patch5 -p1
# patch6 -p1
# patch7 -p1
# patch8 -p1
# patch9 -p1
# patch10 -p1 TRY AGAIN!
# patch11 -p0
# patch12 -p2
# patch13 -p1
%patch14 -p0
# patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p2
%patch19 -p1
%patch20 -p2

# The following patch can only be applied on SLC5 or later (extra linker
# options only available with the SLC5 binutils)
case %cmsplatf in
  slc[56]_* | slc5onl_* )
%patch3 -p1
  ;;
esac

# Delete these (irrelevant) files as the fits appear to confuse rpm on OSX
# (It tries to run install_name_tool on them.)
rm -fR tutorials/fitsio

%build

mkdir -p %i
export LIBJPG_ROOT
export ROOTSYS=%_builddir/root
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

%if "%online" == "true"
# Also skip xrootd and odbc for online case:

EXTRA_CONFIG_ARGS="--with-f77=/usr
             --disable-odbc --disable-astiff"
%else
export LIBPNG_ROOT ZLIB_ROOT LIBTIFF_ROOT LIBUNGIF_ROOT
EXTRA_CONFIG_ARGS="--with-f77=${GCC_ROOT}
             --with-ssl-incdir=${OPENSSL_ROOT}/include
             --with-ssl-libdir=${OPENSSL_ROOT}/lib"
%endif
LZMA=${XZ_ROOT}
export LZMA
CONFIG_ARGS="--enable-table 
             --disable-builtin-pcre
             --disable-builtin-freetype
             --disable-builtin-zlib
             --with-gccxml=${GCCXML_ROOT} 
             --enable-python --with-python-libdir=${PYTHON_ROOT}/lib --with-python-incdir=${PYTHON_ROOT}/include/python${PYTHONV}
             --enable-explicitlink 
             --enable-mathmore
             --enable-reflex  
             --enable-cintex 
             --enable-minuit2
             --disable-builtin-lzma
             --enable-fftw3
             --with-fftw3-incdir=${FFTW3_ROOT}/include
             --with-fftw3-libdir=${FFTW3_ROOT}/lib
             --disable-ldap
             --disable-krb5
             --with-xrootd=${XROOTD_ROOT}
             --with-gsl-incdir=${GSL_ROOT}/include
             --with-gsl-libdir=${GSL_ROOT}/lib
             --with-dcap-libdir=${DCAP_ROOT}/lib 
             --with-dcap-incdir=${DCAP_ROOT}/include
             --disable-pgsql
             --disable-mysql
             --disable-qt --disable-qtgsi
             --disable-oracle ${EXTRA_CONFIG_ARGS}"

case %cmsos in
  slc*)
    ./configure linuxx8664gcc $CONFIG_ARGS --with-rfio-libdir=${CASTOR_ROOT}/lib --with-rfio-incdir=${CASTOR_ROOT}/include/shift --with-castor-libdir=${CASTOR_ROOT}/lib --with-castor-incdir=${CASTOR_ROOT}/include/shift ;; 
  osx*)
    comparch=x86_64
    macconfig=macosx64
    ./configure $arch $CONFIG_ARGS --disable-rfio --disable-builtin_afterimage ;;
  slc*_ppc64*)
    ./configure linux $CONFIG_ARGS --disable-rfio;;
esac

makeopts="%makeprocesses"

make $makeopts

%install
# Override installers if we are using GNU fileutils cp.  On OS X
# ROOT's INSTALL is defined to "cp -pPR", which only works with
# the system cp (/bin/cp).  If you have fileutils on fink, you
# lose.  Check which one is getting picked up and select syntax
# accordingly.  (FIXME: do we need to check that -P is accepted?)
if (cp --help | grep -e '-P.*--parents') >/dev/null 2>&1; then
  cp="cp -dpR"
else
  cp="cp -pPR"
fi

export ROOTSYS=%i
make INSTALL="$cp" INSTALLDATA="$cp" install
mkdir -p $ROOTSYS/lib/python
cp -r cint/reflex/python/genreflex $ROOTSYS/lib/python
# This file confuses rpm's find-requires because it starts with
# a """ and it thinks is the shebang.
rm -f %i/tutorials/pyroot/mrt.py


