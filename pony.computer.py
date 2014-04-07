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


def env(variable, default = ''):
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
    Popen(command, stdin = sys.stdin, stdout = sys.stdout, stderr = sys.stderr).wait()

def spawn_pipe(*command):
    '''
    Spawn an external process and read its output
    
    @param   command:*str  The command arguments
    @return  :str          The output to the command's stdout, with at most one trailing LF removed
    '''
    out = Popen(command, stdin = sys.stdin, stdout = PIPE, stderr = sys.stderr).communicate()[0]
    out = out.decode('utf-8', 'replace')
    return out[:-1] if out.endswith('\n') else out

def print(text = '', end = '\n', flush = True):
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

def printerr(text = '', end = '\n', flush = True):
    '''
    stderr equivalent to print()
    
    @param  text:str    The text to print (empty string is default)
    @param  end:str     The appendix to the text to print (line breaking is default)
    @param  flush:bool  Whether to flush the output
    '''
    sys.stderr.buffer.write((str(text) + end).encode('utf-8'))
    if flush:
        sys.stderr.buffer.flush()

def printtag(name, value, flush = False):
    '''
    Print a tag
    
    @param  name:str    The name of the tag
    @param  value:str   The value of the tag
    @param  flush:bool  Whether to flush the output
    '''
    print('\033[%sm%s:\033[00;%sm %s' % (tagc, name, valuec, value), end = '\n', flush = flush)

def try_(*functions):
    '''
    Try a series of functions an return the return of whatever function that did not raise an exception
    
    @param   functions:*()→¿V?  Functions to try to run
    @return  :¿V?|''            The return of the first function that works, empty string on total failure
    '''
    for function in functions:
        try:
            return function()
        except:
            pass
    return ''

def cat(pathname):
    '''
    Read a file
    
    @param   pathname:str  The file to read
    @return  :str          The file's contain with trailing NF:s removed
    '''
    with open(pathname, 'r') as file:
        return file.read().rstrip('\n')

def unique(items):
    '''
    Keep only one copy of duplicate items
    
    @param   items:itr<¿V?>  The items
    @return  :list<¿V?>      The items deduplicated
    '''
    rc, last = [], None
    for item in items:
        if item == last:
            continue
        rc.append(item)
        last = item
    return rc

def strdur(seconds):
    '''
    Convert an amount of seconds to a human readable duration representation
    
    @param   seconds:float|str  The number of seconds of the duration
    @return  :str               The duration as a string
    '''
    (seconds, s) = divmod(float(seconds), 60)
    (seconds, m) = divmod(seconds, 60)
    (d, h) = divmod(seconds, 24)
    return '%id%02i:%02i:%05.2f' % (d, h, m, s)


