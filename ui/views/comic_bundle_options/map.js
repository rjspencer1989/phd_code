function(doc) {
  if(doc.setting_type === "comic_bundle_options"){
		emit(doc.row, {name: doc.name, value: doc.value});
	} 
}