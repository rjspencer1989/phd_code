#!/bin/bash
start(){
    echo "starting"
    ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock --detach --monitor --pidfile=$PIDDIR/ovsdb-server.pid
    ovs-vswitchd --detach --monitor --pidfile=$PIDDIR/ovs-vswitchd.pid

    cd pox
    ./pox.py misc.full_payload misc.pidfile --file=$PIDDIR/pox.pid --force homework_dhcp homework_routing homework &> $HOME/pox.out &
    ifconfig $BRIDGE $GATEWAY_ADDRESS up
    ifconfig $WIRED_IF down
    ifconfig $WLESS_IF down
    ifconfig $WIRED_IF "0.0.0.0" up
    ifconfig $WLESS_IF "0.0.0.0" up
    echo "1" > /proc/sys/net/ipv4/ip_forward
    service hostapd start
    return 0
}

stop(){
    echo "stopping"
    ifconfig $BRIDGE down

    [ -e $PIDDIR/pox.pid ] && (
	pid=`cat $PIDDIR/pox.pid`
	kill $pid
	rm $PIDDIR/pox.pid
    )

    [ -e $PIDDIR/ovs-vswitchd.pid ] && (
        pid=`cat $PIDDIR/ovs-vswitchd.pid`
        kill $pid
    )

    [ -e $PIDDIR/ovsdb-server.pid ] && (
        pid=`cat $PIDDIR/ovsdb-server.pid`
        kill $pid
    )

    service hostapd stop
}

user=`id -u`
if [ $user != "0" ]; then
    echo "error: this script must be run as root" 1>&2
    exit 1
fi
cd /home/homeuser
. router.conf

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    *)
        echo $"Usage: $0 {start|stop}"
        exit 1
        ;;
esac
