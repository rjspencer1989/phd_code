function (newDoc, oldDoc, userCtx){
    function required(field, message /* optional */) {
        message = message || "Document must have a " + field;
        if (!newDoc[field]) throw({forbidden : message});
    }

    function unchanged(field) {
        if (oldDoc && toJSON(oldDoc[field]) !== toJSON(newDoc[field]))
          throw({forbidden : "Field can't be changed: " + field});
    }

    function user_is(role) {
        return userCtx.roles.indexOf(role) >= 0;
    }

    required("collection");

    if(newDoc.collection == "wifi"){
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
        if(newDoc.mode !== "n" && newDoc.mode !== "g"){
            throw({forbidden: "Mode must be n or g"});
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

        if(newDoc.encryption_type === "wep"){
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
        }

    } else if (newDoc.collection === "notification") {
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
        if(newDoc.lease_action !== "add" && newDoc.lease_action !== "del"){
            throw({forbidden: "you can only add or del leases"});
        }

        if(newDoc.action !== "permit" && newDoc.action !== "deny"){
            throw({forbidden: 'you can only permit or deny devices'});
        }

        if(newDoc.state !== "pending" && newDoc.state !== "permit" && newDoc.state !== "deny"){
            throw({forbidden: 'state must be pending, permit, or deny'});
        }
    }
}
