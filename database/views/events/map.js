function(doc){
    if(doc.collection === "events"){
        emit(doc.timestamp, doc);
    }
}
