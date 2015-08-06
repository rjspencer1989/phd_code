function (doc, req) {
    if (doc.collection === 'main_user' && doc.status === 'pending') {
        return true;
    }
    return false;
}