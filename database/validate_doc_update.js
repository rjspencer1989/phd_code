function (newDoc, oldDoc, userCtx){
    function required(field, message /* optional */) {
        message = message || "Document must have a " + field;
        if (!newDoc.hasOwnProperty(field)) throw({forbidden : message});
    }

    function required_array_object(arr, field, message){
        message = message || arr + " must have objects with a " + field + " field.";
        newDoc[arr].forEach(function(item){
            if(!item.hasOwnProperty(field)){
                throw({forbidden: message});
            }
        });
    }

    function unchanged(field) {
        if (oldDoc && toJSON(oldDoc[field]) !== toJSON(newDoc[field])){
            throw({forbidden : "Field can't be changed: " + field});
        }
    }

    function is_valid_collection(){
        if(["wifi", "notifications", "devices", "events", "request_notification", "request_revert", "main_user", "connection_state", "dns"].indexOf(newDoc.collection) === -1){
            throw({forbidden: "collection must be one of wifi, notifications, devices, events, request_notification, request_revert, main_user, connection_state", "dns"});
        }
    }

    function empty_string(field) {
        if(newDoc[field] === ""){
            throw({forbidden : "Field can't be empty: " + field});
        }
    }

    function email_regex(field){
        if (!newDoc[field].match(/^[a-zA_Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/)) {
            throw({forbidden: "not a valid email address " + newDoc[field]});
        }
    }

    function date_regex(field){
        //regex taken from https://code.google.com/p/jquery-localtime/issues/detail?id=4
        rg="^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[0-1]|0[1-9]|[1-2][0-9])T(2[0-3]|[0-1][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[0-1][0-9]):[0-5][0-9])?$";
        if (!newDoc[field].match(new RegExp(rg))) {
            throw({forbidden: "not a valid timestamp"});
        }
    }

    function mac_address_regex(field){
        rg="^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$";
        if (!newDoc[field].match(new RegExp(rg))) {
            throw({forbidden: "not a valid mac address"});
        }
    }

    required("collection");
    is_valid_collection();

    if(newDoc.collection === "wifi"){
        required("status");
        if(newDoc.status != "done"){
            if(newDoc.status != "pending"){
                if(newDoc.status != "error"){
                    throw({forbidden: "Status must be one of done, pending, or error"});
                }
            }
        }

        required("ssid");
        if(newDoc.ssid.length < 1 || newDoc.ssid.length > 32){
            throw({forbidden: "SSID is required and must not be longer than 32 characters"});
        }

        required("mode");
        if(newDoc.mode !== "g" && newDoc.mode !== "n"){
            throw({forbidden: "Mode must be g or n"});
        }

        required("channel");
        if(newDoc.channel < 1 || newDoc.channel > 11){
            throw({forbidden: "Channel must be a number from 1 to 11"});
        }

        required("encryption_type");
        if(newDoc.encryption_type !== "wpa"){
            throw({forbidden: "Encryption Type must be wpa"});
        }

        required("password");
        if(newDoc.password.search("^[\x20-\x7e]{8,63}$") == -1){
            throw({forbidden: "WPA passwords must be 8-63 characters long"});
        }
    } else if (newDoc.collection === "notifications") {
        required("name");
        unchanged("name");
        required("service");
        unchanged("service");
        unchanged("collection");
        required("user");
        required("status");
        if(newDoc.status !== "done"){
            if(newDoc.status !== "pending"){
                if(newDoc.status !== "error"){
                    throw({forbidden: "Status must be one of done, pending, or error"});
                }
            }
        }
        if (newDoc['service'] === 'email') {
            email_regex('user');
        }
    } else if(newDoc.collection === "devices"){
        required("action");
        required("device_name");
        required("host_name");
        required("ip_address");
        required("lease_action");
        required("mac_address");
        required("name");
        required("state");
        required("device_type");
        required("notification_service");
        required("timestamp");
        unchanged("hostname");
        unchanged("ip_address");
        unchanged("mac_address");
        unchanged("collection");
        required("connection_event");
        if (newDoc.connection_event !== "connect" && newDoc.connection_event !== "disconnect") {
            throw({forbidden: "devices can either connect or disconnect"});
        }
        required("changed_by");
        if(newDoc.changed_by !== "system" && newDoc.changed_by !== "user" && newDoc.changed_by !== "connected_devices"){
            throw({forbidden: "devices can only be changed by the system or a user or to update connnected devices"});
        }
        if(newDoc.lease_action !== "add" && newDoc.lease_action !== "del"){
            throw({forbidden: "you can only add or del leases"});
        }

        if(newDoc.action !== "permit" && newDoc.action !== "deny" && newDoc.action !== ""){
            throw({forbidden: 'you can only permit or deny devices'});
        }

        if(newDoc.state !== "pending" && newDoc.state !== "permit" && newDoc.state !== "deny"){
            throw({forbidden: 'state must be pending, permit, or deny'});
        }

        empty_string('mac_address');
        empty_string('ip_address');
        mac_address_regex('mac_address');

        if(newDoc.action === "" && (newDoc.name.length > 0 || newDoc.device_name.length > 0 || newDoc.device_type.length > 0 || newDoc.notification_service.length > 0) && newDoc.changed_by === "user" && newDoc.state === "pending"){
            throw({forbidden: "Device details cannot be changed when a device is pending, without also permitting or denying the device"});
        }

    } else if(newDoc.collection === "events"){
        required("collection");
        unchanged("collection");
        required("title");
        required("description");
        required("timestamp");
        required("undoable");
        required("perform_undo");
        required("docs");

        required_array_object("docs", "doc_id");
        required_array_object("docs", "doc_rev");
        required_array_object("docs", "action");
        required_array_object("docs", "doc_collection");

        if(newDoc.undoable === false && newDoc.perform_undo === true){
            throw({forbidden: 'You can\'t undo an event that isn\'t undoable'});
        }
        date_regex('timestamp');
        if(newDoc.undoable === false && newDoc.prompt){
            throw({forbidden: "prompt should only be used if undoable is true"});
        }
    } else if(newDoc.collection === "request_notification"){
        required("collection");
        unchanged("collection");
        required("to");
        required("service");
        required("status");
        required("body");

        if(newDoc.status !== "pending" && newDoc.status !== "done" && newDoc.status !== "error"){
            throw({forbidden: "Status must be one of done, pending, or error"});
        }

        empty_string("to");
        empty_string("body");
        empty_string("service");
    } else if (newDoc.collection === "request_revert") {
        required("collection");
        unchanged("collection");
        required("timestamp");
        empty_string("timestamp");
        required('status');
        if(newDoc.status !== "pending" && newDoc.status !== "done" && newDoc.status !== "error"){
            throw({forbidden: "Status must be one of done, pending, or error"});
        }
        date_regex('timestamp');
    }
}
