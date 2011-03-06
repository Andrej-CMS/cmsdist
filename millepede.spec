### RPM external millepede 03.00.00
# CAREFUL: NO VERSION IN TARBALL !!!
# Source: http://www.desy.de/~blobel/Mptwo.tgz
# Source: http://cmsrep.cern.ch/cmssw/millepede-mirror/millepede-2.0.tar.gz

%define svnTag %(echo %realversion | tr '.' '-')
Source: svn://svnsrv.desy.de/public/MillepedeII/tags/V%svnTag/?scheme=http&module=V%svnTag&output=/millepede.tgz

Requires: castor
%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

Patch: millepede_V02-00-01
Patch1: millepede_V02-00-01_64bit
Patch2: millepede_V02-00-01_gcc4
Patch3: millepede_V02-00-01_gcc45

%prep
%setup -n V%svnTag
%patch -p1

%if "%cpu" == "amd64"
%patch1 -p1
%endif

case %gccver in
  4.[01234].* )
%patch2 -p1
  ;;
  4.[56].*)
%patch3 -p1
  ;;
esac

perl -p -i -e "s!-lshift!-L$CASTOR_ROOT/lib -lshift -lcastorrfio!" Makefile
perl -p -i -e "s!C_INCLUDEDIRS =!C_INCLUDEDIRS = -I$CASTOR_ROOT/include!" Makefile

case %cmsplatf in osx*)
    perl -p -i -e "s|-lshift|-lcastorrfio|" Makefile ;;
esac

%build
# gcc on the mac cannot be used as a fortran compiler / linker because
# gfortran is installed somewhere else.
make %makeprocesses FCOMP=gfortran LOADER=gfortran

%install
make install
mkdir -p %i/bin
cp bin/* %i/bin
