function (newDoc, oldDoc, userCtx) {
    if (userCtx.roles.indexOf('_admin') === -1) {
        throw({forbidden: 'need to be an admin to change the ui'});
    }
}
