from django.db.models import CharField, DateTimeField, Model, TextField


class OSV_Cache(Model):
    osv_id = CharField(max_length=255, unique=True)
    data = TextField()
    modified = DateTimeField()

    def __str__(self):
        return self.osv_id
