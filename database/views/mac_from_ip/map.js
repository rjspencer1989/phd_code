function (doc) {
    if (doc.collection === "devices") {
        emit(doc.ip_address, doc.mac_address);
    }
}
