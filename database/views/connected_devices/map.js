function(doc){
    if(doc.collection === "devices" && doc.connection_event === "connected"){
        emit(doc.mac_address, doc);
    }
}
