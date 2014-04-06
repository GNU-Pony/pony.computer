# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without any warranty.

PREFIX = /usr
DATA = /share
BIN = /bin
PKGNAME = pony.computer
SHEBANG = /usr$(BIN)/env bash
COMMAND = pony.computer
LICENSES = $(PREFIX)$(DATA)


all: pony.computer #doc

#doc: info

#info: pony.computer.info

#%.info: info/%.texinfo
#	makeinfo "$<"

pony.computer: pony.computer.sh
	cp "$<" "$@"
	sed -i 's:#!/usr/bin/env bash:#!$(SHEBANG):' "$@"

install: pony.computer #pony.computer.info
	install -dm755 "$(DESTDIR)$(PREFIX)$(BIN)"
	install -m755 pony.computer "$(DESTDIR)$(PREFIX)$(BIN)"
	install -dm755 "$(DESTDIR)$(LICENSES)/$(PKGNAME)"
	install -m644 COPYING LICENSE "$(DESTDIR)$(LICENSES)/$(PKGNAME)"
#	install -dm755 "$(DESTDIR)$(PREFIX)$(DATA)/info"
#	install -m644 pony.computer.info "$(DESTDIR)$(PREFIX)$(DATA)/info/$(PKGNAME).info"

uninstall:
	rm -- "$(DESTDIR)$(PREFIX)$(BIN)/$(COMMAND)"
	rm -- "$(DESTDIR)$(LICENSES)/$(PKGNAME)/COPYING"
	rm -- "$(DESTDIR)$(LICENSES)/$(PKGNAME)/LICENSE"
	rmdir -- "$(DESTDIR)$(LICENSES)/$(PKGNAME)"
#	rm -- "$(DESTDIR)$(PREFIX)$(DATA)/info/$(PKGNAME).info"

.PHONY: clean
clean:
	-rm pony.computer

