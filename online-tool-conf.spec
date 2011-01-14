### RPM cms online-tool-conf 6.0
# with cmsBuild, change the above version only when a new
# tool is added
## INITENV SET CMSSW_TOOL_CONF_ROOT $ONLINE_TOOL_CONF_ROOT
Provides: tmp/slc3_ia32_gcc323/src/FWCore/TFWLiteSelector/test/libFWCoreTFWLiteSelectorTest.so
Provides: libboost_regex-gcc-mt.so 
Provides: libboost_signals-gcc-mt.so 
Provides: libboost_thread-gcc-mt.so

Requires: coral
Requires: gmake
Requires: gdb
Requires: pcre
Requires: bz2lib
Requires: uuid
Requires: python
Requires: expat
Requires: gccxml
Requires: boost
Requires: gsl-toolfile
Requires: clhep-toolfile
Requires: root
Requires: roofit
Requires: castor
Requires: libjpg
Requires: dcap
Requires: oracle-env
Requires: p5-dbd-oracle
Requires: frontier_client
Requires: sqlite
Requires: hepmc
Requires: heppdt
Requires: elementtree
Requires: sigcpp
Requires: valgrind
Requires: fastjet-toolfile
Requires: ktjet
Requires: cmsswdata
Requires: onlinesystemtools
Requires: igprof-toolfile
Requires: classlib-toolfile

%define skipreqtools jcompiler
%define onlinesystemtoolsroot ${ONLINESYSTEMTOOLS_ROOT}
## IMPORT scramv1-tool-conf
