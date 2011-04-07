### RPM cms das 0.6.3.pre11
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 
%define wmcver WMCORE_0_7_2
%define webdoc_files %i/doc/
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
Source0: %svnserver/WMCore/tags/%{wmcver}?scheme=svn+ssh&strategy=export&module=WMCore&output=/wmcore_das.tar.gz
Source1: %svnserver/DAS/tags/%{realversion}?scheme=svn+ssh&strategy=export&module=DAS&output=/das.tar.gz
Requires: python py2-simplejson py2-sqlalchemy py2-httplib2 cherrypy py2-cheetah yui
Requires: mongo py2-pymongo py2-cjson py2-yaml py2-pystemmer py2-mongoengine py2-lxml py2-ply py2-yajl
Requires: py2-sphinx rotatelogs

%prep
%setup -T -b 0 -n WMCore
%setup -D -T -b 1 -n DAS

# remove ipython deps
rm src/python/DAS/tools/ipy_profile_mongo.py

%build
cd ../WMCore
python setup.py build_system -s wmc-web
cd ../DAS
python setup.py build

# build DAS JSON maps out of DAS YML files
cmd="python src/python/DAS/tools/das_drop_maps.py"
dir="src/python/DAS/services/cms_maps/"
map_file="$dir/das_maps.js"
rm -f $map_file
export PYTHONPATH=$PYTHONPATH:$PWD/src/python
for amap in `ls $dir/*.yml`
do
    $cmd --uri-map=$amap >> $map_file
    $cmd --notation-map=$amap >> $map_file
    $cmd --presentation-map=$amap >> $map_file
done
rm -f $dir/*.yml
rm -rf src/python/DAS/services/maps

# build DAS sphinx documentation
PYTHONPATH=$PWD/src/python:$PYTHONPATH
cd doc
cat sphinx/conf.py | sed "s,development,%{realversion},g" > sphinx/conf.py.tmp
mv sphinx/conf.py.tmp sphinx/conf.py
mkdir -p build
make html

%install
cd ../WMCore
python setup.py install_system -s wmc-web --prefix=%i
cd ../DAS
#python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
python setup.py install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/doc
tar --exclude '.buildinfo' -C doc/build/html -cf - . | tar -C %i/doc -xvf -

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%i/
%exclude %i/doc

## SUBPACKAGE webdoc
