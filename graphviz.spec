### RPM external graphviz 2.16.1
Source: http://www.graphviz.org/pub/%{n}/ARCHIVE/%{n}-%{realversion}.tar.gz  
Requires: expat zlib libjpg libpng 

%prep
%setup -n %{n}-%{realversion}

%build
which gcc
LIB64_SUFFIX=
case %cmsplatf in
    *_ia32_* )
        export LD_LIBRARY_PATH=`echo $LD_LIBRARY_PATH | sed -e 's|lib64|lib|g'`
        ADDITIONAL_OPTIONS="--with-freetype2=no --disable-shared --enable-static --disable-libtdl"
    ;;
    *_amd64_* )
        LIB64_SUFFIX=64
        ADDITIONAL_OPTIONS="--with-freetype2=no --disable-shared --enable-static --disable-ltdl"
    ;;
    osx* )
        ADDITIONAL_OPTIONS="--with-freetype2=no"
    ;;
esac
./configure \
  --with-expatlibdir=$EXPAT_ROOT/lib$LIB64_SUFFIX \
  --with-expatincludedir=$EXPAT_ROOT/include \
  --with-zincludedir=$ZLIB_ROOT/include \
  --with-zlibdir=$ZLIB_ROOT/lib \
  --with-pngincludedir=$LIBPNG_ROOT/include \
  --with-pnglibdir=$LIBPNG_ROOT/lib \
  --with-jpegincludedir=$LIBJPG_ROOT/include \
  --with-jpeglibdir=$LIBJPG_ROOT/lib \
  --without-x \
  --without-tclsh \
  --without-tcl \
  --without-fontconfig \
  --without-tk \
  --without-perl \
  --without-python \
  --without-ruby \
  --disable-ruby \
  --disable-perl \
  --without-pangocairo \
  --without-fontconfig \
  --without-gdk-pixbuf \
  --disable-sharp \
  --disable-guile \
  --disable-java \
  --disable-lua \
  --disable-ocaml \
  --disable-perl \
  --disable-php \
  --disable-python \
  --prefix=%{i} \
  $ADDITIONAL_OPTIONS

# This is a workaround for the fact that sort from coreutils 5.96 doesn't 
# like "sort +0 -1", not really something specific to ppc64/ydl5.0
if [ "$(uname -m)" == "ppc64" ]
then
perl -p -i -e "s|\+0 \-1|-k1,1|g" dotneato/common/Makefile
fi
# Probably the configure should just be remade on Darwin, but it builds
# as-is with this small cleanup
perl -p -i -e "s|-lexpat||g" configure
# make %makeprocesses
make 

%install
make install
# To match configure options above
case %cmsplatf in
    *_ia32_* | *_amd64_*)
        ln -s dot_static %i/bin/dot
    ;;
esac

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <info url="http://www.research.att.com/sw/tools/graphviz/"/>
    <client>
      <environment name="GRAPHVIZ_BASE" default="%i"/>
      <environment name="GRAPHVIZ_BINDIR" default="$GRAPHVIZ_BASE/bin"/>
      <environment name="LIBDIR" default="$GRAPHVIZ_BASE/lib/graphviz"/>
    </client>
    <runtime name="PATH" value="$GRAPHVIZ_BINDIR" type="path"/>
    <use name="expat"/>
    <use name="zlib"/>
    <use name="libjpg"/>
    <use name="libpng"/>
  </tool>
EOF_TOOLFILE

%post
# It appears one needs to list at least one explicitly as the macro adds
# the prefix, but then the find can add it and the others (also with the 
# prefix)
%{relocateConfig}/lib/libgraph.la `find $RPM_INSTALL_PREFIX/%pkgrel/lib -name *.la`
%{relocateConfig}etc/scram.d/%n.xml
