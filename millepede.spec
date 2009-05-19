### RPM external millepede 2.0
## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) false ;; esac 

# CAREFUL: NO VERSION IN TARBALL !!!
# Source: http://www.desy.de/~blobel/Mptwo.tgz
Source: http://cmsrep.cern.ch/cmssw/millepede-mirror/millepede-2.0.tar.gz

Patch: millepede_2009_01_22
Patch1: millepede_64bit_2008_08_18
Patch2: millepede-gcc412

%prep
%setup -n millepede-%realversion
%patch -p1

%if "%cpu" == "amd64"
%patch1 -p1
%endif

case %gccver in
  4.*)
%patch2 -p0
  ;;
esac

%build
make %makeprocesses

%install
make install
mkdir -p %i/bin
cp bin/* %i/bin

# Toolfile with only PATH
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
# millepede tool file
cat << \EOF_TOOLFILE >%i/etc/scram.d/millepede
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=millepede version=%v>
<info url="http://www.desy.de/~blobel"></info>
<Client>
 <Environment name=MILLEPEDE_BASE default="%i"></Environment>
</Client>
<use name=sockets>
<use name=pcre>
<use name=zlib>
<Runtime name=PATH value="$MILLEPEDE_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n


