function(doc, req){
    if(doc.collection === 'wifi' && !doc.hasOwnProperty('hidden')){
        return true;
    }
    return false;
}
