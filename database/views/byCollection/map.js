function(doc){
    if(doc.collection && doc.hasOwnProperty('hidden') === false){
        emit(doc.collection, doc);
    }
}
