function(doc) {
  	if(doc.setting_type === "comic_bundle_options" && doc._attachments){
  		var name = doc._id + "/" + Object.keys(doc._attachments)[0];
		emit(doc.row, {image: name, alt: doc.name});
	} 
}