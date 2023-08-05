#!/bin/bash

function _common_systemd_pitfalls {
    local cmd=$1
    # do some sanity checks on $cmd to see things we don't expect to work

    if [[ "$cmd" =~ "sudo" ]]; then
        local msg=<<EOF
You are trying to use run_process with sudo, this is not going to work under systemd.

If you need to run a service as a user other than $STACK_USER call it with:

   run_process \$name \$cmd \$group \$user
EOF
        die $LINENO $msg
    fi

    if [[ ! "$cmd" =~ ^/ ]]; then
        local msg=<<EOF
The cmd="$cmd" does not start with an absolute path. It will fail to
start under systemd.

Please update your run_process stanza to have an absolute path.
EOF
        die $LINENO $msg
    fi

}

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

KILL_PATH="$(which kill)"

function write_user_unit_file {
    local service=$1
    local command="$2"
    local group=$3
    local user=$4
    local extra=""
    if [[ -n "$group" ]]; then
        extra="Group=$group"
    fi
    local unitfile="/etc/systemd/system/$service"
    mkdir -p /etc/systemd/system/

    iniset -sudo $unitfile "Unit" "Description" "RHOSP13 $service"
    if [[ -n "$user" ]]; then
        iniset -sudo $unitfile "Service" "User" "$user"
    fi
    iniset -sudo $unitfile "Service" "ExecStart" "$command"
    iniset -sudo $unitfile "Service" "KillMode" "process"
    iniset -sudo $unitfile "Service" "TimeoutStopSec" "300"
    iniset -sudo $unitfile "Service" "ExecReload" "$KILL_PATH -HUP \$MAINPID"
    if [[ -n "$group" ]]; then
        iniset -sudo $unitfile "Service" "Group" "$group"
    fi
    iniset -sudo $unitfile "Install" "WantedBy" "multi-user.target"

    # changes to existing units sometimes need a refresh
    sudo systemctl daemon-reload
}

STACK_USER="stack"

function _run_under_systemd {
    local service=$1
    local command="$2"
    local cmd=$command
    # sanity check the command
    _common_systemd_pitfalls "$cmd"

    local systemd_service="$service.service"
    local group=$3
    #local user=${4:-$STACK_USER}
    local user=$4
    if [[ "$command" =~ "uwsgi" ]] ; then
        write_uwsgi_user_unit_file $systemd_service "$cmd" "$group" "$user"
    else
        write_user_unit_file $systemd_service "$cmd" "$group" "$user"
    fi

    sudo systemctl enable $systemd_service
    sudo systemctl start $systemd_service
}

function run_process {
    local service=$1
    local command=$2
    local group=$3
    local user=$4

    local name=$service

    _run_under_systemd "$name" "$command" "$group" "$user"
}


########### main process ###########
run_process $1 "$2" $3 $4
