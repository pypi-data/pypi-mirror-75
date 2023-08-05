#!/bin/bash

function ini_has_option {
    local xtrace
    xtrace=$(set +o | grep xtrace)
    set +o xtrace
    local file=$1
    local section=$2
    local option=$3
    local line

    line=$(sed -ne "/^\[$section\]/,/^\[.*\]/ { /^$option[ \t]*=/ p; }" "$file")
    $xtrace
    [ -n "$line" ]
}

function iniset {
    local xtrace
    xtrace=$(set +o | grep xtrace)
    set +o xtrace
    local sudo=""
    if [ $1 == "-sudo" ]; then
        sudo="sudo "
        shift
    fi
    local file=$1
    local section=$2
    local option=$3
    local value=$4

    if [[ -z $section || -z $option ]]; then
        $xtrace
        return
    fi

    if ! grep -q "^\[$section\]" "$file" 2>/dev/null; then
        # Add section at the end
        echo -e "\n[$section]" | $sudo tee --append "$file" > /dev/null
    fi
    if ! ini_has_option "$file" "$section" "$option"; then
        # Add it
        $sudo sed -i -e "/^\[$section\]/ a\\
$option = $value
" "$file"
    else
        local sep
        sep=$(echo -ne "\x01")
        # Replace it
        $sudo sed -i -e '/^\['${section}'\]/,/^\[.*\]/ s'${sep}'^\('"${option}"'[ \t]*=[ \t]*\).*$'${sep}'\1'"${value}"${sep} "$file"
    fi
    $xtrace
}

function build_spp_vf_service() {
    local sec_id=$1
    local core_mask=$2
    local service="spp_vf-$sec_id.service"
    local unitfile="/etc/systemd/system/$service"

    SEC_BIN=$4
    SEC_CMD="$SEC_BIN -c $core_mask -n 4 --proc-type secondary -- --client-id $sec_id -s 127.0.0.1:$3 --vhost-client"

    iniset -sudo $unitfile "Unit" "Description" "RHOSP13 $service"
    iniset -sudo $unitfile "Service" "User" "root"
    iniset -sudo $unitfile "Service" "ExecStart" "$SEC_CMD"
}

################# main process #################
build_spp_vf_service $1 $2 $3 $4
