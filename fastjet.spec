### RPM external fastjet 2.4.0
Source: http://www.lpthe.jussieu.fr/~salam/fastjet/repo/%n-%realversion.tar.gz
Patch1: fastjet-2.1.0-nobanner
Patch2: fastjet-2.3.4-siscone-banner
Patch3: fastjet-2.4.0-gcc44

%prep
%setup -n %n-%realversion
%patch1 -p1
%patch2 -p1
%patch3 -p1

./configure --enable-shared --enable-cmsiterativecone --enable-atlascone --prefix=%i

%build
make

%install
make install


# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=FastJet version=%v>
<info url=http://www.lpthe.jussieu.fr/~salam/fastjet/></info>
<lib name=CMSIterativeConePlugin>
<lib name=SISConePlugin>
<lib name=CDFConesPlugin>
<lib name=ATLASConePlugin>
<lib name=siscone>
<lib name=siscone_spherical>
<lib name=fastjet>
<client>
 <Environment name=FASTJET_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$FASTJET_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$FASTJET_BASE/include"></Environment>
</client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
