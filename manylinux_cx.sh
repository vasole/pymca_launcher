#! sudo docker run --rm -v ~/artifacts:/io -i -t centos:5 /bin/bash
# Script executed as root

export http_proxy="http://proxy.esrf.fr:3128"
export https_proxy="http://proxy.esrf.fr:3128"

cat > /etc/yum/yum.conf <<EOF
[main]
proxy=http://proxy.esrf.fr:3128
EOF

# dependencies needed by python, pip and git
yum install wget gcc gcc-c++ make zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel cpio expat-devel gettext-devel curl-devel
#ln -s /usr/bin/gcc44 /usr/bin/gcc
#ln -s /usr/bin/g++44 /usr/bin/g++
# openGL
yum install mesa-libGL mesa-libGL-devel mesa-libGLU mesa-libGLU-devel
# qt
#yum install fontconfig fontconfig-devel qt4 qt4-devel qt4-doc qt4-postgresql qt4-odbc qt4-sqlite qt-creator

alias wget="wget --no-check-certificate"

#############
# python 3.5
#############
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
tar -xzf Python-3.5.2.tgz
cd Python-3.5.2
./configure --enable-shared 
make
make install

echo "/usr/local/lib" > /etc/ld.so.conf.d/libpython3.5.conf
ldconfig

pip3 install --upgrade pip

#####################
# build dependencies
#####################
pip3 install cx_Freeze numpy
pip3 install --upgrade setuptools
# pip3 install --upgrade wheel

#####################
# GUI dependencies
#####################
pip3 install matplotlib sip

# sip
#cd /
#wget https://sourceforge.net/projects/pyqt/files/sip/sip-4.18.1/sip-4.18.1.tar.gz
#tar xzvf sip-4.18.1.tar.gz
#cd sip-4.18.1
#python3 configure.py; make ; make install

# pyqt4
#cd /
#wget http://downloads.sourceforge.net/project/pyqt/PyQt4/PyQt-4.11.4/PyQt-x11-gpl-4.11.4.tar.gz
#tar xzvf PyQt-x11-gpl-4.11.4.tar.gz 
#cd PyQt-x11-gpl-4.11.4
#python3 ./configure.py  --qmake=/usr/lib64/qt4/bin/qmake
#cd qpy
#make ; make install

pip3 install pyqt5

#############
# install git
#############
# (https://gist.github.com/eddarmitage/2001099)
# http://www.liquidweb.com/kb/install-git-on-centos-5/
# http://stackoverflow.com/questions/7880454/python-executable-not-finding-libpython-shared-library
cd /
wget https://www.kernel.org/pub/software/scm/git/git-2.9.3.tar.gz
tar xvzf git-2.9.3.tar.gz
cd git-2.9.3
./configure; make; make install

############
# pymca
############
export CFLAGS='-std=gnu99'
export SPECFILE_USE_GNU_SOURCE=1
# FIXME: change repo to vasole
cd /
git clone https://github.com/PiRK/pymca_launcher.git 
cd pymca_launcher

python3 setup.py install

pip3 install hdf5plugin
python3 cx_setup.py build_exe
