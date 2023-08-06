==============================
SKYETECH GROUP USER MANAGEMENT
==============================

skyeusers is an app for managing users for skyetech backend api systems.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "skyeusers" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'skyeusers',
    ]

2. Include the skyeusers URLconf in your project urls.py like this::

    path('skyeusers/', include('skyeusers.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/skyeusers/
   to

5. Read the documentation for instructions on how to extend it and add new users, set random passwords, email users, add users roles and permission