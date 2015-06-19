function(doc, req){
    if(doc.collection === 'notifications' && doc.hasOwnProperty('hidden') === false){
        return true;
    }
    return false;
}
