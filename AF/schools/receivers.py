from schools.models import *
def KLP_obj_Perm(sender, **kwargs):
	userObj = kwargs['user']
	instObj =  kwargs['instance']
	permission = kwargs['permission']
	assessmentObj = kwargs['Assessment']
	if (userObj.id != None or userObj.is_active)  and assessmentObj.active ==2:
		chkPerm = userObj.has_any_perms(instObj, perms=[permission])
	else:
		raise Exception("Insufficient Previliges")
	if not(userObj.is_superuser or userObj.is_staff or chkPerm):
		raise Exception("Insufficient Previliges")

		
def KLP_user_Perm(sender, **kwargs):
	userObj = kwargs['user']
	modelName = kwargs['model']
	operation = kwargs['operation']
	klp_UserGroups = userObj.groups.all()
	user_GroupsList = ['%s' %(str(usergroup.name)) for usergroup in klp_UserGroups]
	if userObj.id != None or userObj.is_active: 
		if userObj.is_superuser:
			pass
		elif 'AdminGroup' in user_GroupsList:
			if modelName != 'Users':
				raise Exception("Insufficient Previliges")
		elif userObj.is_staff:
			if modelName == 'Users':
				raise Exception("Insufficient Previliges")
		elif 'Data Entry Executive' in user_GroupsList:
			if modelName not in ['Institution', 'Staff', 'StudentGroup', 'Student', 'Answer']:
				raise Exception("Insufficient Previliges")
		elif 'Data Entry Operator' in user_GroupsList:
			if modelName not in ['Student', 'Answer']:
				raise Exception("Insufficient Previliges")
		else:
			raise Exception("Insufficient Previliges")
	else:
		raise Exception("Insufficient Previliges")	

def KLP_NewInst_Permission(sender, instance, created, **kwargs):
	if created:
		parentBoundary = instance.boundary
		inst_list = Institution.objects.filter(boundary=parentBoundary, active=2)
		users_List =  User.objects.filter(groups__name__in=['Data Entry Executive', 'Data Entry Operator'], is_active=1)
		lenInst = len(inst_list)
		for user in users_List:
			userPerm = []
			for inst in inst_list:
				userPerm.append(user.has_any_perms(inst, perms=['Acess']))
			lenTrue = userPerm.count(True)
			if lenTrue == lenInst - 1:
				user.set_perms(['Acess'], instance)		
