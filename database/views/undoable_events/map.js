function(doc){
    if(doc.collection === "events" && doc.undoable === true){
        emit(doc.timestamp, doc);
    }
}
