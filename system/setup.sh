#!/bin/bash

hwr_conf_acpi () {

	f="/etc/acpi/events/powerbtn"
	if [ ! -e $f ]; then
		return 1
	fi

	l=`sed -n '/^action=\/bin\/true$/p' $f` # $f already configured
	if [ -z "$l" ]; then
		cp $f $f.bak
		# disable power button
		sed -i "s/^action=\/etc\/acpi\/powerbtn.sh$/action=\/bin\/true\n/g" $f
	fi

	f="/etc/init/control-alt-delete.conf"
	rm $f
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
# Autostart for hostapd daemon is disabled.
#
hwr_conf_init () {

	t=`which rcconf`
	[ -z $t ] && C_MSG="rcconf not found" && return 1

	[ ! -e /etc/init.d/hostapd ] && C_MSG="hostapd not installed" && \
	return 1
	/etc/init.d/hostapd stop &>/dev/null

	rcconf --off hostapd &> /dev/null
	return 0
}

#
# User 'homeuser' autologins.
#
hwr_conf_tty1 () {

	f="/etc/init/tty1.conf"
	# $f exists by default
	l=`sed -n '/^exec \/sbin\/getty -8 38400 tty1 -a homeuser$/p' $f`
	[ -z "$l" ] && return 0

	cp -f $f $f.bak
	sed -i 's/^exec \/sbin\/getty -8 38400 tty1$/^exec \/sbin\/getty -8 38400 tty1 -a homeuser/' $f
	return 0
}

if [ $# -gt 0 ]; then
	while [ $1 ]; do
		echo $1
		shift
	done
else
	echo "need argument"
fi
