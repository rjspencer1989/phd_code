function(doc, req){
    if(doc.collection === 'notifications' && doc.status === 'pending'){
        return true;
    }
    return false;
}
