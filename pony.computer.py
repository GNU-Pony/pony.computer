#!/usr/bin/env python3
'''
pony.computer – Show computer information and a pony

Copyright © 2013, 2014  Mattias Andrée (maandree@member.fsf.org)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import random
import os
import sys
from subprocess import Popen, PIPE


global ponies, padding, top, tagc, valuec, home


distro = ''
'''
:str  Fallback value for the operating system distribution name.
'''

ponies = ['+f fyrefly']
'''
:list<list<str>|str>  List of options to choose from that should be
                      passed to ponysay to print a pony. If an element
                      in this list is a string, rather than list or
                      tuple, it is split at whitespace with empty
                      elements removed.
'''

padding = 8
'''
:int  The number of columns between the right side of the pony and
      the left side of the text.
'''

top = 1
'''
:int  The number of empty lines above the text
'''

tagc = '01;35'
'''
:str  The colour of the tag names in the text
'''

valuec = '01;34'
'''
:str  The colour of the tag values in the text
'''


def env(variable, default = None):
    '''
    Read an environment variable
    
    @param   variable:str     The name of the environment variable
    @param   default:str?     The value to use if the variable is not defined (defined if empty)
    @return  :str|{default:}  The environment variable's value, but `default` if not defined
    '''
    return os.environ[variable] if variable in os.environ else default

def spawn(*command):
    '''
    Spawn an external process
    
    @param  command:*str  The command arguments
    '''
    Popen(command, sys.stdin = sys.stdin, stdout = sys.stdout, stderr = sys.stderr).wait()

def spawn_pipe(*command):
    '''
    Spawn an external process and read its output
    
    @param   command:*str  The command arguments
    @return  :str          The output to the command's stdout, with at most one trailing LF removed
    '''
    out = Popen(command, sys.stdin = sys.stdin, stdout = PIPE, stderr = sys.stderr).communuicate()[0]
    return out[:-1] if out.endswith('\n') else out

def print(text = '', end = '\n', flush = False):
    '''
    Hack to enforce UTF-8 in output (in the future, if you see anypony not using utf-8 in
    programs by default, report them to Princess Celestia so she can banish them to the moon)
    
    @param  text:str    The text to print (empty string is default)
    @param  end:str     The appendix to the text to print (line breaking is default)
    @param  flush:bool  Whether to flush the output
    '''
    sys.stdout.buffer.write((str(text) + end).encode('utf-8'))
    if flush:
        sys.stdout.buffer.flush()

def printerr(text = '', end = '\n', flush = False):
    '''
    stderr equivalent to print()
    
    @param  text:str    The text to print (empty string is default)
    @param  end:str     The appendix to the text to print (line breaking is default)
    @param  flush:bool  Whether to flush the output
    '''
    sys.stderr.buffer.write((str(text) + end).encode('utf-8'))
    if flush:
        sys.stderr.buffer.flush()


def infofunc() ## FIXME not ported
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
    echo -e "\e[${left}C\e[${tagc}mWindow manager:\e[00;${valuec}m ${DESKTOP_SESSION}"
    echo -e "\e[${left}C\e[${tagc}mEditor:\e[00;${valuec}m ${EDITOR}"
    echo -e "\e[${left}C\e[${tagc}mLocale:\e[00;${valuec}m ${LANG}"


## Get distribution name by way of reading /etc/os-release or /etc/lsb-release
etc_distro = ''
if os.path.exists('/etc/os-release'):
    etc_distro = spawn_pipe('sh', '-c', '. /etc/os-release && echo "${PRETTY_NAME}"')
elif os.path.exists('/etc/lsb-release'):
    etc_distro = spawn_pipe('sh', '-c', '. /etc/lsb-release && echo "${DISTRIB_DESCRIPTION}"')
# Use fallback, specified by packager, if not found
if not etc_distro == '':
    distro = etc_distro


## Read environment variables, select empty
## strings for those that are not defined
## because both empty and not defined should
## be treated as not defined.
XDG_CONFIG_HOME = env('XDG_CONFIG_HOME', '')
HOME = home     = env('HOME', '')
XDG_CONFIG_DIRS = env('XDG_CONFIG_DIRS', '')

## List possible configuration script files.
# From $HOME/.config and $HOME:
conffiles = [(XDG_CONFIG_HOME, '%s/pony.computer/pony.computerrc'),
             (HOME, '%s/.config/pony.computer/pony.computerrc'),
             (HOME, '%s/.config/pony.computerrc'),
             (HOME, '%s/.config/.pony.computerrc'),
             (HOME, '%s/.pony.computerrc')]
# From ~/.config and ~:
try:
    import pwd
    # Get home directory for the real user.
    home = pwd.getpwuid(os.getuid()).pw_dir
    # As the listing above except with actual home.
    conffiles += [(home, pathpattern) for _, pathpattern in conffiles[1:]]
except:
    # What, you are not even running a Unix-like system‽
    # Or do you not exist...?
    pass
# System-wide alternatives:
conffiles += [(confdir, '%s/pony.computerrc') for confdir in XDG_CONFIG_DIRS.split(':')]
conffiles.append((None, '/etc/pony.computerrc'))


## Look for the highest-precedence existing configuration file.
for superdir, pathpattern in conffiles:
    ## Base pathname on pattern, or just the pattern
    ## verbatim if we do not have `superdir`.
    pathname = pathpattern
    if superdir is not None:
        if superdir == '':
            # The environment variable we not defined
            # continue with next alternative.
            continue
        # Add the environment variable to the pathname.
        pathname %= superdir
    code = None
    try:
        ## Read the configuration script, if it exists.
        with open(pathname, 'r') as file:
            code = file.read()
    except:
        # It is easier to ask for forgiveness than for permission.
        continue
    
    ## Combine our globals and locals for the
    ## configuration script to use.
    _globals_, _locals_ = globals(), dict(locals())
    for key in _locals_:
        _globals_[key] = _locals_[key]
    
    ## Add a line breaking at the end so we do not get any
    ## error if the last line is not terminated.
    code += '\n'
    ## Compile configuration script.
    code = compile(code, pathname, 'exec')
    ## Load configuration script.
    exec(code, _globals_)
    ## Stop searching, with found the one with highest precedence.
    break


## Select ponysay options
pony = random.choice(ponies)
# If the selected options were defined as one string,
if isinstance(pony, str):
    # split at at whitespace and remove empty arguments.
    pony = [arg for arg in pony.split() if not arg == '']


## Fetch information about the selected pony.
ponyinfo = spawn_pipe('ponysay', '-i', *pony).split('\n')
select_info = lambda key : int([line for line in ponyinfo if ('m%s\033' % key) in line][0].split(': ')[1])

## Extract the width of the pony to
## determine where the text should start.
left = padding + select_info('WIDTH')

## Extract the height of the pony.
height = select_info('HEIGHT') - select_info('BALLOON TOP') - select_info('BALLOON BOTTOM')

## Truncate height to the size of the terminal.
height = min(height, int(spawn_pipe('stty', 'size').split()[0]))


## Jump to beginning of terminal,
## this is done to avoid some effects,
## that is difficult to fully work around
## in all terminals.
print('\033[H\033[2J', end = '', flush = True)

## Print the pony with ponysay.
spawn('ponysay', '-o', *pony)

## Reset palette after ponysay.
if not env('PONYSAY_KMS_PALETTE', '') == '':
    # We have a palette.
    print(env('PONYSAY_KMS_PALETTE'), end = '')
else:
    # We have a palette printing command,
    # we are wrapping it with printing so
    # that it does not print an empty line.
    print(spawn_pipe('sh', '-c', 'exec %s' % env('PONYSAY_KMS_PALETTE_CMD')), end = '')

## Jump to where the text should begin.
print('\033[%i;1H' % (top + 1), end = '', flush = True)


info="$(infofunc)" ## FIXME not ported

## Print the information.
print(info, end = '\n', flush = True)
## Count lines in the information.
lines = len(info.split('\n'))
## And check how many lines we should jump
## down to get to the end of this program's output.
lines = height - lines - top - 1
## Jump to the end of the output.
if lines > 0:
    print('\033[%iB' % lines, end = '', flush = True)

