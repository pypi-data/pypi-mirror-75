=====
Secret Parametrizer
=====

Stop saving your secrets in files and start parametrizing dynamically 
inside django admin.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "secret_parametrizer" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'secret_parametrizer',
    ]

2. Run ``python manage.py migrate`` to create the polls models.

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a param (you'll need the Admin app enabled).

4. Call your params inside your code just get the Queryset.