""" This file containd the receivers definations. Once Signal get call the respective receiver will get execute """

from schools.models import *
def KLP_obj_Perm(sender, **kwargs):
	""" This receiver method is used to check user object level permissions """
	""" Get user, instance(Instituion), assessment objects to check permissions"""
	userObj = kwargs['user']
	instObj =  kwargs['instance']
	permission = kwargs['permission']
	assessmentObj = kwargs['Assessment']
	# Check user is logged in or not if logged in check user is active user or not and check assessment object state is active(2)
	if (userObj.id != None or userObj.is_active)  and assessmentObj.active ==2:
		# If true check user has permissions to access intitution object
		chkPerm = userObj.has_any_perms(instObj, perms=[permission])
	else:
		# else raise Insufficient Previliges exception
		raise Exception("Insufficient Previliges")
	if not(userObj.is_superuser or userObj.is_staff or chkPerm):
		# If user is not super user and he is not in staff and user doesn't has permission with intitution object raise Insufficient Previliges exception
		raise Exception("Insufficient Previliges")

		
def KLP_user_Perm(sender, **kwargs):
	""" This receiver method is used to check user operational permissions based on model """
	""" Get User, model name and operation(Add/update/delete) to check permissions"""
	userObj = kwargs['user']
	modelName = kwargs['model']
	operation = kwargs['operation']
	# get user groups 
	klp_UserGroups = userObj.groups.all()
	user_GroupsList = ['%s' %(str(usergroup.name)) for usergroup in klp_UserGroups]
	# check logged in user is active user or not
	if userObj.is_active: 		
		if userObj.is_superuser:
			# if user is super user allow all the operations
			pass
		elif 'AdminGroup' in user_GroupsList:
			# if user in admin group allow to add/update/delete users and pemissions
			if modelName != 'Users':
				raise Exception("Insufficient Previliges")
		elif userObj.is_staff:
			# if user is in staff allow to access all models other than users
			if modelName == 'Users':
				raise Exception("Insufficient Previliges")
		elif 'Data Entry Executive' in user_GroupsList:
			# if user in Data Entry Executive group allow to access 'Institution', 'Staff', 'StudentGroup', 'Student' and 'Answer' models
			if modelName not in ['Institution', 'Staff', 'StudentGroup', 'Student', 'Answer']:
				raise Exception("Insufficient Previliges")
		elif 'Data Entry Operator' in user_GroupsList:
			# if user in Data Entry Operator group allow to access 'Student' and 'Answer' models
			if modelName not in ['Student', 'Answer']:
				raise Exception("Insufficient Previliges")
		else:
			# if user not in any of the group and not staff and not super user then raise Insufficient Previliges exception
			raise Exception("Insufficient Previliges")
	else:
		# if user is not active user raise Insufficient Previliges exception
		raise Exception("Insufficient Previliges")	

def KLP_NewInst_Permission(sender, instance, created, **kwargs):
	""" This receiver method is used to assign permissions to users on new institution creation"""
	# Check institution is creating or editing.
	if created:	
		# If new institution is creating get parent boundary of institution
		parentBoundary = instance.boundary
		# Get all instititons under boundary to check permissions
		inst_list = Institution.objects.filter(boundary=parentBoundary, active=2)
		# get all active users in Data Entry Executive and Data Entry Operator group
		users_List =  User.objects.filter(groups__name__in=['Data Entry Executive', 'Data Entry Operator'], is_active=1)
		# get count of institutions under boundary
		lenInst = inst_list.count()
		for user in users_List:
			userPerm = []
			for inst in inst_list:
				# check user permission with institutions under boundary
				userPerm.append(user.has_any_perms(inst, perms=['Acess']))
			lenTrue = userPerm.count(True) # get count of instituions where user has permission
			if lenTrue == lenInst - 1:
				# if user has permission with all institutions under boundary except newly created institution, set permissions to user for new institution also
				user.set_perms(['Acess'], instance)		
