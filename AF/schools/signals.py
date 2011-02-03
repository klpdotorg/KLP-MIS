from django.dispatch import Signal

check_perm = Signal(providing_args=["user", "instance", "Assessment", "permission"])	

check_user_perm = Signal(providing_args=["user", "model", "operation"])	

