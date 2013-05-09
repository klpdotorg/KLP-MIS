#!/usr/bin/python
# -*- coding: utf-8 -*-

""" This file containd the methods  and receiver methods to check the user permissions and to assign permission on new institution creation"""


def KLP_obj_Perm(
    userObj,
    instObj,
    permission,
    assessmentObj,
    ):
    """ This method is used to check user object level permissions """

    from schools.models import UserAssessmentPermissions

    # Check user is logged in or not if logged in, check user is active user or not

    if userObj.id is not None or userObj.is_active:

        # If true check user has permissions to access intitution and assessment object

        chkPerm = False
        userAsmList = \
            UserAssessmentPermissions.objects.filter(user=userObj,
                instituion=instObj, assessment=assessmentObj).values()
        if userAsmList:
            chkPerm = userAsmList[0].get('access') or False
    else:

        # else raise Insufficient Previliges exception

        raise Exception('Insufficient Previliges')
    if not (userObj.is_superuser or userObj.is_staff or chkPerm):

        # If user is not super user and he is not in staff and user doesn't has permission with intitution object raise Insufficient Previliges exception

        raise Exception('Insufficient Previliges')


def KLP_user_Perm(userObj, modelName, operation):
    """ This method is used to check user operational permissions based on model """

    # get user groups

    klp_UserGroups = userObj.groups.all()
    user_GroupsList = ['%s' % str(usergroup.name) for usergroup in
                       klp_UserGroups]

    # check logged in user is active user or not

    if userObj.is_active:
        if userObj.is_superuser:

            # if user is super user allow all the operations

            pass
        elif 'AdminGroup' in user_GroupsList:

            # if user in admin group allow to add/update/delete users and pemissions

            if modelName != 'Users':
                raise Exception('Insufficient Previliges')
        elif userObj.is_staff:

            # if user is in staff allow to access all models other than users

            if modelName == 'Users':
                raise Exception('Insufficient Previliges')
        elif 'Data Entry Executive' in user_GroupsList:

            # if user in Data Entry Executive group allow to access 'Institution', 'Staff', 'StudentGroup', 'Student' and 'Answer' models

            if modelName.lower() not in ['institution', 'staff',
                    'studentgroup', 'student', 'answer']:
                raise Exception('Insufficient Previliges')
        elif 'Data Entry Operator' in user_GroupsList:

            # if user in Data Entry Operator group allow to access 'Student' and 'Answer' models

            if modelName.lower() not in ['student', 'answer']:
                raise Exception('Insufficient Previliges')
        else:

            # if user not in any of the group and not staff and not super user then raise Insufficient Previliges exception

            raise Exception('Insufficient Previliges')
    else:

        # if user is not active user raise Insufficient Previliges exception

        raise Exception('Insufficient Previliges')


def KLP_NewInst_Permission(
    sender,
    instance,
    created,
    **kwargs
    ):
    """ This receiver method is used to assign permissions to users on new institution creation"""

    # Check institution is creating or editing.

    if created:
        from schools.models import Institution
        from django.contrib.auth.models import User

        # If new institution is creating get parent boundary of institution

        parentBoundary = instance.boundary

        # Get all instititons under boundary to check permissions

        inst_list = Institution.objects.filter(boundary=parentBoundary,
                active=2)

        # get all active users in Data Entry Executive and Data Entry Operator group

        users_List = \
            User.objects.filter(groups__name__in=['Data Entry Executive'
                                , 'Data Entry Operator'], is_active=1)

        # get count of institutions under boundary

        lenInst = inst_list.count()
        for user in users_List:
            userPerm = []
            for inst in inst_list:

                # check user permission with institutions under boundary

                userPerm.append(user.has_any_perms(inst, perms=['Acess'
                                ]))
            lenTrue = userPerm.count(True)  # get count of instituions where user has permission
            if lenTrue == lenInst - 1:

                # if user has permission with all institutions under boundary except newly created institution, set permissions to user for new institution also

                user.set_perms(['Acess'], instance)