def infofunc():
    '''
    Print system information to stdout
    '''
    S = lambda cmd : spawn_pipe(*(cmd.split()))
    uname = os.uname()
    printtag('User', env('USER'))
    printtag('Home', home)
    printtag('Hostname', uname.nodename)
    printtag('Distribution', distro)
    osname = (S('uname --operating-system'), uname.sysname, uname.release)
    printtag('Operating system', '%s with %s %s kernel' % osname)
    printtag('Kernel version', uname.version)
    printtag('Processor architecture', uname.machine)
    if os.path.exists('/proc'):
        try:
            cpuinfo = cat('/proc/cpuinfo').split('\n')
            cpu = [line for line in cpuinfo if line.startswith('model name')]
            for cpu in [line.split(':')[1] for line in unique(sorted(cpu))]:
                printtag('Processor model', cpu.strip())
            cpu = sum([float(line.split(':')[1].strip()) for line in cpuinfo if line.startswith('cpu MHz')])
            printtag('Current CPU speed', '%.0f MHz' % cpu)
        except:
            pass
        try_(lambda : printtag('Load average', cat('/proc/loadavg')))
        try_(lambda : printtag('Uptime', '%s %s' % tuple([strdur(c) for c in cat('/proc/uptime').split()])))
        try:
            mem = cat('/proc/meminfo').split('\n')
            mem = dict([[cell.strip() for cell in line.split(':')[:2]] for line in mem])
            try_(lambda : printtag('Total memory', '%s + %s swap' % (mem['MemTotal'], mem['SwapTotal'])))
            try_(lambda : printtag('Hardware corrupted memory', mem['HardwareCorrupted']))
            try_(lambda : printtag('Kernel memory', '%s stack + %s slab' % (mem['KernelStack'], mem['Slab'])))
            try_(lambda : printtag('Shared memory', mem['Shmem']))
            try_(lambda : printtag('Locked memory', '%s, %s unevictable' % (mem['Mlocked'], mem['Unevictable'])))
            try_(lambda : printtag('Memory buffers', mem['Buffers']))
            try_(lambda : printtag('Cached memory', '%s + %s swap' % (mem['Cached'], mem['SwapCached'])))
        except:
            pass
        try:
            route = [line.split('\t')[2] for line in cat('/proc/net/route').split('\n')]
            route = [line for line in route if ('Gateway' not in line) and ('00000000' not in line)]
            for g in route:
                g = '%i.%i.%i.%i' % (int(g[6:8], 16), int(g[4:6], 16), int(g[2:4], 16), int(g[0:2], 16))
                printtag('Default gateway', g)
        except:
            pass
    printtag('Shell', env('SHELL'))
    printtag('Shell version', spawn_pipe(env('SHELL'), '--version').split('\n')[0])
    printtag('Teletypewriter', try_(lambda : os.ttyname(2), lambda : os.ttyname(0)))
    printtag('Terminal', '%s %s' % (env('TERM'), env('COLORTERM')))
    printtag('X display', env('DISPLAY'))
    printtag('Wayland display', env('WAYLAND_DISPLAY'))
    printtag('Window manager', env('DESKTOP_SESSION'))
    printtag('Editor', env('EDITOR'))
    printtag('Locale', env('LANG'))


def invoke_read(function):
    '''
    Read the output to stdout make by a function
    
    @param   function:()→void  The function to invoke and read read stdout output from
    @return  :str              The function's output to stdout
    '''
    # Create pipe for intraprocess use.
    (r_end, w_end) = os.pipe()
    
    # Backup stdout.
    stdout = os.dup(1)
    os.close(1)
    
    # Replace stdout with the write end of the pipe.
    os.dup2(w_end, 1)
    os.close(w_end)
    
    # Invoke the functions, its stdout will be
    # the write end of the pipe.
    function()
    # Flush output.
    sys.stdout.buffer.flush()
    
    # Close the pipe.
    os.close(1)
    
    # Read from the pipe.
    rc = None
    with os.fdopen(r_end, 'rb') as file:
        rc = file.read()
    
    # Restore stdout.
    os.dup2(stdout, 1)
    os.close(stdout)
    
    # Decode output.
    rc = rc.decode('utf-8', 'replace')
    # Remove at most on trailing NF.
    return rc[:-1] if rc.endswith('\n') else rc


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
             (XDG_CONFIG_HOME, '%s/pony.computerrc'),
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
    conffiles += [(home, pathpattern) for _, pathpattern in conffiles[2:]]
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
    print(env('PONYSAY_KMS_PALETTE'), end = '', flush = False)
elif not env('PONYSAY_KMS_PALETTE_CMD', '') == '':
    # We have a palette printing command,
    # we are wrapping it with printing so
    # that it does not print an empty line.
    print(spawn_pipe('sh', '-c', env('PONYSAY_KMS_PALETTE_CMD')), end = '', flush = False)

## Jump to where the text should begin.
print('\033[%i;1H' % (top + 1), end = '', flush = True)

## Get system information.
info = invoke_read(infofunc)
## Prepend whitespace to the left side of the text.
whitespace = '' if left == 0 else ('\033[%iC' % left)
info = whitespace + info.replace('\n', '\n' + whitespace)

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

