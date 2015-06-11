function(doc, req){
    if(doc.collection === 'wifi' && doc.status === 'pending' && !doc.hasOwnProperty('hidden')){
        return true;
    }
    return false;
}
