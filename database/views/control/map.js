function(doc) {
  if(doc.collection === "devices"){
    emit(doc.connected, doc);
  }
}
