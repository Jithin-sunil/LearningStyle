from django.contrib import admin
from .models import (
    tbl_assignment,
    tbl_content,
    tbl_learningresult,
    tbl_suggestion,
    tbl_topic,
    tbl_trainer,
    tbl_user,
)

admin.site.register(tbl_user)
admin.site.register(tbl_trainer)
admin.site.register(tbl_topic)
admin.site.register(tbl_content)
admin.site.register(tbl_learningresult)
admin.site.register(tbl_assignment)
admin.site.register(tbl_suggestion)
