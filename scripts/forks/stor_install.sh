#!/bin/env bash
#
# Installs Stor as per https://github.com/Stor-Network/stor-blockchain
#

STOR_BRANCH=$1
# On 2021-12-26
HASH=3c3cd1a3b99592e88160107ca5b81afc0937b992

if [ -z ${STOR_BRANCH} ]; then
    echo 'Skipping Stor install as not requested.'
else
    git clone --branch ${STOR_BRANCH} --recurse-submodules https://github.com/Stor-Network/stor-blockchain.git /stor-blockchain 
    cd /stor-blockchain
    git submodule update --init mozilla-ca
    git checkout $HASH
    chmod +x install.sh
    # 2022-01-30: pip broke due to https://github.com/pypa/pip/issues/10825
    sed -i 's/upgrade\ pip$/upgrade\ "pip<22.0"/' install.sh
    # 2022-07-20: Python needs 'packaging==21.3'
    sed -i 's/packaging==21.0/packaging==21.3/g' setup.py
    /usr/bin/sh ./install.sh

    if [ ! -d /chia-blockchain/venv ]; then
        cd /
        rmdir /chia-blockchain
        ln -s /stor-blockchain /chia-blockchain
        ln -s /stor-blockchain/venv/bin/stor /chia-blockchain/venv/bin/chia
    fi
fi
