### RPM external xdaq VR15487
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac

Requires: zlib mimetic xerces-c uuid sqlite
%define xdaqv %(echo %v | cut -f1 -d- | tr . _) 
%define libext so

Source: svn://svn.cern.ch/reps/cmsos/trunk/?scheme=svn+ssh&revision=15487&strategy=export&module=xdaq&output=/xdaq.gz

Patch: xdaq_build
Provides: /bin/awk

%prep
%setup -T -b 0 -n xdaq

%patch -p1
ls
echo " Install root in prep:" %{i}    %{pkginstroot}

%build
# Xdaq does not provide makeinstall,  it uses "simplify" script instead to 
# reorganize the directory structure after the build is done.
# Therefore build is done in the install area.

%install
# Copy all code into the installation area, and build directly there:
cp -rp *  %{i} # assuming there are no symlinks in the original source code
cd %{i}
export XDAQ_ROOT=$PWD
cd %{i}/daq
# Fix up a problem for the 64bit build
case %cmsplatf in
  *amd64* )
    perl -p -i -e "s!configure --prefix!configure --with-pic --prefix!" extern/asyncresolv/Makefile
    ;;
esac
export MIMETIC_PREFIX=$MIMETIC_ROOT
export XERCES_PREFIX=$XERCES_C_ROOT
export UUID_LIB_PREFIX=$UUID_ROOT/lib
export SQLITE_PREFIX=$SQLITE_ROOT
export SEARCH_PATH=$PATH

make CPPDEFINES=linux Set=extern_coretools install
make CPPDEFINES=linux Set=coretools install
make CPPDEFINES=linux Set=extern_powerpack install
make CPPDEFINES=linux Set=powerpack install
cd xdaq2rc
make CPPDEFINES=linux install

# The following structure used as defined in Xdaq "simplify" script:
cd %{i}
mv x86*/lib .
mv x86*/bin .
mv x86*/include .
# Make the following directory (it will be missing in the gcc4 case where
# things fail during the build and scram at least needs to see it)
mkdir -p include/linux

mkdir -p htdocs

for subdir in `echo "xdaq2rc"; grep -h -v \# config/mfSet.coretools config/mfSet.extern_coretools config/mfSet.extern_powerpack config/mfSet.powerpack | grep -v Packages= | grep '[a-z]' | awk '{print $1}'`
do
	mkdir -p %{i}/htdocs/$subdir/{images,xml,html}
	echo $subdir
	if [ -d daq/$subdir/xml ]; then
	        cd daq/$subdir/xml
                find . -name "*.*" -exec install -m 655 -D {} %{i}/htdocs/$subdir/xml/{} \;
		cd %{i}
        fi	
	if [ -d daq/$subdir/images ]; then
	        cd daq/$subdir/images
                find . -name "*.*" -exec install -m 655 -D {} %{i}/htdocs/$subdir/images/{} \;
		cd %{i}
        fi	
	if [ -d daq/$subdir/html ]; then
	        cd daq/$subdir/html
                find . -name "*.*" -exec install -m 655 -D {} %{i}/htdocs/$subdir/html/{} \;
		cd %{i}
        fi	
done

mkdir -p include/interface
mv daq/interface/evb/include/interface/evb include/interface
mv daq/interface/shared/include/interface/shared include/interface
mkdir -p etc
mv daq/xdaq/etc/default.profile etc/
rm -fr daq 
rm -fr CVS
rm -fr x86*
#rm -f %{i}/lib/lib*.a %{i}/lib/lib*.la

# Libraries from extern (not found cause they are symlinks)

#find daq -type f ! -path "*/extern/*lib*" -name "*.a" -exec cp {} %{i}/lib \;
perl -p -i -e "s|^#!.*make|#!/usr/bin/env make|" %{i}/daq/extern/slp/openslp-1.2.0/debian/rules

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=XDAQ version=%v>
<info url=http://home.cern.ch/xdaq></info>
<lib name=toolbox>
<lib name=xdaq>
<lib name=config>
<lib name=xoap>
<lib name=xgi>
<lib name=xdata>
<lib name=cgicc>
<lib name=log4cplus>
<lib name=xcept>
<lib name=logudpappender>
<lib name=peer>
<lib name=logxmlappender>
<lib name=asyncresolv>
<lib name=ptfifo>
<lib name=pthttp>
<lib name=pttcp>
<lib name=i2outils>
<lib name=xdaq2rc>
<lib name=xoapfilter>
<lib name=xalan-c>
<lib name=xalanMsg>
<lib name=wsaddressing>
<lib name=wsclientsubscriber>
<lib name=wseventing>
<lib name=wsserviceeventing>
<Client>
<Environment name=XDAQ_BASE  default="%i"></Environment>
<Environment name=LIBDIR default="$XDAQ_BASE/lib"></Environment>
<Environment name=BINDIR default="$XDAQ_BASE/bin"></Environment>
<Environment name=INCLUDE default="$XDAQ_BASE/include"></Environment>
<Environment name=INCLUDE default="$XDAQ_BASE/include/linux"></Environment>
</Client>
<use name=xerces-c>
<use name=sockets>
<use name=mimetic>
<use name=uuid>
<runtime name=XDAQ_OS value="linux">
<runtime name=XDAQ_PLATFORM value="x86">
<runtime name=PATH value="$BINDIR" type=path>
<runtime name=XDAQ_ROOT value="$XDAQ_BASE">
<runtime name=XDAQ_DOCUMENT_ROOT value="$XDAQ_BASE/htdocs">
<flags CPPDEFINES="SOAP__ LITTLE_ENDIAN__">
<flags CPPDEFINES="linux">
</Tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/xdaqheader
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=XDAQHEADER version=%v>
<info url=http://home.cern.ch/xdaq></info>
<Client>
<Environment name=XDAQHEADER_BASE  default="%i"></Environment>
<Environment name=INCLUDE default="$XDAQHEADER_BASE/include"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

%post
find $RPM_INSTALL_PREFIX/%pkgrel -type l | xargs ls -la | sed -e "s|.*[ ]\(/.*\) -> \(.*\)| \2 \1|;s|[ ]/[^ ]*/external| $RPM_INSTALL_PREFIX/%cmsplatf/external|g" | xargs -n2 ln -sf
%{relocateConfig}etc/scram.d/%n
%{relocateConfig}etc/scram.d/xdaqheader

