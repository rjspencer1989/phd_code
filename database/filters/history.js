function(doc, req){
    if (doc.collection === 'events' && doc._rev.indexOf('1-') === 0) {
        return true;
    }
}