### RPM cms fwlite CMSSW_3_3_2_FWLITE
## IMPORT configurations 
Provides: /bin/zsh
Provides: /bin/sed
Provides: perl(Date::Format)
Provides: perl(Term::ReadKey)
Provides: perl(full)
Provides: perl(Template)
Requires: fwlite-tool-conf python

%define cmssw_release   %(perl -e '$_="%v"; s/_FWLITE//; print;')
%define cvsprojuc       %(echo %n | sed -e "s|-debug||"| tr 'a-z' 'A-Z')
%define cvsprojlc       %(echo %cvsprojuc | tr 'A-Z' 'a-z')
%define cvsdir          %cvsprojuc
%define cvsserver       %cvsprojlc
%define useCmsTC        1
%define saveDeps        yes

#Defines for file containing list of packages for checkout and build:
%define buildsetfile    fwlite_build_set

# Skip library load and symbol checks to avoid dependency on seal:
%define nolibchecks     on

# Switch off building tests and plugins:
%define patchsrc3 perl -p -i -e ' s|(<classpath.*test\\+test.*>)||;' config/BuildFile.xml*
%define patchsrc4 perl -p -i -e ' s|(<classpath.*plugins\\+plugins.*>)||;' config/BuildFile.xml*


## IMPORT cms-scram-build
## IMPORT partial-build
## IMPORT scramv1-build
