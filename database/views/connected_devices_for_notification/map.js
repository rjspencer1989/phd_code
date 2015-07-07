function(doc){
    if(doc.collection === "devices" && doc.connection_event === "connect" && doc.state === "permit"){
        emit(doc.mac_address, doc);
    }
}
