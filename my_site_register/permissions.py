from functools import wraps
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.shortcuts import redirect

User = get_user_model()

ROLE_PERMISSION_MAP = {
    'Admin': [
        'my_site_app.view_processor',
        'my_site_app.add_processor',
        'my_site_app.change_processor',
        'my_site_app.delete_processor',
        'my_site_app.view_gpu',
        'my_site_app.add_gpu',
        'my_site_app.change_gpu',
        'my_site_app.delete_gpu',
        'my_site_app.view_ram',
        'my_site_app.add_ram',
        'my_site_app.change_ram',
        'my_site_app.delete_ram',
        'my_site_app.view_motherboard',
        'my_site_app.add_motherboard',
        'my_site_app.change_motherboard',
        'my_site_app.delete_motherboard',
        'my_site_app.view_storage',
        'my_site_app.add_storage',
        'my_site_app.change_storage',
        'my_site_app.delete_storage',
        'my_site_app.view_powersupply',
        'my_site_app.add_powersupply',
        'my_site_app.change_powersupply',
        'my_site_app.delete_powersupply',
        'my_site_app.view_case',
        'my_site_app.add_case',
        'my_site_app.change_case',
        'my_site_app.delete_case',
        'my_site_app.view_laptop',
        'my_site_app.add_laptop',
        'my_site_app.change_laptop',
        'my_site_app.delete_laptop',
        'orders.view_order',
        'orders.change_order',
        'reviews.view_review',
        'reviews.change_review',
        'reviews.delete_review',
    ],
    'User': [
        'my_site_app.view_processor',
        'my_site_app.view_gpu',
        'my_site_app.view_ram',
        'my_site_app.view_motherboard',
        'my_site_app.view_storage',
        'my_site_app.view_powersupply',
        'my_site_app.view_case',
        'my_site_app.view_laptop',
        'configurator.add_pcconfiguration',
        'configurator.view_pcconfiguration',
        'configurator.change_pcconfiguration',
        'configurator.delete_pcconfiguration',
        'orders.add_order',
        'orders.view_order',
        'reviews.add_review',
        'reviews.view_review',
        'my_site_app.add_wishlist',
        'my_site_app.view_wishlist',
        'my_site_app.delete_wishlist',
    ],
}

def get_logged_in_user(request):
    if hasattr(request, 'current_user'):
        return request.current_user

    user = request.user

    if not user.is_authenticated:
        request.current_user = None
        return None

    request.current_user = (
        User.objects.filter(pk=user.pk)
        .prefetch_related(
            'groups',
            'groups__permissions__content_type',
            'user_permissions__content_type',
        )
        .first()
    )
    return request.current_user


def assign_role(user, role_name, replace_existing=False):
    role, _ = Group.objects.get_or_create(name=role_name)

    if replace_existing:
        user.groups.set([role])
    else:
        user.groups.add(role)

    return role


def sync_roles_and_permissions():
    for role_name, permission_names in ROLE_PERMISSION_MAP.items():
        role, _ = Group.objects.get_or_create(name=role_name)

        codenames = []
        app_labels = []
        for permission_name in permission_names:
            parts = permission_name.split('.', 1)
            app_labels.append(parts[0])
            codenames.append(parts[1])

        permissions = Permission.objects.filter(
            content_type__app_label__in=app_labels,
            codename__in=codenames,
        ).distinct()

        role.permissions.set(permissions)

    user_role = Group.objects.get(name='User')
    for user in User.objects.filter(groups__isnull=True).distinct():
        user.groups.add(user_role)


def build_permission_flags(user):
    if not user:
        return {
            'role_names': [],
            'permission_codes': [],
            'is_admin': False,
            'can_manage_products': False,
            'can_manage_orders': False,
            'can_create_configuration': False,
        }

    return {
        'role_names': [g.name for g in user.groups.all()],
        'permission_codes': sorted(user.get_all_permissions()),
        'is_admin': user.groups.filter(name='Admin').exists(),
        'can_manage_products': user.has_perm('my_site_app.add_processor'),
        'can_manage_orders': user.has_perm('orders.change_order'),
        'can_create_configuration': user.has_perm('configurator.add_pcconfiguration'),
    }


def session_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = get_logged_in_user(request)

        if not user:
            messages.error(request, 'Please log in first.')
            return redirect('login')

        return view_func(request, *args, **kwargs)

    return wrapper


def permission_required(permission_name):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = get_logged_in_user(request)

            if not user:
                messages.error(request, 'First you need to log in')
                return redirect('login')

            if not user.has_perm(permission_name):
                messages.error(request, 'You dont have permission to do this')
                return redirect('home')

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def role_required(*role_names):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = get_logged_in_user(request)

            if not user:
                messages.error(request, 'First you need to log in')
                return redirect('login')

            user_roles = [g.name for g in user.groups.all()]
            if not any(role in user_roles for role in role_names):
                messages.error(request, 'You dont have role to do this')
                return redirect('home')

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = get_logged_in_user(request)

        if not user:
            messages.error(request, 'First you need to log in')
            return redirect('login')

        if not user.is_staff and not user.groups.filter(name='Admin').exists():
            messages.error(request, 'Admin access required')
            return redirect('home')

        return view_func(request, *args, **kwargs)

    return wrapper
