#!/bin/sh

# Assuming this file is always run inside the docker container or a system that contains curl

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"


if [ "$1" == "" ]; then
    echo "Invalid Source Data Directory"
fi

echo "Downloading thredds data files...."

cd ~
touch .urs_cookies

mkdir -p $1/thredds/public
mkdir -p $1/thredds/public/gldas/raw/

chmod -R 0755 $1/thredds/public

cd $1/thredds/public/gldas/raw/


cat $DIR/urls.txt | tr -d '\r' | xargs -n 1 -P 4 curl -LJO -n -c ~/.urs_cookies -b ~/.urs_cookies

echo "......Download Done"

# Move NCML Files into thredds data directory

cp $DIR/tethysapp/gldas/ncml/* $1/thredds/public/gldas/