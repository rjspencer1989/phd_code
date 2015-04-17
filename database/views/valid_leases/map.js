function(doc){
    if(doc.collection === 'devices' && doc.lease_action === 'add'){
        emit(doc.mac_address, doc.ip_address)
    }
}
