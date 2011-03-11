
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


var KLP_Set_Session = function(typVal){
	$.ajax({
		url: '/set/session/',
                data:'sessionVal='+typVal,
                success: function(data) {
			return false;
                }
        });
}


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
				nodeId.remove();
				$("#dyncData").html("");
				$("#klp_MsgTxt").html(" Sucessfully deleted "+msgType+'  '+msgText);
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


var KLP_Hide_Msg = function(){
	$("#successMsgHead").hide();
        $("#failureMsgHead").hide();
}


var KLP_Create_Node = function(thisObj,ObjValue){
	currentId=thisObj;
	ccid = currentId.attr('id');
        if (typeof ccid=='undefined' ){
        	currentId=$('#treeBlk');
                ObjValue='boundary';
                ObjId = $('#'+ObjValue+'_id').val();
	}
        else{
        	ObjId = $('#'+ObjValue+'_id').val();
        }
	newChildId = (ObjValue+'_'+$('#'+ObjValue+'_id').val());
	$.ajax({
		url: '/createnew/'+ObjValue+'/'+ObjId+'/',
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
                       
                       var newNode = $('#'+newChildId).find("a:first");
		       KLP_BredaCrumb(newNode);
		       
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


var KLP_validateScript=function(formId){
 	$('#'+formId).validate({
      		submitHandler: function(){
      			formName = formId;
	             	form=$('#'+formName)
        		var txtFields = $(form).find("input[type=text]:visible");
        	        DeFlag=false		
       			txtFields.each(function(index){
       				isDE = $(this).attr("dE");
       				
       				if (isDE == "true"){
       				        DeFlag=true;
       					$(this).attr("remote", "/answer/data/validation/");
       				}
       			});
       			if (DeFlag){ 
       			    $(form).valid();
       			
       			    $(form).submit(function(){
       				KLP_post_script(form,formName)
	       			
	       		       });
	       		   }
	       		else
	       		       KLP_post_script(form,formName)
	       		
    		}	
      });

}


var KLP_post_script=function(form,formName){
	$.post(
		"/answer/data/entry/",
		$(form).serialize(),
		function(data){	
			$("#"+formName+"_status").html(data);
			$("#"+formName+"_status").show();
			var txtFields = $(form).find("input[type=text]:visible");
			txtFields.each(function(index){
       				isSE = $(this).attr("sE");
       				if (isSE == "true"){
       					$(this).attr("disabled", "true");
       				}
       			});   
		}
	);    

}


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

