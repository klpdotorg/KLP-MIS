function autoCompleteCall(url,FieldNames,multiSelects,databaseSelects,extraParam){
if (extraParam =='1')
    extValue = $("#id_class_section").val();
else
    extValue = 0
    
databaseSelects=databaseSelects.split(',')
multiSelects=multiSelects.split(',')
FieldNames=FieldNames.split(',')
  for(i=0;i<FieldNames.length;i++){
    FieldName=FieldNames[i]; 
       
    mutiVal = false
    if (multiSelects[i]=='true' || multiSelects[i]=='True')
        mutiVal = true                    
	$("#"+FieldName).autocomplete(url, {
		width: 300,
		
		multiple: mutiVal,
		mustMatch: true,
		matchContains: true,
		//formatItem: formatItem,
		formatResult: formatResult,
		extraParams: { 'fieldName':FieldName,'Database':databaseSelects[i],'extraPram':extValue},
	});
	$("#"+FieldName).result(function(event, data, formatted) {		
		hiddenId=$(this).attr('id');		
		var hidden = $("#id_"+hiddenId);
		if (mutiVal){		   
		    $("#id_"+hiddenId).append($('<option selected="True"></option>').val(data[1]).html(data[0]));
		}
		else{
		    //hidden.val( (hidden.val() ? hidden.val() + "," : hidden.val()) +data[1]);		    
		    if (data)
		        hidden.val(data[1]);
		}		
	});

}

}
function formatItem(row) {
		return row[0] + " (<strong>id: " + row[1] + "</strong>)";
	}
	function formatResult(row) {
		return row[0].replace(/(<.+?>)/gi, '');
	}
