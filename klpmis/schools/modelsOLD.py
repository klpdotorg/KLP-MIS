#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models


    # Table Structure For Klp

class School_Category(models.Model):

    name = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % self.name


School_Types = ['boys', 'girls', 'co-ed']
School_Type = []
for school in School_Types:
    type_school = (school, school)
    School_Type.append(type_school)

Sex = ['male', 'female']
Gender = []
for gender in Sex:
    genders = (gender, gender)
    Gender.append(genders)


class Moi_Type(models.Model):

    name = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % self.name


class School_Management(models.Model):

    name = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % self.name


Questions = ['text', 'numeric', 'radio']
Question_Type = []
for question in Questions:
    QuestionType = (question, question)
    Question_Type.append(QuestionType)


class Sections(models.Model):

    '''This Sections stores the Section types'''

    name = models.CharField(max_length=1)

    def __unicode__(self):
        return '%s' % self.name


class Boundary_Type(models.Model):

    '''This Class stores the Boundary Type'''

    boundary_type = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s' % self.boundary_type


class Boundary(models.Model):

    '''This class specifies the longitude and latitute of the area'''

    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=300)
    boundary_type = models.ForeignKey(Boundary_Type, blank=True,
            null=True)
    geo_code = models.CharField(max_length=300)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s' % self.name


class Address(models.Model):

    '''This class stores the address of all the schools'''

    address = models.CharField(max_length=1000)
    landmark = models.CharField(max_length=1000, blank=True, null=True)
    pin = models.CharField(max_length=1000, blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.address


class School(models.Model):

    ''' It stores the all data regarding schools'''

    boundary = models.ForeignKey(Boundary)
    address = models.ForeignKey(Address, blank=True, null=True)
    dise_code = models.CharField(max_length=14, blank=True, null=True)
    name = models.CharField(max_length=300)
    cat = models.ForeignKey(School_Category, blank=True, null=True)
    school_type = models.CharField(max_length=10, choices=School_Type,
                                   default='co-ed')
    languages = models.ManyToManyField(Moi_Type, default='kannada')
    mgmt = models.ForeignKey(School_Management, default='ed')
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return '%s' % self.name


class Child(models.Model):

    ''' This class stores the personnel information of the childrens'''

    name = models.CharField(max_length=300)
    dob = models.DateField(max_length=20, blank=True, null=True)
    sex = models.CharField(max_length=10, choices=Gender, default='male'
                           )
    mt = models.ForeignKey(Moi_Type, default='kannada')

    def __unicode__(self):
        return '%s' % self.name


class Class(models.Model):

    ''' Here it holds the informaion of the class and section of the schools'''

    sid = models.ForeignKey(School)
    name = models.IntegerField()
    section = models.ManyToManyField(Sections, blank=True, null=True)

    def __unicode__(self):
        return '%s' % self.name


class Academic_Year(models.Model):

    ''' Its stores the academic years information'''

    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class student(models.Model):

    ''' This class gives information regarding the students class , academic year and personnel details'''

    clid = models.ForeignKey(Class)
    child = models.ForeignKey(Child)
    academic = models.ForeignKey(Academic_Year)

    def __unicode__(self):
        return '%s---->%s---->%s' % (self.child, self.clid,
                self.academic)


