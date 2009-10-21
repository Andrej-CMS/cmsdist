### RPM external castor 2.1.7.14
# Override default realversion since they have a "-" in the realversion
%define realversion 2.1.7-14
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) true ;; esac
%define downloadv v%(echo %realversion | tr - _ | tr . _)
%define baseVersion %(echo %realversion | cut -d- -f1)
%define patchLevel %(echo %realversion | cut -d- -f2)
%define cpu %(echo %cmsplatf | cut -d_ -f2)
%if "%cpu" != "amd64"
%define libsuffix %nil
%else
%define libsuffix ()(64bit)
%endif

#Source: http://cern.ch/castor/DIST/CERN/savannah/CASTOR.pkg/%realversion/castor-%downloadv.tar.gz
#Source: cvs://:pserver:cvs@root.cern.ch:2401/user/cvs?passwd=Ah<Z&tag=-rv%(echo %realversion | tr . -)&module=root&output=/%{n}_v%{v}.source.tar.gz
Source: cvs://:pserver:anonymous@isscvs.cern.ch:/local/reps/castor?passwd=Ah<Z&tag=-r%{downloadv}&module=CASTOR2&output=/%{n}-%{realversion}.source.tar.gz
Patch0: castor-2.1.7.14-gcc43
Patch1: castor-2.1.7.14-gcc44

# Ugly kludge : forces libshift.x.y to be in the provides (rpm only puts libshift.so.x)
# root rpm require .x.y
Provides: libshift.so.%(echo %realversion |cut -d. -f1,2)%{libsuffix}

%prep
%setup -n CASTOR2 

%patch0 -p1
%patch1 -p1

%build

# make sure the version gets properly set up as otherwise it's "unknown" to the server
# to check: " %i/bin/castor -v " should give back the version
perl -pi -e "s/\ \ __MAJORVERSION__/%(echo %realversion | cut -d. -f1)/" h/patchlevel.h
perl -pi -e "s/\ \ __MINORVERSION__/%(echo %realversion | cut -d. -f2)/" h/patchlevel.h
perl -pi -e "s/\ \ __MAJORRELEASE__/%(echo %realversion | cut -d. -f3 | cut -d- -f 1 )/" h/patchlevel.h
perl -pi -e "s/\ \ __MINORRELEASE__/%(echo %realversion | cut -d- -f2)/" h/patchlevel.h

perl -p -i -e "s!__PATCHLEVEL__!%patchLevel!;s!__BASEVERSION__!\"%baseVersion\"!;s!__TIMESTAMP__!%(date +%%s)!" h/patchlevel.h

for this in BuildCupvDaemon BuildDlfDaemon BuildNameServerDaemon BuildRHCpp \
            BuildRtcpclientd BuildSchedPlugin BuildVolumeMgrDaemon UseOracle \
            UseScheduler BuildOraCpp BuildStageDaemon; do
    perl -pi -e "s/$this(?: |\t)+.*(YES|NO)/$this\tNO/g" config/site.def
done

for this in BuildSchedPlugin BuildJob BuildRmMaster; do
    perl -pi -e "s/$this(?: |\t)+.*(YES|NO)/$this\tNO/g" config/site.def
done

for this in BuildTapeDaemon; do
    perl -pi -e "s/$this(?: |\t)+.*(YES|NO)/$this\tNO/g" config/site.def
done

for this in BuildRfioClient BuildRfioLibrary BuildStageClient BuildStageLibrary; do
    perl -pi -e "s/$this(?: |\t)+.*(YES|NO)/$this\tYES/g" config/site.def
done

mkdir -p %i/bin %i/lib %i/man/man4 %i/man/man3 %i/man/man1 %i/etc/sysconfig

find . -type f -exec touch {} \;
make -f Makefile.ini Makefiles
which makedepend >& /dev/null
[ $? -eq 0 ] && make depend

make -j7 MAJOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f1-2) \
         MINOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f3-4 | tr '-' '.' )

%install
make install MAJOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f1-2) \
                MINOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f3-4 | tr '-' '.' ) \
                EXPORTLIB=/ \
                DESTDIR=%i/ \
                PREFIX= \
                CONFIGDIR=etc \
                FILMANDIR=man/man4 \
                LIBMANDIR=man/man3 \
                MANDIR=man/man1 \
                LIBDIR=lib \
                BINDIR=bin \
                LIB=lib \
                BIN=bin \
                DESTDIRCASTOR=include/shift \
                TOPINCLUDE=include 

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=shift>
<Client>
 <Environment name=CASTOR_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$CASTOR_BASE/include"></Environment>
 <Environment name=LIBDIR default="$CASTOR_BASE/lib"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
