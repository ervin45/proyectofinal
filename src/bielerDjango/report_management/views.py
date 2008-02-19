from models import ReportTemplate

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from pprint import pprint

def report_list(request):
    reports = ReportTemplate.objects.all()
    
    return render_to_response('report_list.html',locals())

def insert(request):
    return render_to_response('insert.html',locals())

def delete(request, id):
    report = ReportTemplate.objects.get(id=id)
    report.delete()
    
    return HttpResponseRedirect("/report/report_list/")
