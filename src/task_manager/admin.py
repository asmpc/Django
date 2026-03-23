from django.contrib import admin
from account.models import User
from task_manager.models import Tasks, Tags, Projects, ProjectDetails, Comments, Attachments


admin.site.register(User)
admin.site.register(Tasks)
admin.site.register(Tags)
admin.site.register(Projects)
admin.site.register(ProjectDetails)
admin.site.register(Comments)
admin.site.register(Attachments)

# Register your models here.