#!/bin/env bash
#
# Used to swap to my dev copy of Plotman for editing
#

echo 'Swapping to development Plotman...'
cd /chia-blockchain/venv/lib/python3.10/site-packages
if [ -d ./plotman ]; then
    mv ./plotman ./plotman.orig
fi
ln -s /code/plotman/src/plotman
