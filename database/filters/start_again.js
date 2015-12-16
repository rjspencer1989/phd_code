function(doc, req){
    if(doc.collection === "reset" && doc['_rev'].startswith("1-")){
        return true;
    }
    return false;
}