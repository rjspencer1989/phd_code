function(doc){
    if(doc.collection === "devices" && doc.connection_event === "connect" && doc.state === "permit" && (doc.port === "wlan0" || doc.port === "wlan0_1")){
        emit(doc.mac_address, doc);
    }
}
