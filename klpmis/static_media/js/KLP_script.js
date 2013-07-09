/* This File Contains user defined JQuery functions */

/* KLP_Programme_List is used to get list of programmes on change of boundary type value */
var KLP_Programme_List = function(typVal){
	$.ajax({
		url: '/filter/'+typVal+'/programms/',
                success: function(data) {
			if (data != 'fail'){
		        	rows = data.split('&&')
		                selOption = '<option value="None">--</option>'
		                for (i=0;i<rows.length;i++){
		                	vals = rows[i].split('$$')
		                	selOption += "<option value="+vals[0]+">"+vals[1]+"</option>"
		        	}
		                $("#filtProg").html(selOption);
		        }
                 }
        });

}


var KLP_ChangeFilter = function(){
	$("#treeStruc").html('<ul id="treeBlk" class="filetree treeview-famfamfam"></ul>');
}

var KLP_TreeBLK = function(treeUrl){
	$("#treeBlk").treeview({
		url: treeUrl,
	});
}

/* Edit the the asessement lookup edit*/
var KLP_EditEvent2=function(){

        lookupId=$(this).attr('id');
                
                valueTDObj=$('#'+lookupId+'_value');
                desTDObj=$('#'+lookupId+'_des');
                CurObj=$(this);
                Curhtml=CurObj.html();
                if(Curhtml=='Edit'){
                
                
                valueTDObj.html('<input type="text" value="'+valueTDObj.html()+'" id="'+lookupId+'_valueinput" name="'+lookupId+'_value">');
                desTDObj.html('<input type="text" value="'+desTDObj.html()+'" id="'+lookupId+'_desinput" name="'+lookupId+'_des">');
                CurObj.html('Save');
                }
                else{
                $.post(
                "/assessment_lookup_value/inlineedit/",
                'lookupId='+lookupId+'&name='+$('#'+lookupId+'_valueinput').val()+'&des='+$('#'+lookupId+'_desinput').val(),
                function(data){ 
                        
                        $("#"+lookupId+'_status').html(data);
                        $("#"+lookupId+'_status').show();
                        if(data=='Data Saved'){
                           valueTDObj.html($('#'+lookupId+'_valueinput').val())
                           desTDObj.html($('#'+lookupId+'_desinput').val());
                           }
                         
                CurObj.html('Edit');
                
                });
                
                }
        return false;
}


/* KLP_Set_Session is used to change or set session value, on change of boundary type value */
var KLP_Set_Session = function(typVal){
	$.ajax({
		url: '/set/session/',
                data:'sessionVal='+typVal,
                success: function(data) {
			return false;
                }
        });
}


/* This method shows an error, if reponse has any error. The error is shown based on status of reponse*/
$.ajaxSetup({
	error:function(x,e){
		if(x.status==0){
			$("#failureMsgHead").show();
   		    	$("#klp_fail_MsgTxt").html("You are offline!! Please Check Your Network.");
		}else if(x.status==404){
			$("#failureMsgHead").show();
   		    	$("#klp_fail_MsgTxt").html("Requested URL not found.");
		}else if(x.status==500){
			$("#failureMsgHead").show();
			//respTxt = x.responseText;
			//var exceptionVal = $(".exception_value", respTxt).html(); 
			$("#klp_fail_MsgTxt").html("Invalid data or insufficient priviliges");
		}else if(e=='parsererror'){
			$("#failureMsgHead").show();
   		    	$("#klp_fail_MsgTxt").html("Error.\nParsing JSON Request failed.");
		}else if(e=='timeout'){
			$("#failureMsgHead").show();
   		    	$("#klp_fail_MsgTxt").html("Request Time out.");
		}else {
			$("#failureMsgHead").show();
   		    	//$("#klp_fail_MsgTxt").html("Unknow Error.\n"+x.responseText);
   		    	$("#klp_fail_MsgTxt").html("Invalid data or insufficient priviliges");
		}
	}
});


/* KLP_Del method is used to call common delete method, to delete boundary, institution, sg, programme, assessment and question */
var KLP_Del = function(referKey,type, msgText){
	KLP_Hide_Msg();
	if (type.toLowerCase()=='class' || type.toLowerCase()=='center')
        	nodeId = $("#studentgroup_"+referKey) 
        else
                nodeId = $("#"+type+'_'+referKey)  
        if (type=='assessmentdetail')
                msgType = 'question'
        else
                msgType = type
        var conf = confirm("Are you sure, you want to delete "+msgType +' '+msgText);
        if (conf==true){                                
                $.ajax({                    
                	url: '/delete/'+type+'/'+referKey+'/',
                	success: function(data) {
				if(data.match(/Successfully Deleted/g)){
				        nodeId.remove();
				    }
                                 if(type=='staff'){
                                                  $("#staff_"+referKey).remove();
                                        }
                                 else{
				$("#dyncData").html("");
                                      //nodeId.remove();
                                            }
				$("#klp_MsgTxt").html(data);
				$("#successMsgHead").show();
                    }
                });
        }
}
        
