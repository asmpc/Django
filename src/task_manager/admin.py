from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from task_manager.models import Tasks, Tags, Projects, ProjectDetails, Comments, Attachments



# inline

class CommentInline(admin.TabularInline):
    model = Comments
    extra = 0

class TagInline(admin.TabularInline):
    model = Tags.tasks.through
    extra = 0
    verbose_name = 'Тэги'
    verbose_name_plural = verbose_name


class AttachmentInline(admin.TabularInline):
    model = Attachments
    extra = 0



# @admin.register(Tasks)
class TaskAdmin(admin.ModelAdmin):
    # fields = (('name', 'status',), 'description', 'priority', 'create_at',)

    fieldsets = [
        (
            None,
            {
                "fields": [('name', 'status',), 'description', 'priority'],
            },
        ),
                (
            "Дополнительные опции",
            {
                # "classes": ["collapse"],
                "fields": ['is_reopen','project', 'assignee'],
            },
        ),
        ("Служебные поля",
         {
            # "classes": ["collapse"],
            "fields": ("created_at", "updated_at", "comments_count",)
        }
         ),
    ]
    readonly_fields = ("created_at", "updated_at", "comments_count",)

    def comments_count(self, obj):
        return f"{obj.comments.count()} шт."
    comments_count.short_description = "Количество комментариев"

    inlines = (CommentInline, TagInline, AttachmentInline, )

    # список полей главной страницы
    list_display = ('name', 'status', 'priority', 'project', 'assignee', 'is_reopen', 'comments_list',) #"task_name_status",)

    # кастомное поле главной страницы
    # @admin.display(description="Наименование задачи и статус выполнения")
    # def task_name_status(self, obj):
    #     return f"{obj.name} - {obj.status}"

    # ссылка с каких полей
    list_display_links = ('name',)
    # редактируемые поля на главной странице
    list_editable = ('status', 'priority', 'is_reopen',)
    # показать все записи
    list_max_show_all = 10000
    # количество записей на странице
    list_per_page = 20
    # фильтр по полям
    list_filter = ('status', 'priority', 'assignee', 'project',)
    # поиск по полям (связанные сущности через __)
    search_fields = ('name', 'project__name', 'assignee__username',)
    # сортировка
    ordering = ('-priority', 'name',)
    # actions
    actions = ('make_completed', 'make_canceled', 'make_reopen', 'make_comment', 'make_admin',)

    @admin.display(description="Комментарии")
    def comments_list(self, obj):
        comments = obj.comments.all()
        if not comments.exists():
            return mark_safe("<p>Нет комментариев</p>")
        else:
            items = "".join(
                f"<li>{comment.message}</li>"
                for comment in comments
            )

        return mark_safe(f"<ul>{items}</ul>")

    @admin.action(description="Отметить задачи как завершенные.")
    def make_completed(self, request, queryset):
        queryset.update(status="completed")

    @admin.action(description="Отметить задачи как отмененные.")
    def make_canceled(self, request, queryset):
        queryset.update(status="canceled")

    @admin.action(description="Сбросить флаг переоткрытия задачи.")
    def make_reopen(self, request, queryset):
        queryset.update(is_reopen = False)

    @admin.action(description='Создать комментарий: “Processed by admin”.')
    def make_comment(self, request, queryset):
        for task in queryset:
            task.comments.get_or_create(message = 'Processed by admin', user = request.user)

    @admin.action(description='Назначить текущего пользователя исполнителем.')
    def make_admin(self, request, queryset):
        queryset.update(assignee=request.user)


# inline

class ProjectDetailInline(admin.StackedInline):
    model = ProjectDetails
    extra = 0



@admin.register(Projects)
class ProjectAdmin(admin.ModelAdmin):
    # fields = ('name', 'description',)
    exclude = ('owner', )
    list_display = ('name', 'owner',)
    list_editable = ('owner',)
    inlines = (ProjectDetailInline, )
    actions = ('make_admin',)

    @admin.action(description='Назначить текущего пользователя руководителем.')
    def make_admin(self, request, queryset):
        queryset.update(owner=request.user)


admin.site.register(Tasks,TaskAdmin)
admin.site.register(Tags)
# admin.site.register(Projects)
admin.site.register(ProjectDetails)
admin.site.register(Comments)
admin.site.register(Attachments)

# Register your models here.