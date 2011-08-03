### RPM cms filemover 1.0.9.pre3
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
%define wmcver 0.7.4
%define webdoc_files %i/doc/
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
Source0: %svnserver/WMCore/tags/%{wmcver}?scheme=svn+ssh&strategy=export&module=WMCore&output=/wmcore_fm.tar.gz
Source1: %svnserver/FileMover/tags/%{realversion}?scheme=svn+ssh&strategy=export&module=FileMover&output=/filemover.tar.gz
Requires: python py2-simplejson py2-sqlalchemy py2-httplib2 cherrypy py2-cheetah yui
Requires: py2-sphinx rotatelogs java-jdk srmcp

%prep
%setup -T -b 0 -n WMCore
%setup -D -T -b 1 -n FileMover

%build
cd ../WMCore
python setup.py build_system -s wmc-web
cd ../FileMover
python setup.py build

# build FileMover sphinx documentation
PYTHONPATH=$PWD/src/python:$PYTHONPATH
cd doc
cat sphinx/conf.py | sed "s,development,%{realversion},g" > sphinx/conf.py.tmp
mv sphinx/conf.py.tmp sphinx/conf.py
mkdir -p build
make html

%install
cd ../WMCore
python setup.py install_system -s wmc-web --prefix=%i
cd ../FileMover
python setup.py install --prefix=%i
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
