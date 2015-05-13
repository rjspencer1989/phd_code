function(doc){
    if(doc.collection === "devices" && doc.connected === true){
        emit(doc.mac_address, doc);
    }
}
