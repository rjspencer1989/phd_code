#!/bin/bash
service homework-pox stop
service homework-notifications stop
service homework-notification-registration stop
service homework-wifi-processor stop
service homework-undo stop
service homework-rollback stop
service homework-device-edit-processor stop
service homework-ethtool-monitor stop
service homework-iw-monitor stop
service homework-user-edit stop
service homework-set-dns stop
service homework-break-dns stop
curl http://admin:homework@localhost:8000/config -X DELETE
curl http://admin:homework@localhost:8000/config -X PUT
cd database && couchapp push && cd ..
rm /etc/hostapd.deny
touch /etc/hostapd.deny
/etc/init.d/hostapd reload
ifdown eth1
ifdown eth2
ifdown eth3
/etc/init.d/hostapd stop
service homework-notifications start
service homework-notification-registration start
service homework-wifi-processor start
service homework-undo start
service homework-rollback start
service homework-device-edit-processor start
service homework-ethtool-monitor start
service homework-iw-monitor start
service homework-user-edit start
service homework-set-dns start
service homework-break-dns start
service homework-pox start
