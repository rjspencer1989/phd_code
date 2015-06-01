function(doc){
    if(doc.collection === "devices" && doc.connection_event === "connect"){
        emit(doc.mac_address, doc);
    }
}
