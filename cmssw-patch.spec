### RPM cms cmssw-patch CMSSW_4_2_8_SLHCtk3_patch2
Requires: cmssw-patch-tool-conf 

%define runGlimpse      yes
%define useCmsTC        yes
%define saveDeps        yes

#Set it to -cmsX added by cmsBuild (if any) to the base release
%define baserel_postfix %{nil}

## IMPORT cmssw-patch-build
## IMPORT scram-project-build
