$("#boundary_2").click(function(){
 var topbranch = $("<li><span class='folder'>New Sublist</span></li>").appendTo("#boundary_2");

 $("#boundary_2").treeview({
  add: topbranch
 });
});
