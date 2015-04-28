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
		"s/\(^127.0.0.1\tlocalhost$\)/127.0.0.1\tlocalhost\t${n}/g" \
		/etc/hosts
	return 0
}

#
# Autostart for hostapd daemon is disabled.
#
hwr_conf_init () {

	t=`which rcconf`
	[ -z $t ] && echo="rcconf not found" && return 1

	[ ! -e /etc/init.d/hostapd ] && echo "hostapd not installed" && \
	return 1
	/etc/init.d/hostapd stop

	rcconf --off hostapd
	return 0
}

#
# User 'homeuser' autologins.
#
hwr_conf_tty1 () {

	f="/etc/init/tty1.conf"
	# $f exists by default
	l=`sed -n '/^exec \/sbin\/getty -8 38400 tty1 -a homeuser$/p' $f`
	[ -n "$l" ] && return 0

	cp -f $f $f.bak
	sed -i 's/^exec \/sbin\/getty -8 38400 tty1$/exec \/sbin\/getty -8 38400 tty1 -a homeuser/' $f
	return 0
}

usage () {
	echo "usage: setup.sh [[-a all] | [-i init] [-p power] [-l login] [-n host] [-h help]]"
}

all () {
	hwr_conf_init
	hwr_conf_acpi
	hwr_conf_host
	hwr_conf_tty1
	prep_install
}

prep_install () {
	. $HOME/router.conf
	mkdir -p $PIDDIR
	ehco -e "#!/bin/sh -e\niptables -t nat -A POSTROUTING -o $GATEWAY -j MASQUERADE\nreturn0" > /etc/rc.local
}

while [ $1 ]; do
	case $1 in
		-h | --help )	usage
						exit
						;;
		-l | --login )	hwr_conf_tty1
						;;
		-i | --init	)	hwr_conf_init
						;;
		-p | --power )	hwr_conf_acpi
						;;
		-n | --host	)	hwr_conf_host
						;;
		-d | --piddir )	prep_install
		;;
		-a | --all	)	all
						;;
		* )
						usage
						exit 1
	esac
	shift
done
