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

function build_spp_primary_service() {
    local service="spp_primary.service"
    local unitfile="/etc/systemd/system/$service"

    PORT_MASK=0
    for ((i=0; i<$1; i++)); do
        PORT_MASK=$(( $PORT_MASK + (1 << $i) ))
    done
    NUM_VHOST=$2
    NUM_RING=$(( $NUM_VHOST * 2 ))

    PRIMARY_BIN=$7
    PRIMARY_CMD="$PRIMARY_BIN -c $3 -n 4 --socket-mem $4 --huge-dir $5 --proc-type primary -- -p $PORT_MASK -n $NUM_RING -s 127.0.0.1:$6"

    iniset -sudo $unitfile "Unit" "Description" "RHOSP13 $service"
    iniset -sudo $unitfile "Service" "User" "root"
    iniset -sudo $unitfile "Service" "ExecStart" "$PRIMARY_CMD"
}


################# main process #################
build_spp_primary_service $1 $2 $3 $4 $5 $6 $7
