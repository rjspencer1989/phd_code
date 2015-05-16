function doc(doc, req){
    if(doc.collection === "events" /*&& doc.perform_undo === true && doc.undoable === true*/){
        return true;
    }
    return false;
}
