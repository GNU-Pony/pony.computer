# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

# The package path prefix, if you want to install to another root, set DESTDIR to that root
PREFIX ?= /usr
# The command path excluding prefix
BIN ?= /bin
# The resource path excluding prefix
DATA ?= /share
# The command path including prefix
BINDIR ?= $(PREFIX)$(BIN)
# The resource path including prefix
DATADIR ?= $(PREFIX)$(DATA)
# The generic documentation path including prefix
DOCDIR ?= $(DATADIR)/doc
# The info manual documentation path including prefix
INFODIR ?= $(DATADIR)/info
# The license base path including prefix
LICENSEDIR ?= $(DATADIR)/licenses

# Python 3 command to use in shebangs
SHEBANG = /usr$(BIN)/env python3
# The name of the command as it should be installed
COMMAND = pony.computer
# The name of the package as it should be installed
PKGNAME = pony.computer

# Specify operating system distribution here,
# make sure it does not cause syntax error when
# resolved.
DISTRO = 



# Build rules

.PHONY: default
default: pony.computer # info

.PHONY: all
all: pony.computer # doc

#.PHONY: doc
#doc: info pdf dvi ps

#.PHONY: info
#info: pony.computer.info
#%.info: info/%.texinfo info/fdl.texinfo
#	makeinfo "$<"

#.PHONY: pdf
#pdf: pony.computer.pdf
#%.pdf: info/%.texinfo info/fdl.texinfo
#	mkdir -p obj
#	cd obj && yes X | texi2pdf "../$<"
#	mv "obj/$@" "$@"

#.PHONY: dvi
#dvi: pony.computer.dvi
#%.dvi: info/%.texinfo info/fdl.texinfo
#	mkdir -p obj
#	cd obj && yes X | $(TEXI2DVI) "../$<"
#	mv "obj/$@" "$@"

#.PHONY: ps
#ps: pony.computer.ps
#%.ps: info/%.texinfo info/fdl.texinfo
#	mkdir -p obj
#	cd obj && yes X | texi2pdf --ps "../$<"
#	mv "obj/$@" "$@"

pony.computer: pony.computer.py
	cp "$<" "$@"
	sed -i 's:#!/usr/bin/env python3:#!$(SHEBANG):' "$@"
	sed -i "s#^distro = ''"'$$'"#distro = '$(DISTRO)'#" "$@"


# Install rules

.PHONY: install
install: install-base # install-info

.PHONY: install-all
install-all: install-base # install-doc

.PHONY: install-base
install-base: install-command install-license

.PHONY: install-command
install-command: pony.computer
	install -dm755 -- "$(DESTDIR)$(BINDIR)"
	install -m755 "$<" -- "$(DESTDIR)$(BINDIR)/$(COMMAND)"

.PHONY: install-license
install-license:
	install -dm755 -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"
	install -m644 COPYING LICENSE -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"

#.PHONY: install-doc
#install-doc: install-info install-pdf install-ps install-dvi

#.PHONY: install-info
#install-info: pony.computer.info
#	install -dm755 -- "$(DESTDIR)$(INFODIR)"
#	install -m644 "$<" -- "$(DESTDIR)$(INFODIR)/$(PKGNAME).info"

#.PHONY: install-pdf
#install-pdf: pony.computer.pdf
#	install -dm755 -- "$(DESTDIR)$(DOCDIR)"
#	install -m644 "$<" -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).pdf"

#.PHONY: install-ps
#install-ps: pony.computer.ps
#	install -dm755 -- "$(DESTDIR)$(DOCDIR)"
#	install -m644 "$<" -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).ps"

#.PHONY: install-dvi
#install-dvi: pony.computer.dvi
#	install -dm755 -- "$(DESTDIR)$(DOCDIR)"
#	install -m644 "$<" -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).dvi"


# Uninstall rules

uninstall:
	rm -- "$(DESTDIR)$(BINDIR)/$(COMMAND)"
	rm -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)/COPYING"
	rm -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)/LICENSE"
	rmdir -- "$(DESTDIR)$(LICENSEDIR)/$(PKGNAME)"
#	rm -- "$(DESTDIR)$(INFODIR)/$(PKGNAME).info"
#	rm -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).pdf"
#	rm -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).ps"
#	rm -- "$(DESTDIR)$(DOCDIR)/$(PKGNAME).dvi"


# Clean rules

.PHONY: clean
clean:
	-rm -rf pony.computer # pony.computer.{info,pdf,ps,dvi} obj

