function (doc) {
    if (doc.collection === "devices") {
        emit(doc.ip_address, {'mac_address': doc.mac_address});
    }
}
