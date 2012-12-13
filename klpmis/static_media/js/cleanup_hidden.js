function Cleanuphidden(idnames){
idnames=idnames.split(',');
for(k=0;k<idnames.length;k++){ 
  $('#'+idnames[k]).keyup(function() {
	changeId=$(this).attr('id');
	$("#id_"+changeId).val('');
});

}
}
