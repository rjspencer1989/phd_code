function(doc){
    if(doc.collection==="devices" && doc.notification_service !== ""){
        emit(doc.mac_address, {name: doc.name, service: doc.notification_service});
    }
}
