from django.db import models

class Group(models.Model):
    mail = models.EmailField()
    note = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mail

class Invited(models.Model):
    first_name = models.CharField(max_length=250, blank=True)
    last_name = models.CharField(max_length=250, blank=True)
    menu = models.CharField(max_length=250, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="invites")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name