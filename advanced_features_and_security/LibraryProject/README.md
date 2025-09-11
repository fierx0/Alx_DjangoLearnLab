# Permissions & Groups Setup (advanced_features_and_security)

## Overview
Implements role-based access using custom permissions on `core.Article`:
- `can_view`, `can_create`, `can_edit`, `can_delete`

> Django still creates default `view/add/change/delete` perms; we enforce the **custom** ones above in views.

## Files
- `core/models.py`: defines `Article` + custom permissions in `Meta.permissions`.
- `core/admin.py`: registers `Article`.
- `core/management/commands/create_default_groups.py`: creates groups and assigns custom perms.
- `core/views.py`: shows both FBV and CBV enforcement using:
  - `@permission_required('core.can_*', raise_exception=True)`
  - `PermissionRequiredMixin` with `permission_required = 'core.can_*'`
- `core/urls.py`: routes for list/detail/create/edit/delete.
- Templates in `core/templates/core/`: minimal forms and pages.

## Groups
- **Viewers** → `can_view`
- **Editors** → `can_view`, `can_create`, `can_edit`
- **Admins** → `can_view`, `can_create`, `can_edit`, `can_delete`

## Commands
```bash
python manage.py makemigrations core
python manage.py migrate
python manage.py createsuperuser
python manage.py create_default_groups
python manage.py runserver
