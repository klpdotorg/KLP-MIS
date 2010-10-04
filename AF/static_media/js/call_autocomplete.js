function autoCompleteCall(url,FieldNames,multiSelects,databaseSelects){
var myArray = new Array();
databaseSelects=databaseSelects.split(',')
multiSelects=multiSelects.split(',')
FieldNames=FieldNames.split(',')
  for(i=0;i<FieldNames.length;i++){
    FieldName=FieldNames[i];
           options = { serviceUrl:url,
   
           minChars:1,

   delimiter: /(,|;)\s*/, // regex or character
   maxHeight:400,
   width:300,
   zIndex: 9999,
   onSelect: function(fieldName,value, data){  $('#'+fieldName).val(data) },
   deferRequestBy: 0, //miliseconds
   params: { 'fieldName':FieldName,'Database':databaseSelects[i]}, //aditional parameters
   noCache: false, //default is false, set to true to disable caching
   multiple:false,
 };
 myArray[i] = $('#'+FieldName).autocomplete(options);
 
 }
}
