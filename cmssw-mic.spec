### RPM cms cmssw-mic CMSSW_6_2_0_pre7
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%define ucprojtype CMSSW
Requires: cmssw-mic-tool-conf python

%define runGlimpse      yes
%define saveDeps        yes
%define source1         %{cvsrepo}&tag=-rCMSSW_6_2_0_pre7&module=Utilities/Timing&export=%{srctree}&output=/src.tar.gz
%define patchsrc4       perl -p -i -e 's!(<classpath.*/tests\\+.*>)!!;' config/BuildFile.xml; \
                        echo '<architecture name="_mic_"><flags DEFAULT_COMPILER="icc"/></architecture>' >> config/BuildFile.xml ; \
                        sed -i -e 's|</client>|<architecture name="_mic_"><flags DEFAULT_COMPILER="icc"/></architecture></client>|' config/Self.xml ;\
                        sed -i -e 's|^CMD_python := $(PYTHON_BASE)/bin/python|CMD_python := true|' config/SCRAM/GMake/Makefile.rules

## IMPORT scram-project-build
