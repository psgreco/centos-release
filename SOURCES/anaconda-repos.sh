#!/bin/bash
########################################################################
# anaconda expects some specific reponames, so we are going to make them
########################################################################
sed -e 's/\[base\]/[centos]/' /etc/yum.repos.d/CentOS-Base.repo > /etc/anaconda.repos.d/centos.repo

########################################################################
# anaconda uses a custom yum root, so setup the relevant yumvars
########################################################################
mkdir -p /tmp/yum.root/etc/yum/vars
cp /etc/yum/vars/* /tmp/yum.root/etc/yum/vars/

