function(doc, req){
    if(doc.collection === 'notifications'){
        return true;
    }
    return false;
}
