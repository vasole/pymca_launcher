#! sudo docker run --rm -v ~/artifacts:/io -i -t centos:5 /bin/bash

export http_proxy="http://proxy.esrf.fr:3128"
export https_proxy="http://proxy.esrf.fr:3128"

cat > /etc/yum/yum.conf <<EOF
[main]
proxy=http://proxy.esrf.fr:3128
EOF

# dependencies needed by python, pip and git
yum install wget gcc gcc-c++ make zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel cpio expat-devel gettext-devel curl-devel

#############
# python 3.5
#############
wget --no-check-certificate https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
tar -xzf Python-3.5.2.tgz
cd Python-3.5.2
./configure --enable-shared 
make
make install

#############
# libpython
#############
echo "/usr/local/lib" > /etc/ld.so.conf.d/libpython3.5.conf
ldconfig

pip3 install --upgrade pip

#####################
# build dependencies
#####################
pip3 install cx_Freeze
pip3 install numpy
pip3 install --upgrade setuptools
# pip install --upgrade wheel?

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
./configure
make
make install

############
# pymca
############
# FIXME: change repo to vasole
cd /
git clone https://github.com/PiRK/pymca_launcher.git 
cd pymca_launcher
pip3 install .

python3 cx_setup.py build_exe
