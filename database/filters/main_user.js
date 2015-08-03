function (doc, req) {
    if (doc.collection === 'main_user') {
        return true;
    }
    return false;
}