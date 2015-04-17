function(doc, req){
    if(doc.collection === 'wifi' && doc.status === 'pending'){
        return true;
    }
    return false;
}
