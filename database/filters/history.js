function(doc, req){
    if (doc.collection === 'events') {
        return true;
    }
    return false;
}
