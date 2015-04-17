function(doc) {
  if(doc.collection === "devices"){
    emit(doc.mac_address, doc);
  }
}
