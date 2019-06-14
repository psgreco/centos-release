#!/bin/bash
########################################################################
# Anaconda uses a custom yum root, so we need to link our custom
# vars into there
########################################################################
SELFCOPIES=${1:-0}
TRIGGERCOPIES=${2:-0}
########################################################################
echo '[Unit]' > /usr/lib/systemd/system/anaconda-repos.service
echo 'ConditionPathExists=/etc/anaconda.repos.d' >> /usr/lib/systemd/system/anaconda-repos.service
echo 'Description=Setup CentOS Anaconda repos' >> /usr/lib/systemd/system/anaconda-repos.service
echo '[Install]' >> /usr/lib/systemd/system/anaconda-repos.service
echo 'WantedBy=anaconda.target' >> /usr/lib/systemd/system/anaconda-repos.service
echo '[Service]' >> /usr/lib/systemd/system/anaconda-repos.service
echo 'ExecStart=/usr/libexec/centos-release/anaconda-repos.sh' >> /usr/lib/systemd/system/anaconda-repos.service

########################################################################
systemctl enable anaconda-repos.service
########################################################################

