from django.contrib import admin
from .models import Modalidade
from .models import Client
from .models import Driver
from .models import Boat
from .models import Instructor
from .models import Event
from .models import Gender
from .models import Profile
# Register your models here.

from .models import (
    Client
)

admin.site.register(Client)
admin.site.register(Modalidade)
admin.site.register(Driver)
admin.site.register(Boat)
admin.site.register(Instructor)
admin.site.register(Event)
admin.site.register(Gender)
admin.site.register(Profile)
