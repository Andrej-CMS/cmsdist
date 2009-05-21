### RPM external mcdb 1.0.2
Source: http://mcdb.cern.ch/distribution/api/%{n}-api-%{realversion}.tar.gz
Requires: xerces-c

%prep
%setup -q -n %{n}-api-%{realversion}

rm config.mk
touch config.mk
case %cmsplatf in
  osx105_ia32_gcc401  ) 
echo "PLATFORM = %cmsplatf" >> config.mk
echo "CC       = gcc" >> config.mk
echo "CXX      = g++" >> config.mk
echo "CFLAGS   = -O2 -pipe -Wall -W -fPIC" >> config.mk
echo "CXXFLAGS = -O2 -pipe -Wall -W -fPIC" >> config.mk
echo "LINK     = g++" >> config.mk
echo "LFLAGS   = -dynamiclib " >> config.mk
echo "XERCESC  = $XERCES_C_ROOT" >> config.mk
;;
  *ia32*  ) 
echo "PLATFORM = %cmsplatf" >> config.mk
echo "CC       = gcc" >> config.mk
echo "CXX      = g++" >> config.mk
echo "CFLAGS   = -O2 -pipe -Wall -W -march=i386 -mtune=i686 -fPIC" >> config.mk
echo "CXXFLAGS = -O2 -pipe -Wall -W -march=i386 -mtune=i686 -fPIC" >> config.mk
echo "LINK     = g++" >> config.mk
echo "LFLAGS   = -shared -Wl,-soname,libmcdb.so" >> config.mk
echo "XERCESC  = $XERCES_C_ROOT" >> config.mk
;;
  *amd64* ) 
echo "PLATFORM = %cmsplatf" >> config.mk
echo "CC       = gcc" >> config.mk
echo "CXX      = g++" >> config.mk
echo "CFLAGS   = -O2 -pipe -Wall -W -fPIC" >> config.mk
echo "CXXFLAGS = -O2 -pipe -Wall -W -fPIC" >> config.mk
echo "LINK     = g++" >> config.mk
echo "LFLAGS   = -shared -Wl,-soname,libmcdb.so" >> config.mk
echo "XERCESC  = $XERCES_C_ROOT" >> config.mk
;;
  *       )    # This default is bogus, needs specification for each non-linux
echo "PLATFORM = %cmsplatf" >> config.mk
echo "CC       = gcc" >> config.mk
echo "CXX      = g++" >> config.mk
echo "CFLAGS   = -O2 -pipe -Wall -W -march=i386 -mtune=i686 -fPIC" >> config.mk
echo "CXXFLAGS = -O2 -pipe -Wall -W -march=i386 -mtune=i686 -fPIC" >> config.mk
echo "LINK     = g++" >> config.mk
echo "LFLAGS   = -shared -Wl,-soname,libmcdb.so" >> config.mk
echo "XERCESC  = $XERCES_C_ROOT" >> config.mk
;;
esac




%build
make

%install
tar -c lib interface | tar -x -C %i
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=mcdb version=%v>
<Client>
 <Environment name=MCDB_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$MCDB_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$MCDB_BASE/interface"></Environment>
</Client>
<lib name=mcdb>
<use name=xerces-c>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
