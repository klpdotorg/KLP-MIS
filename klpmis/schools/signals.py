"""This File Contains the Signal definations. These signals are used
 to check permissions of user """

from django.dispatch import Signal

check_perm = Signal(providing_args=["user", "instance", "Assessment",
<<<<<<< HEAD:klp/schools/signals.py
"permission"])  # This Signal used to check user object level permissions
=======
"permission"])	# This Signal used to check user object level permissions
>>>>>>> c4fe4887ceb637424ee30c8a3353d73c856997d4:klpmis/schools/signals.py

check_user_perm = Signal(providing_args=["user", "model", "operation"])
# This Signal used to check user operational permissions
#(add/update/delete permissions)