var KLP_Boundary_Add = function(thisObj){
	KLP_Hide_Msg();
	currentId=$(thisObj).attr('id');
	addId=currentId.split('_')[0];
	$.ajax({
            url: $(thisObj).attr('href'),
            success: function(data) {
                $("#dyncData").html(data); 
		NFInit();
		$('input:visible:enabled:first').focus();
                $('#id_form-0-parent').val(addId);
                if ($(thisObj).attr('boundaryCategory')){
			$("#id_form-0-boundary_category").val($(thisObj).attr('boundaryCategory'));
		}
            }
        });
	return false;
}

/* KLP_view method is used to show view on clicking on nodes in tree or clicking add or edit buttons */
var KLP_View = function(thisObj){
	$("body").append("<div id='TB_load'><img src='/static_media/images/loadingAnimation.gif'></div>");
	$('#TB_load').show();
	$.ajax({
        	url: thisObj.href,
        	success: function(data) {
        		KLP_Hide_Msg();
        		$("#dyncData").html(data);
        		var asEntryVal = $("#id_entry_view").val();
        		if (asEntryVal == 'True'){
        			$(".KLP_Button_Header").hide();
        		}
			NFInit();
			$('input:visible:enabled:first').focus();
	        	tb_init('a.thickbox, area.thickbox, input.thickbox');
	        	$("#subForm").html('');
	        	//$.validationEngine.closePrompt(".formError",true);
	        	if ($(thisObj).attr('boundaryCategory')){
			        $("#id_form-0-boundary_category").val($(thisObj).attr('boundaryCategory'));
	        	}
	        	currentObj = $(thisObj)
	        	KLP_BredaCrumb(currentObj);
            	}
        });
        $('#TB_load').remove();
	return false;
}

/* KLP_Hide_Msg is used to hide success or failure messages*/
var KLP_Hide_Msg = function(){
	$("#successMsgHead").hide();
        $("#failureMsgHead").hide();
}

/* KLP_Create_Node is used to create new node in tree, on creation of new boundary, institution, sg, programme, assessment and question */
var KLP_Create_Node = function(thisObj,ObjValue){
	currentId=thisObj;
	ccid = currentId.attr('id');
	ObjValues=ObjValue.split('_');
	ObjValue=ObjValues[0];
        if (typeof ccid=='undefined' ){
        	currentId=$('#treeBlk');
                ObjValue='boundary';
                ObjId = $('#'+ObjValue+'_id').val();
	}
        else{
        	ObjId = $('#'+ObjValue+'_id').val();
        }
        syncflag=true;
        if (ObjValues.length==2){
        
          syncflag=false;
        }  
	newChildId = ObjValue+'_'+$('#'+ObjValue+'_id').val();
	$.ajax({
		url: '/createnew/'+ObjValue+'/'+ObjId+'/',
                        async:syncflag,
            	data: 'boundaryType='+$("#boundary_type").val(),
            	success: function(data) {
            		curentHtml=currentId.html();
		     	curId = currentId.attr('id');
		      	Ulhas=$("#"+curId).is(":has(>ul)")     
                      	if (curId=='treeBlk'){
                      		var topbranch = $("<li id="+newChildId+" >"+data+"</li>").appendTo("#"+curId);
                      	}
                      	else if (Ulhas){
				 var topbranch = $("<li id='"+newChildId+"' class='last'>"+data+"</li>").appendTo("#"+curId +' >ul:first');
			}
			else{
				addStr='<div class="hitarea hasChildren-hitarea collapsable-hitarea"></div>'
				$("#"+curId).prepend(addStr)
                                var topbranch = $("<ul style='display: block;'><li id='"+newChildId+"' class='collapsable'>"+data+"</li></ul>").appendTo("#"+curId);
                                
                                $("#"+curId).filter(":not(:has(>a))").find(">span").click(function(event) {
						KLP_toggler($(this).parent());
			        }).add( $("a", $("#"+curId)) ).hoverClass();
                                
                                
                                $("#"+curId).find("div:first").click( function(event){
                                	KLP_toggler($(this).parent());
                                });
		       }
		       
                       $("#"+curId).treeview({
                       		add: topbranch,
                       });
                       if(ObjValues.length!=2){
                       var newNode = $('#'+newChildId).find("a:first");
		       KLP_BredaCrumb(newNode);
		       }
                       return false;
		        
		}
	});
}


