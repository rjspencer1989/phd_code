function(doc) {
  if(doc.collection === "devices"){
    emit(doc.connection_event, doc);
  }
}
