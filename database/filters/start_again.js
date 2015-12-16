function(doc, req){
    if(doc.collection === "reset"){
        return true;
    }
    return false;
}