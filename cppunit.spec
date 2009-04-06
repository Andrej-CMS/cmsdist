### RPM external cppunit 1.12.1
Source0: http://switch.dl.sourceforge.net/sourceforge/%n/%n-%realversion.tar.gz
Source1: http://spi.cvs.cern.ch:8180/cgi-bin/spi.cgi/*checkout*/Components/UnitTesting/Tools/CppUnit/CppUnit_testdriver.cpp?rev=1.1

%prep
%setup -n %n-%realversion

%build
case %cmsplatf in
    osx105* ) perl -p -i -e 's|rm(.*)conftest|rm -fr $1 conftest|g' configure \
                                                                    aclocal.m4 \
						                						    libtool \
						                						    config/ltmain.sh
    ;;
esac
case $(uname) in
    Linux )
       # Ugly hack to force -ldl to be linked, which for some reason is
       # not currently happening via configure
       perl -p -i -e 's|LIBS.*LIBS.*lm|LIBS="$LIBS -lm -ldl|' configure
    ;;
esac
./configure --prefix=%i 
make %makeprocesses
%install
make install
cp %_sourcedir/CppUnit_testdriver.cpp* %i/include/CppUnit_testdriver.cpp

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=cppunit>
<Client>
 <Environment name=CPPUNIT_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$CPPUNIT_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$CPPUNIT_BASE/include"></Environment>
</Client>
<use name=sockets>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}/bin/cppunit-config
%{relocateConfig}/lib/libcppunit.la
%{relocateConfig}etc/scram.d/%n
