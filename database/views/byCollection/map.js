function(doc){
    if(doc.collection && !doc.hasOwnProperty('hidden')){
        emit(doc.collection, doc);
    }
}
