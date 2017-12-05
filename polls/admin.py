from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice


class MyAdminSite(admin.AdminSite):
    '''
    custom admin site
    '''
    site_header = 'Interstellar based Starfleet'

    def quicklogin(self,request):
        '''
        custom view
        login without authentication
        :param request:
        :return:
        '''
        from django.contrib.auth import login
        from django.contrib.auth.models import User
        user = User.objects.get(id=1)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return HttpResponseRedirect('/admin')

    def get_urls(self):
        '''
        add custom view url to urls
        :return:
        '''
        from django.conf.urls import url
        urls = super(MyAdminSite, self).get_urls()
        urls += [
           url(r'^quicklogin/', self.quicklogin, name='quicklogin'),
        ]
        return urls


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text'], 'description':'content of the question'}),
        ('Date information', {'fields': ['pub_date'],'classes' : ['collapse']}),
    ]
    inlines= [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text', 'pub_date']
    date_hierarchy = 'pub_date'
    list_per_page = 10

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Question, QuestionAdmin)
