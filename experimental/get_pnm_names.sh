#!/bin/ksh
#
# pnm macro assistance tool.
#
# Usage:
#  get_pnm_names specfile
# 

PKG_CLIENT_TIMEOUT=120;export PKG_CLIENT_TIMEOUT
VERSION=`uname -v | sed 's/[^0-9]//g'`

# Get IPS Package name from SVR4NAME
# Usage:
#  IPS_PACKAGE_NAME=`get_ips_name $SVR4_PACKAGE_NAME`
function get_ips_name {
    svr4pkgname=$1
    pkg search -r $svr4pkgname 2> /dev/null | awk '/^legacy_pkg.*'${VERSION}'$/{print $4}' | sort | tail -1
}

function get_ips_name_list {
    typeset SVRPKGS=$*

    typeset TEMP=`mktemp /tmp/get_ips_name_list.XXXXXX`
    rm -f ${TEMP}
    touch ${TEMP}

    for pkgname in $SVRPKGS;do
	if echo $pkgname | egrep -e 'pnm_(build)?requires_' > /dev/null 2>&1; then
	    echo "$pkgname is already changes">/dev/stderr
	else
	    echo searching ${pkgname}' ... \c' > /dev/stderr
	    IPSNAME=`get_ips_name ${pkgname}`
	    echo ${IPSNAME} >/dev/stderr
	    echo ${pkgname} ${IPSNAME}>> ${TEMP}
	fi
    done
    cat ${TEMP}
    rm -f ${TEMP}
}

SPECFILE=$1

if [ -z ${SPECFILE} ];then
    echo "get_pnm_names.sh specfile" > /dev/stderr
    exit 1
fi

if [ ! -r ${SPECFILE} ];then
    echo "File not found: ${SPECFILE}" > /dev/stderr
    exit 1
fi

REQUIRES=`awk -F: '/^Require/{print $2}' ${SPECFILE} | xargs `
BUILD_REQUIRES=`awk -F: '/^BuildRequire/{print $2}' ${SPECFILE} | xargs `

REQ_TEMP=`mktemp /tmp/make_pnm_macros_require.XXXXXX`
BREQ_TEMP=`mktemp /tmp/make_pnm_macros_build_require.XXXXXX`
get_ips_name_list ${REQUIRES} >${REQ_TEMP}
get_ips_name_list ${BUILD_REQUIRES} > ${BREQ_TEMP}

echo ----- These package names are exist in include/packagenames.define*.inc, perfectly ?---
echo ----- You need to check include/packagenames.define*.inc. -----------------------------
cat ${REQ_TEMP} | sed 's/^\([^ ]*\)[\ \t]*pkg:\/\([^@]*\)@.*$/%define pnm_requires_\1 \2/' | sed 's/-/_/g'
cat ${BREQ_TEMP}| sed 's/^\([^ ]*\)[\ \t]*pkg:\/\([^@]*\)@.*$/%define pnm_buildrequires_\1 \2/' | sed 's/-/_/g'

echo ------ Cut Here, and Change to ${SPECFILE} by your hand -----------------------------------
cat ${REQ_TEMP} | awk '{printf"Requires: %%{pnm_requires_%s}\n",$1}' | sed 's/-/_/g'
cat ${BREQ_TEMP}| awk '{printf"BuildRequires: %%{pnm_buildrequires_%s}\n",$1}' | sed 's/-/_/g'

rm -f ${REQ_TEMP} ${BREQ_TEMP}
