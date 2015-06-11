function(doc, req){
    if(doc.collection === 'notifications' && doc.status === 'pending' && !doc.hasOwnProperty('hidden')){
        return true;
    }
    return false;
}
