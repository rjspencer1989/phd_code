function(doc){
    if(doc.collection === "devices" && (doc.port === "wlan0" || doc.port === "wlan0_1")){
        emit(doc.mac_address, doc);
    }
}
