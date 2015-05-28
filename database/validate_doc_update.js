function (newDoc, oldDoc, userCtx){
    function required(field, message /* optional */) {
        message = message || "Document must have a " + field;
        if (!newDoc.hasOwnProperty(field)) throw({forbidden : message});
    }

    function unchanged(field) {
        if (oldDoc && toJSON(oldDoc[field]) !== toJSON(newDoc[field])){
            throw({forbidden : "Field can't be changed: " + field});
        }
    }

    function is_valid_collection(){
        if(["wifi", "notifications", "devices", "events", "request_notification", "request_revert"].indexOf(newDoc.collection) === -1){
            throw({forbidden: "collection must be one of wifi, notifications, devices, events, request_notification, request_revert"});
        }
    }

    function empty_string(field) {
        if(newDoc[field] === ""){
            throw({forbidden : "Field can't be empty: " + field});
        }
    }

    function date_regex(field){
        //regex taken from https://code.google.com/p/jquery-localtime/issues/detail?id=4
        if (!newDoc[field].match(/^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[0-1]|0[1-9]|[1-2][0-9])T(2[0-3]|[0-1][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[0-1][0-9]):[0-5][0-9])?$/)) {
            throw({forbidden: "not a valid timestamp"});
        }
    }

    function email_regex(field){
        if (!newDoc[field].match(/^[a-zA_Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/)) {
            throw({forbidden: "not a valid email address " + newDoc[field]});
        }
    }

    if(!newDoc.hasOwnProperty('_deleted')){
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
            if(newDoc.mode !== "g"){
                throw({forbidden: "Mode must be g"});
            }

            required("channel");
            if(newDoc.channel < 1 || newDoc.channel > 11){
                throw({forbidden: "Channel must be a number from 1 to 11"});
            }

            required("encryption_type");
            if(newDoc.encryption_type !== "wep"){
                throw({forbidden: "Encryption Type must be wep"});
            }

            required("password_type");
            if(newDoc.password_type !== "txt" && newDoc.password_type !== "hex"){
                throw({forbidden: "Password Type must be txt or hex"});
            }

            required("password");

            if(newDoc.password_type === "txt"){
                if(newDoc.password.length !== 5 && newDoc.password.length !== 13){
                    throw({forbidden: "WEP passwords in TXT format must be 5 or 13 characters long"});
                }
            } else{
                if(newDoc.password.length !== 10 && newDoc.password.length !== 26){
                    throw({forbidden: "WEP passwords in HEX format must be 10 or 26 characters long"});
                }
                if(newDoc.password.search("^[0-9A-Fa-f]+$") == -1){
                    throw({forbidden: "WEP passwords in HEX format must have only 0-9 and A-F"});
                }
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
            required("connected");
            required("changed_by");
            if(newDoc.changed_by !== "system" && newDoc.changed_by !== "user"){
                throw({forbidden: "devices can only be changed by the system or a user"})
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
        } else if(newDoc.collection === "events"){
            required("collection");
            unchanged("collection");
            required("title");
            required("description");
            required("user");
            required("timestamp");
            required("doc_id");
            required("doc_rev");
            required("undoable");
            required("perform_undo");
            if(newDoc.undoable === false && newDoc.perform_undo === true){
                throw({forbidden: 'You can\'t undo an event that isn\'t undoable'});
            }
            date_regex('timestamp');
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
}