var KLP_toggler = function(thisObj) {
	
	thisObj
		// swap classes for hitarea
		.find(">.hitarea")
			.swapClass( "collapsable-hitarea", "expandable-hitarea" )
			.swapClass( "lastCollapsable-hitarea", "lastExpandable-hitarea" )
		.end()
		// swap classes for parent li
		.swapClass( "collapsable", "expandable" )
		.swapClass( "lastCollapsable", "lastExpandable" )
		// find child lists
		.find( ">ul" )
		// toggle them
		e1=thisObj.addClass("selected");
		data = $(e1).is(":has(>ul:first:visible)") ? 0 : 1;
		$(e1).find(">ul:first")[ parseInt(data) ? "show" : "hide" ]();
}

/* KLP_BreadCrumb is used to show the breadcrumb on clicking on tree node */
var KLP_BredaCrumb = function(currentObj){
	var isParent =false;
	var thisClass = $(currentObj).attr('class');
	if (thisClass && thisClass != "KLP_Button"){
		var prvSel = $("#id_prvSelNode").val();
		if (prvSel){
			prvAnc = $('#'+prvSel).find('a:first');
			$(prvAnc).removeClass("KLP_selNode");			
			$(prvAnc).addClass("KLP_treetxt");
		}
		$(currentObj).removeClass("KLP_treetxt");
		$(currentObj).addClass("KLP_selNode");
		$("#id_prvSelNode").val($(currentObj).parent().parent().attr("id"));
				
       		var thisTitle = "<span class=KLP_BreadCrumbTxt> "+$(currentObj).attr('title')+" </span>";
       		do{
       			isParent = $(currentObj).parent().parent().parent().parent().is(':has(>span>a)');
       			if (isParent){
       				currentObj = $(currentObj).parent().parent().parent().parent().find('a:first');
       				thisTitle = "<span class=KLP_BreadCrumbTxt> "+$(currentObj).attr("title") +" </span>  >  " + thisTitle
       			}
       		}while(isParent)
       		$("#custom_BreadCrumb").html(thisTitle);
	}
}

/* KLP_validateScript is used to validate answer data on submiting the form */
var KLP_validateScript=function(formId){
 	$('#'+formId).validate({
      		submitHandler: function(){
      			$("body").append("<div id='KLP_overlay' class='KLP_overlayBG'></div>");
			$("#KLP_overlay").show();
      			$("#"+formId+"_submit").hide();
      			formName = formId;
	             	form=$('#'+formName)
	             	count = 0
	             	$("#successMsgHead").hide();
        		$("#failureMsgHead").hide();
        		var txtFields = $(form).find("input[type=text]:visible");
        	        DeFlag=false		
                        
       			txtFields.each(function(index){
       				isDE = $(this).attr("dE");
       				tempAt = "#"+$(this).attr("id");
       				if (isDE == "true"){
       				        DeFlag=true;
       					$(this).attr("remote", "/answer/data/validation/");
       					count = count + 1
       					form.validate().element(tempAt);
       				}
       				
       			});
                        if ($(txtFields[0]).attr('id').indexOf('primaryvalue')!=-1)
                                txtlength=txtFields.length-1
                        else
                              txtlength=txtFields.length
       			if ( DeFlag==true && count == txtlength){ 
       			    errLength = $(form).children().find('label.error:visible').length
                            //alert(errLength);
       			    if (errLength == 0){
			   		KLP_post_script(form,formName)
			    }
			    else{
			    	$("#"+formId+"_submit").show();
			    }		
	       		   }
	       		else{
	       		       KLP_post_script(form,formName)
	       		       $("#"+formId+"_submit").show();
	       		}
	       		
    		}	
      });

}

/* KLP_post_script is used to post answers data */
var KLP_post_script=function(form,formName){
	$.post(
		"/answer/data/entry/",
		$(form).serialize(),
		function(data){	
			statusObj=$("#"+formName).find('#formcounter');
			//$("#id_Student"+statusObj.val()+"_status").html(data);
			//$("#id_Student"+statusObj.val()+"_status").show();
                        successData=data.split('|');
			$("#id_Student_"+$("#"+formName).find('#formcounter').val()+"_status").html(successData[0]);
                        //set the saved ansId
                        if (successData.length==2){
                         ansObjs=$("#"+formName).find('.ansIds');
                         ansVals=successData[1].split(',');
                         $.each(ansObjs,function(index,val ){
                                $(this).val(ansVals[index]);
                         })  

                       }  
			$("#id_Student_"+$("#"+formName).find('#formcounter').val()+"_status").show();
			var txtFields = $(form).find("input[type=text]:visible");
			txtFields.each(function(index){
       				isSE = $(this).attr("sE");
       				if (isSE == "true"){
       					$(this).attr("disabled", "true");
       					$("#"+formName+"_submit").show()
       					$("#"+formName+"_submit").attr("disabled", "true");
       				}
       			}); 
       			 
		}
	);    

}

/* KLP_isLog is used to check user authentication*/
var KLP_isLog = function(){
	$.ajax({
		url: '/user/authentication',
		success: function(data){
			if (data == 'False'){
				window.location.href="/"
				return false;
			}
			return true;
		}
	});
}

