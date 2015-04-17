#!/bin/bash

#
# Every function, if unsuccessful, returns
# an error message stored in $C_MSG.
#
C_MSG=

hwr_conf_acpi () {

	f="/etc/acpi/events/powerbtn"
	if [ ! -e $f ]; then
		C_MSG="$f not found" # acpi not installed
		return 1
	fi

	l=`sed -n '/^action=\/bin\/true$/p' $f` # $f already configured
	if [ -z "$l" ]; then
		cp $f $f.bak
		# disable power button
		sed -i "s/\(^action.*\)/action=\/bin\/true\n/g" $f
	fi

	f="/etc/init/control-alt-delete.conf"
	# $f exists by default
	l=`sed -n '/^exec \/bin\/true$/p' $f` # $f already configured
	if [ -z "$l" ]; then
		cp $f $f.bak
		# disable ctrl-alt-del
		sed -i "s/\(^exec.*\)/exec \/bin\/true\n/g" $f
	fi
	# Restart acpi
	service acpid restart &>/dev/null
	return $?
}

#
# A hack.
#
hwr_conf_host () {

	n=`hostname`
	sed -i \
		"s/\(^127.0.0.1\tlocalhost$\)/127.0.0.1\tlocalhost ${n}/g" \
		/etc/hosts
	return 0
}

#
# User 'homeuser' becomes a sudoer.
#
hwr_conf_user () {

	[ -e /etc/sudoers.d/homework ] && return 0

	echo "homeuser ALL=(ALL) NOPASSWD: ALL" > homework.sudoer
	mv homework.sudoer /etc/sudoers.d/homework
	chmod 0440 /etc/sudoers.d/homework
	return $?
}

#
# Autostart for hostapd, dnsmasq, and tomcat6 daemons is disabled.
#
hwr_conf_init () {

	t=`which rcconf`
	[ -z $t ] && C_MSG="rcconf not found" && return 1

	[ ! -e /etc/init.d/hostapd ] && C_MSG="hostapd not installed" && \
	return 1
	/etc/init.d/hostapd stop &>/dev/null

	[ ! -e /etc/init.d/dnsmasq ] && C_MSG="dnsmasq not installed" && \
	return 1
	/etc/init.d/dnsmasq stop &>/dev/null

	[ ! -e /etc/init.d/tomcat6 ] && C_MSG="tomcat6 not installed" && \
	return 1
	/etc/init.d/tomcat6 stop &>/dev/null

	rcconf --off tomcat6,dnsmasq,hostapd &> /dev/null
	return 0
}

#
# User 'homeuser' autologins.
#
hwr_conf_tty1 () {

	f="/etc/init/tty1.conf"
	# $f exists by default

	l=`sed -n '/^exec \/sbin\/getty -8 38400 tty1$/p' $f`
	[ -z "$l" ] && return 0

	cp -f $f $f.bak
	p="exec \/bin\/login -f homeuser < \/dev\/tty1 > \/dev\/tty1 2>\&1"
	sed -i "s/\(^exec.*\)/$p/g" $f
	return 0
}
