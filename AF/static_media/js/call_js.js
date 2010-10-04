$("#treeBlk").click(function(){
 var topbranch = $("<li><span class='folder'>New Sublist</span></li>").appendTo("#treeBlk");

 $("#treeBlk").treeview({
  add: topbranch
 });
});
