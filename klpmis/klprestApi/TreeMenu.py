#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
TreeMenu is used to filter all objects to genrate tree menu
"""
from django.contrib.auth.models import *
from django.conf.urls.defaults import *
from django_restapi.model_resource import Collection
from django_restapi.responder import *
from schools.models import *
from django.http import *
from klprestApi.Treeresponder import *
from django.db.models.query import QuerySet
from django.db import transaction
asstable = {2: Assessment_StudentGroup_Association,
            3: Assessment_Class_Association,
            1: Assessment_Institution_Association}


def hasChild(
    query,
    typ,
    boundaryType,
    filterBy,
    secFilter,
    permFilter,
    assessmentPerm,
    shPerm,
    userSel,
    request,
    showflag,
    ):
    """ This method checks for child objects and get urls """

    subboundary = 0
    childtree = 0
    childDic = {}
    AlreadyAdded={}
    for i in query:
        if typ == 'source' or typ == 'boundary':
            if permFilter:
                templist = [i.getPermissionChild(boundaryType),
                            i.getPermissionViewUrl()]
            elif assessmentPerm:
                templist = [i.getPermissionChild(boundaryType),
                            i.getAssessmentPermissionViewUrl(secFilter[0])]
            elif shPerm:
                templist = [i.getPermissionChild(boundaryType),
                            i.showPermissionViewUrl(userSel)]
            else:
                templist = [i.getChild(boundaryType),
                            i.getViewUrl(boundaryType)]
        elif typ == 'institution' and filterBy not in [None, ' ', 'None'
                ] and permFilter in ['', ' ', None]:
            templist = []
            for secFil in secFilter:
                Assobj = Assessment.objects.filter(id=secFil)[0]
                Asstype = int(Assobj.typ)
                logUser = request.user
                klp_UserGroups = logUser.groups.all()
                user_GroupsList = ['%s' % usergroup.name
                                   for usergroup in klp_UserGroups]

                if logUser.is_superuser or logUser.is_staff \
                    or 'AdminGroup' in user_GroupsList:
                    assemenperm = True
                else:
                    insObj = StudentGroup.objects.filter(id=i.id,
                            active=2)[0].institution
                    permObj = \
                        UserAssessmentPermissions.objects.filter(user__id=logUser.id,
                            instituion=insObj,
                            assessment=Assobj).defer('user',
                            'assessment', 'instituion')

                         # print permObj  ,'*********',insObj

                    if permObj:
                        assemenperm = True
                    else:
                        assemenperm = False
                if assemenperm:
                    hasC = i.getChild()
                    mapObj = ''
                    if Asstype == 3:
                        mapObj = \
                            Assessment_StudentGroup_Association.objects.filter(assessment__id=secFil,
                                student_group=i,
                                active=2).defer('assessment',
                                'student_group')
                    elif Asstype == 2:
                        mapObj = \
                            Assessment_Class_Association.objects.filter(assessment__id=secFil,
                                student_group=i,
                                active=2).defer('assessment',
                                'student_group')
                    else:
                        Instlist1 = \
                            StudentGroup.objects.filter(id=i.id,
                                active=2).defer('institution')
                        Instlist = \
                            Instlist1.values_list('institution_id',
                                flat=True).distinct()
                        mapObj = \
                            Assessment_Institution_Association.objects.filter(assessment__id=secFil,
                                institution__in=Instlist,
                                active=2).defer('institution',
                                'assessment')
                        hasC = False
                        if Instlist[0] not in AlreadyAdded.get(secFil,[]) :
									existingList=AlreadyAdded.get(secFil,[])
									existingList.append(Instlist[0])
									AlreadyAdded[secFil]=existingList
                        else:
									mapObj=''         


                    if mapObj:
                        templist.append([i.getChild(),
                                i.getStudentProgrammeUrl(filterBy,
                                secFil)])
        else:

            
            templist = [i.getChild(), i.getViewUrl()]
        try:
            templist.append(i.GetName())
        except:
            pass

        childDic[i.getModuleName() + '_' + str(i.id)] = templist

    return childDic


def KLP_assignedInstitutions(userId):
    """ This method returns assigned institutions for the user"""

    rawQuerySet = \
        Institution.objects.raw(""" SELECT "id","obj_id" FROM "public"."object_permissions_institution_perms" WHERE "user_id" = '%s' AND "Acess" = 1 """
                                 % userId)
    inst_list = []
    for permObj in rawQuerySet:
        inst_list.append(permObj.obj_id)
    return inst_list


def KLP_assignedAssessmentInst(userId, assessmentId):
    """ This method returns assigned Assessments for the user"""

    inst_list = \
        UserAssessmentPermissions.objects.filter(user__id=userId,
            assessment__id__in=assessmentId, access=True).defer('user',
            'assessment', 'instituion').values_list('instituion__id',
            flat=True).distinct()
    return inst_list


def TreeClass(request):
    model = request.GET['root']
    data = request.GET['home']
    filterBy = request.GET['filter']
    secFilter = request.GET['secFilter']
    logUser = request.user
    klp_UserGroups = logUser.groups.all()
    user_GroupsList = ['%s' % usergroup.name for usergroup in
                       klp_UserGroups]
    showflag = (logUser.is_superuser or logUser.is_staff or 'AdminGroup'
                 in user_GroupsList) and filterBy != 'None'
    if filterBy != 'None' and secFilter != 'None':
        seclist = [secFilter]
        secFilter = seclist
    if secFilter == 'None' and filterBy != 'None':
        secFilter = GetAssementList(filterBy, logUser, showflag)

    boundaryType = request.GET['boundTyp']
    permFilter = request.GET.get('permission')
    assessmentPerm = request.GET.get('assesspermission')
    shPerm = request.GET.get('shPerm')
    userSel = request.GET.get('userSel')
    model = model.split('_')
    typ = model[0]

     # logUser = request.user
     # klp_UserGroups = logUser.groups.all().defer('user','permissions')
     # user_GroupsList = ['%s' %(usergroup.name) for usergroup in klp_UserGroups]

    if typ == 'source':

         # if type is source

        if data:

        # if home is true query for boundaries........

            if (logUser.is_superuser or logUser.is_staff or 'AdminGroup'
                 in user_GroupsList) and filterBy == 'None':

            # if logged in user is super user or staff or in AdminGroup and filterBy is none query all active boundary's where parent is 1 and based on boundaryType

                query = Boundary.objects.filter(parent__id=1, active=2,
                        boundary_type=boundaryType).defer('boundary'
                        ).order_by('name'
                                   ).extra(select={'lower_name': 'lower(name)'
                        }).order_by('lower_name')
            else:
                if logUser.is_superuser or logUser.is_staff \
                    or 'AdminGroup' in user_GroupsList:

                # if logged in user is super user or staff or in AdminGroup and filterBy is not none query all active SG's based on assessments

            
                    institutions_list = getAssInst(secFilter)
                elif filterBy == 'None':

                        # print institutions_list....,'INSSSSSSS'....................
                # studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id__in=secFilter, active=2).values_list('student_group', flat=True).distinct()
                # Query institutions based SG's
                # institutions_list = StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution__id', flat=True).distinct()
                # if user is not superuser and not staff and not related to admin group and filterby is none get all assigned institutions.

                    institutions_list = \
                        KLP_assignedInstitutions(logUser.id)
                else:

                # else query for institutions based on map Sg's
                # studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id__in=secFilter, active=2).values_list('student_group', flat=True).distinct()

                    map_institutions_list = getAssInst(secFilter)  # StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution__id', flat=True).distinct()
            
                    institutions_list = list(set(map_institutions_list)
                            & set(KLP_assignedAssessmentInst(logUser.id,
                            secFilter)))
                try:
                    boundary_list = \
                        Boundary.objects.filter(institution__pk__in=institutions_list,
                            active=2,
                            boundary_type=boundaryType).defer('boundary'
                            ).values_list('parent__parent__id',
                            flat=True).distinct()
            
                except:
            
                    boundary_list = \
                        Boundary.objects.filter(institution__pk__in=institutions_list,
                            active=2,
                            boundary_type=boundaryType).defer('boundary'
                            ).values_list('parent__id',
                            flat=True).distinct()
            
                query = Boundary.objects.filter(pk__in=boundary_list,
                        active=2, parent__id=1).defer('boundary'
                        ).distinct().extra(select={'lower_name': 'lower(name)'
                        }).order_by('lower_name')
        else:

        # if data is not true query for all active programmes.

            query = Programme.objects.filter(active=2,
                    programme_institution_category=boundaryType).extra(select={'lower_name': 'lower(name)'
                    }).order_by('-start_date', '-end_date', 'lower_name')
            typ = 'programme'
    else:

         # typ is not source

        if typ == 'boundary':

        # if typ is boundary Query for sub boundaries or Institutions

            if (logUser.is_superuser or logUser.is_staff or 'AdminGroup'
                 in user_GroupsList) and filterBy == 'None':

            # if logged in user is super user or staff or in AdminGroup and filterBy is none query all active boundary's where parent is 1 and based on boundaryType

                query = Boundary.objects.filter(parent__id=model[1],
                        active=2,
                        boundary_type=boundaryType).defer('boundary'
                        ).extra(select={'lower_name': 'lower(name)'
                                }).order_by('lower_name')
            else:
                if logUser.is_superuser or logUser.is_staff \
                    or 'AdminGroup' in user_GroupsList:

                # if logged in user is super user or staff or in AdminGroup and filterBy is not none query all active SG's based on assessments
                # studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id__in=secFilter, active=2).values_list('student_group', flat=True).distinct()
                # Query institutions based SG's

                    institutions_list = getAssInst(secFilter)  # StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution_id', flat=True).distinct()
                elif filterBy == 'None':

                # if user is not superuser and not staff and not related to admin group and filterby is none get all assigned institutions.

                    institutions_list = \
                        KLP_assignedInstitutions(logUser.id)
                else:

                # else query for institutions based on map Sg's
                # studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id__in=secFilter, active=2).values_list('student_group', flat=True).distinct()

                    map_institutions_list = getAssInst(secFilter)  # StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution_id', flat=True).distinct()
                    institutions_list = list(set(map_institutions_list)
                            & set(KLP_assignedAssessmentInst(logUser.id,
                            secFilter)))

                parentBoundary = Boundary.objects.get(id=model[1])
                if parentBoundary.boundary_category.boundary_category \
                    in ['district']:

                # Query for Boundaries based on institutions

                    boundary_list = \
                        Boundary.objects.filter(institution__pk__in=institutions_list,
                            active=2,
                            boundary_type=boundaryType).defer('boundary'
                            ).values_list('parent',
                            flat=True).distinct()
                    query = \
                        Boundary.objects.filter(parent__id=model[1],
                            pk__in=boundary_list, active=2,
                            boundary_type=boundaryType).defer('boundary'
                            ).distinct().extra(select={'lower_name': 'lower(name)'
                            }).order_by('lower_name')
                else:
                    boundaries = \
                        Boundary.objects.filter(parent__id=model[1],
                            institution__pk__in=institutions_list,
                            active=2,
                            boundary_type=boundaryType).defer('boundary'
                            ).values_list('id', flat=True).distinct()
                    query = \
                        Boundary.objects.filter(id__in=boundaries).defer('boundary'
                            ).extra(select={'lower_name': 'lower(name)'
                                    }).order_by('lower_name')

            if not query:

            # If Query is Empty Query for Institutions under boundary

                if (logUser.is_superuser or logUser.is_staff
                    or 'AdminGroup' in user_GroupsList) and filterBy \
                    == 'None':

                # if logged in user is super user or staff or in AdminGroup and filterBy is none query all active institutions's based on boundary

                    query = \
                        Institution.objects.filter(boundary__id=model[1],
                            active=2).extra(select={'lower_name': 'lower(name)'
                            }).order_by('lower_name')
                    typ = 'sch'
                else:
                    if logUser.is_superuser or logUser.is_staff \
                        or 'AdminGroup' in user_GroupsList:

                    # if logged in user is super user or staff or in AdminGroup and filterBy is not none query all active SG's based on assessments
                    # studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id__in=secFilter, active=2).values_list('student_group', flat=True).distinct()

                        institutions_list = getAssInst(secFilter)  # StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution_id', flat=True).distinct()
                    elif filterBy == 'None':

                    # if user is not superuser and not staff and not related to admin group and filterby is none get all assigned institutions.

                        institutions_list = \
                            KLP_assignedInstitutions(logUser.id)
                    else:

                    # else query for institutions based on map Sg's
                    # studentgroup_list = Assessment_StudentGroup_Association.objects.filter(assessment__id__in=secFilter, active=2).values_list('student_group', flat=True).distinct()

                        map_institutions_list = getAssInst(secFilter)  # StudentGroup.objects.filter(id__in=studentgroup_list, active=2).values_list('institution_id', flat=True).distinct()
                        institutions_list = \
                            list(set(map_institutions_list)
                                 & set(KLP_assignedAssessmentInst(logUser.id,
                                 secFilter)))

                    query = \
                        Institution.objects.filter(pk__in=institutions_list,
                            boundary__id=model[1],
                            active=2).distinct().extra(select={'lower_name': 'lower(name)'
                            }).order_by('lower_name')
                    typ = 'sch'
        elif typ == 'programme':
        
        # if typ is programme Query For active assessment based On programme id

            activelist = [1, 2]
            userobj = User.objects.get(id=request.user.id)
            if showflag:

                activelist = [1, 2 ]
            if userobj.is_superuser:
                query = Assessment.objects.filter(programme__id=model[1],
                    active__in=activelist)
            else:
                query = Assessment.objects.filter(programme__id=model[1],
                    active=2)
        elif typ == 'assessment':

        # if typ is assessment Query For active Questions based On assessment id

            query = Question.objects.filter(assessment__id=model[1],
                    active=2)
        else:
            if typ == 'institution':
            
            
            # if typ is Institution Query For active Sgs

                if filterBy != 'None':
            

                    studentgroup_list = getAssSG(secFilter, model[1])

                                # print studentgroup_list

                    if int(boundaryType) == 1:
                        query = \
                            StudentGroup.objects.filter(institution__id=model[1],
                                active=2,
                                id__in=studentgroup_list).distinct().extra(select={'lower_class': 'CAST(name as INT)'
                                }).order_by('lower_class', 'section')
                    else:

                        query = \
                            StudentGroup.objects.filter(institution__id=model[1],
                                active=2,
                                id__in=studentgroup_list).distinct().extra(select={'lower_class': 'lower(name)'
                                }).order_by('lower_class', 'section')
                else:
                    if int(boundaryType) == 1:
                        query = \
                            StudentGroup.objects.filter(institution__id=model[1],
                                active=2).extra(select={'lower_class': 'CAST (name as INT)'
                                }).order_by('lower_class', 'section')
                    else:

                        query = \
                            StudentGroup.objects.filter(institution__id=model[1],
                                active=2).extra(select={'lower_class': 'lower (name)'
                                }).order_by('lower_class', 'section')

    CDict = hasChild(  # Checking for child objects
        query,
        typ,
        boundaryType,
        filterBy,
        secFilter,
        permFilter,
        assessmentPerm,
        shPerm,
        userSel,
        request,
        showflag,
        )
    val = Collection(queryset=query,
                     responder=TreeResponder(CDict=CDict))
    return HttpResponse(val(request), mimetype='application/json')


asstable = {3: Assessment_StudentGroup_Association,
            2: Assessment_Class_Association,
            1: Assessment_Institution_Association}
selectfield = {2: 'student_group_id', 3: 'student_group__id',
               1: 'institution__id'}


def getAssInst(secFilter, superuser=1):
    flag = 0
    institutions_listall = []
    for k in secFilter:
        assobj = Assessment.objects.get(id=k)
        asstype = assobj.typ
        
        studentgroup_list = \
            asstable[asstype].objects.filter(assessment=assobj,
                active=2).values_list(selectfield[asstype],
                flat=True).distinct()

            # Query institutions based SG's

        if asstype in [2, 3]:
            institutions_list = \
                StudentGroup.objects.filter(id__in=studentgroup_list,
                    active=2).values_list('institution__id',
                    flat=True).distinct()
        else:
            flag = 1
            institutions_list = studentgroup_list
        institutions_listall = list(set(institutions_listall)
                                    | set(institutions_list))
    return institutions_listall


def getAssSG(secFilter, instid):
    flag = 0
    sg_listall = []
    sg = StudentGroup.objects.filter(institution__id=instid,
            active=2).values_list('id', flat=True).distinct()
    for k in secFilter:
        assobj = Assessment.objects.get(id=k)
        asstype = assobj.typ

                # Query institutions based SG's

        if asstype in [2, 3]:
            studentgroup_list = \
                asstable[asstype].objects.filter(assessment=assobj,
                    student_group__id__in=sg).values_list('student_group__id'
                    , flat=True).distinct()
            sg_list = \
                StudentGroup.objects.filter(id__in=studentgroup_list,
                    active=2).defer('institution').values_list('id',
                    flat=True).distinct()
        else:
            if sg:
                sg_list = [sg[0]]

        sg_listall = list(set(sg_listall) | set(sg_list))
    return sg_listall


def GetAssementList(programId,loguser,showflag=False):
    activelist = [2]

    userobj = ''
    if showflag:
        try:
            userobj = User.objects.get(id=loguser.id)
        except:
            pass
        
        if userobj and userobj.is_superuser: 
            activelist = [1, 2]
        else:
            activelist = [2]
    return Assessment.objects.filter(programme__id=programId,
            active__in=activelist).values_list('id', flat=True)


urlpatterns = patterns('', url(r'^tree/$', TreeClass))

