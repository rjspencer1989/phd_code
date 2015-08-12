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
curl http://homeuser:homework@localhost:8000/config -X DELETE
curl http://homeuser:homework@localhost:8000/config -X PUT
cd database && couchapp push && cd ..
service homework-notifications start
service homework-notification-registration start
service homework-wifi-processor start
service homework-undo start
service homework-rollback start
service homework-device-edit-processor start
service homework-ethtool-monitor start
service homework-iw-monitor start
service homework-user-edit start
