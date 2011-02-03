from django.core.management.base import BaseCommand, CommandError
from schools.models import *
#import datetime

class Command(BaseCommand):
	#args = '<inst_id inst_id ...>'
	#help = 'Students Promoting to Next Year'
	
	def handle(self, *args, **options):
		try:
			fileName = args[0]
			assessment_id = args[1]
			if fileName and assessment_id:
				mapFile = open(fileName, 'r')
				studenGroups = mapFile.read().replace('\n', '')
				mapFile.close()
				sgList = studenGroups.split(',')
				assessmentObj = Assessment.objects.get(id=assessment_id)
				for sg in sgList:
					sgObj = StudentGroup.objects.get(id=sg)
					mapObj = Assessment_StudentGroup_Association(assessment = assessmentObj, student_group=sgObj, active=2)
					mapObj.save()
					self.stdout.write('%s - Assessment and StudentGroup - %s%s are Mapped ...\n'%(assessmentObj.name, sgObj.name, sgObj.section))
		except IndexError:
			raise CommandError('Pass FileName and Assessment Id\n')
