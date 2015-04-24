#!/bin/bash
start(){
    echo "starting"
    service hostapd start
    service hostapd stop
    # addr=`ifconfig $WLESS_IF | awk '/HWaddr/ {print "02" substr($5, 3, length($5) - 4) "00"}'`
    # ifconfig $WLESS_IF hw ether $addr
    iptables -t nat -A POSTROUTING -o $GATEWAY -j MASQUERADE
    [ "$(lsmod | grep bridge)" ] && rmmod bridge
    modprobe openvswitch
    [ -e ovsdb.conf ] && rm ovsdb.conf
    ovsdb-tool create ovsdb.conf /usr/local/share/openvswitch/vswitch.ovsschema
    f="/var/run/ovsdb-server"
    ovsdb-server ovsdb.conf --remote=punix:$f --detach --monitor --pidfile=$PIDDIR/ovsdb-server.pid
    ovs-vswitchd unix:$f --detach --monitor --pidfile=$PIDDIR/ovs-vswitchd.pid

    ovs-vsctl --db=unix:$f init
    ovs-vsctl --db=unix:$f add-br $BRIDGE
    ovs-vsctl --db=unix:$f set-fail-mode $BRIDGE standalone
    ovs-vsctl --db=unix:$f set-controller $BRIDGE tcp:127.0.0.1:6633
    ovs-vsctl --db=unix:$f add-port $BRIDGE $WLESS_IF
    ovs-vsctl --db=unix:$f add-port $BRIDGE $WIRED_IF

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

bridgeStatus(){
    f="/var/run/ovsdb-server" # Listens on $f for a connection.
    ovs-vsctl --db=unix:$f list-ifaces $BRIDGE
    return 0
}

stop(){
    echo "stopping"
    f="/var/run/ovsdb-server" # Listens on $f for a connection.
    ifconfig $BRIDGE down
    ovs-vsctl --db=unix:$f del-port $BRIDGE $WLESS_IF
    ovs-vsctl --db=unix:$f del-port $BRIDGE $WIRED_IF
    ovs-vsctl --db=unix:$f del-br $BRIDGE

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

    rmmod openvswitch
    service hostapd stop
}

user=`id -u`
if [ $user != "0" ]; then
    echo "error: this script must be run as root" 1>&2
    exit 1
fi
cd $HOME
. router.conf

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    status)
        bridgeStatus
        ;;
    *)
        echo $"Usage: $0 {start|stop}"
        exit 1
        ;;
esac
