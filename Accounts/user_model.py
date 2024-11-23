from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    @property
    def is_user(self):
        return hasattr(self, 'userprofile')
    
    @property
    def is_mob(self):
        return hasattr(self, 'mobprofile')
    
    @property
    def is_customadmin(self):
        return hasattr(self, 'adminprofile')
