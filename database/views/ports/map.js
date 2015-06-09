function(doc) {
  if(doc.collection === "devices"){
    emit(doc.port, doc.mac_address);
  }
}
