from django.db import models


class tbl_user(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(unique=True)
    user_contact = models.CharField(max_length=15)
    user_password = models.CharField(max_length=100)
    user_photo = models.FileField(upload_to='User/', blank=True, null=True)
    user_status = models.IntegerField(default=1)

    def __str__(self):
        return self.user_name


class tbl_trainer(models.Model):
    trainer_name = models.CharField(max_length=100)
    trainer_email = models.EmailField(unique=True)
    trainer_password = models.CharField(max_length=100)
    trainer_status = models.IntegerField(default=0)

    def __str__(self):
        return self.trainer_name


class tbl_topic(models.Model):
    topic_name = models.CharField(max_length=100)
    topic_description = models.TextField()

    def __str__(self):
        return self.topic_name


class tbl_content(models.Model):
    CONTENT_TYPES = (
        ('Text', 'Text'),
        ('Video', 'Video'),
        ('Practical', 'Practical'),
    )
    topic = models.ForeignKey(tbl_topic, on_delete=models.CASCADE)
    content_title = models.CharField(max_length=100)
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES)
    content_file = models.FileField(upload_to='Content/', blank=True, null=True)

    def __str__(self):
        return self.content_title


class tbl_learningresult(models.Model):
    STYLE_CHOICES = (
        ('Text', 'Text Learner'),
        ('Video', 'Video Learner'),
        ('Practical', 'Practical Learner'),
    )
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    text_score = models.IntegerField()
    video_score = models.IntegerField()
    practical_score = models.IntegerField()
    final_style = models.CharField(max_length=50, choices=STYLE_CHOICES)


class tbl_assignment(models.Model):
    trainer = models.ForeignKey(tbl_trainer, on_delete=models.CASCADE)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)


class tbl_suggestion(models.Model):
    trainer = models.ForeignKey(tbl_trainer, on_delete=models.CASCADE)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    suggestion_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
