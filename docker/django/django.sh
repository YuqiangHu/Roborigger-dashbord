python3 manage.py migrate

# Create superuser
FIRST="X"
LAST="X"
PASS="admintest!"
MAIL="admin@local.test"
script="
from django.contrib.auth import get_user_model
User = get_user_model()  # get the currently active user model,
first_name = '$FIRST'
last_name = '$LAST'
password = '$PASS'
email = '$MAIL'
if User.objects.filter(email=email).count()==0:
    user = User.objects.create_superuser(first_name, last_name, email, password)
    user.save()
    print('Superuser created.')
else:
    print('Superuser creation skipped.')
"
printf "$script" | python3 manage.py shell

python manage.py runserver 0.0.0.0:8000