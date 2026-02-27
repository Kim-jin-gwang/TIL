from django.db import models
from django.contrib.auth.models import AbstractUser



# 추상 유저 모델을 상속받음
# 밑에 필드 추가해서 쓸 수 있음
# 근데 

class User(AbstractUser):
    pass
