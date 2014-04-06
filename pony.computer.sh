#!/usr/bin/env bash

##
# pony.computer – Show computer information and a pony
# 
# Copyright © 2013  Mattias Andrée (maandree@member.fsf.org)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##


ponies=('+f fyrefly')

pony=$(( $RANDOM % ${#ponies[@]} ))
pony="${ponies[$pony]}"

padding=8
top=1

tagc='01;35'
valuec='01;34'

if [ ! -z "$XDG_CONFIG_HOME" ] && [ -f "$XDG_CONFIG_HOME/pony.computer/pony.computerrc" ]; then
    . "$XDG_CONFIG_HOME/pony.computer/pony.computerrc"
elif [ ! -z "$HOME" ] && [ -f "$HOME/.config/pony.computer/pony.computerrc" ]; then
    . "$HOME/.config/pony.computer/pony.computerrc"
elif [ ! -z "$HOME" ] && [ -f "$HOME/.config/pony.computerrc" ]; then
    . "$HOME/.config/pony.computerrc"
elif [ ! -z "$HOME" ] && [ -f "$HOME/.config/.pony.computerrc" ]; then
    . "$HOME/.config/.pony.computerrc"
elif [ ! -z "$HOME" ] && [ -f "$HOME/.pony.computerrc" ]; then
    . "$HOME/.pony.computerrc"
elif [ -f ~/.pony.computerrc ]; then
    . ~/.pony.computerrc
elif [ -f /etc/pony.computerrc ]; then
    . /etc/pony.computerrc
fi

if [ -f "/etc/os-release" ]; then
    . "/etc/os-release"
fi

ponyinfo="$(ponysay -i $pony)"

left=$(( $(grep WIDTH <<< "$ponyinfo" | head -n 1 | cut -d : -f 2) + $padding ))
height=$(( $(grep HEIGHT <<< "$ponyinfo" | head -n 1 | cut -d : -f 2) ))
height=$(( $height - $(grep 'BALLOON TOP' <<< "$ponyinfo" | head -n 1 | cut -d : -f 2) ))
height=$(( $height - $(grep 'BALLOON BOTTOM' <<< "$ponyinfo" | head -n 1 | cut -d : -f 2) ))
lines=$(stty size | cut -d ' ' -f 1)

if (( $height > $lines )); then
    $height=$lines
fi

echo -en '\e[H\e[2J'

ponysay -o $pony

if [ ! "${PONYSAY_KMS_PALETTE}" = "" ]; then
    echo -en "${PONYSAY_KMS_PALETTE}"
elif [ ! "${PONYSAY_KMS_PALETTE_CMD}" = "" ]; then
    echo -en "$(${PONYSAY_KMS_PALETTE_CMD})"
fi

echo -en "\e[$(( ${top} + 1));1H"

function infofunc
{
    echo -e "\e[${left}C\e[${tagc}mUser:\e[00;${valuec}m ${USER}"
    echo -e "\e[${left}C\e[${tagc}mHome:\e[00;${valuec}m ${HOME}"
    echo -e "\e[${left}C\e[${tagc}mHostname:\e[00;${valuec}m ${HOSTNAME}"
    echo -e "\e[${left}C\e[${tagc}mDistribution:\e[00;${valuec}m ${PRETTY_NAME}"
    echo -e "\e[${left}C\e[${tagc}mOperating system:\e[00;${valuec}m $(uname --operating-system) with $(uname --kernel-name) $(uname --kernel-release) kernel"
    echo -e "\e[${left}C\e[${tagc}mKernel version:\e[00;${valuec}m $(uname --kernel-version)"
    echo -e "\e[${left}C\e[${tagc}mProcessor architecture:\e[00;${valuec}m $(uname --machine)"
    if [ -e /proc/cpuinfo ] && [ ! -d /proc/cpuinfo ]; then
	cat /proc/cpuinfo | grep '^model name' | sort | uniq | cut -d : -f 2 | while read processor; do
	    echo -e "\e[${left}C\e[${tagc}mProcessor model:\e[00;${valuec}m ${processor}"
	done
	echo -e "\e[${left}C\e[${tagc}mCurrent CPU speed:\e[00;${valuec}m $(python <<< "print($(echo $(cat /proc/cpuinfo | grep '^cpu MHz' | cut -d : -f 2 | sed -e 's:$: +:g') 0))") MHz"
    fi
    if [ -e /proc/loadavg ] && [ ! -d /proc/loadavg ]; then
	echo -e "\e[${left}C\e[${tagc}mLoad average:\e[00;${valuec}m $(cat /proc/loadavg)"
    fi
    if [ -e /proc/uptime ] && [ ! -d /proc/uptime ]; then
	echo -e "\e[${left}C\e[${tagc}mUptime:\e[00;${valuec}m $(cat /proc/uptime)"
    fi
    if [ -e /proc/meminfo ] && [ ! -d /proc/meminfo ]; then
	function mem
	{
	    cat /proc/meminfo | grep "^$1:" | cut -d : -f 2
	}
	echo -e "\e[${left}C\e[${tagc}mTotal memory:\e[00;${valuec}m" $(mem MemTotal) + $(mem SwapTotal) 'swap'
	echo -e "\e[${left}C\e[${tagc}mHardware corrupted memory:\e[00;${valuec}m" $(mem HardwareCorrupted)
	echo -e "\e[${left}C\e[${tagc}mKernel memory:\e[00;${valuec}m" $(mem KernelStack) 'stack +' $(mem Slab) 'slab'
	echo -e "\e[${left}C\e[${tagc}mShared memory:\e[00;${valuec}m" $(mem Shmem)
	echo -e "\e[${left}C\e[${tagc}mLocked memory:\e[00;${valuec}m" $(mem Mlocked), $(mem Unevictable) 'unevictable'
	echo -e "\e[${left}C\e[${tagc}mMemory buffers:\e[00;${valuec}m" $(mem Buffers)
	echo -e "\e[${left}C\e[${tagc}mCached memory:\e[00;${valuec}m" $(mem Cached) + $(mem SwapCached) 'swap'
    fi
    if [ -e /proc/net/route ] && [ ! -d /proc/net/route ]; then
	python -c 'g=input(); print("%i.%i.%i.%i" % (int(g[6:8], 16), int(g[4:6], 16), int(g[2:4], 16), int(g[0:2], 16)))' <<< "$(cat /proc/net/route | cut -f 3 | grep -v 'Gateway' | grep -v 00000000)" |
	while read line; do
	    echo -e "\e[${left}C\e[${tagc}mDefault gateway:\e[00;${valuec}m ${line}"
	done
    fi
    echo -e "\e[${left}C\e[${tagc}mShell:\e[00;${valuec}m ${SHELL}"
    echo -e "\e[${left}C\e[${tagc}mShell version:\e[00;${valuec}m $("${SHELL}" --version | head -n 1)"
    echo -e "\e[${left}C\e[${tagc}mTeletypewriter:\e[00;${valuec}m $(tty)"
    echo -e "\e[${left}C\e[${tagc}mTerminal:\e[00;${valuec}m ${TERM} ${COLORTERM}"
    echo -e "\e[${left}C\e[${tagc}mX display:\e[00;${valuec}m ${DISPLAY}"
    # TODO how do we identify the window manager?
    echo -e "\e[${left}C\e[${tagc}mEditor:\e[00;${valuec}m ${EDITOR}"
    echo -e "\e[${left}C\e[${tagc}mLocale:\e[00;${valuec}m ${LANG}"
}

info="$(infofunc)"
echo "$info"
lines=$(wc -l <<< "$info")
lines=$(( $height - $lines - $top - 1 ))

if (( $lines > 0 )); then
    echo -en '\e['$lines'B'
fi

