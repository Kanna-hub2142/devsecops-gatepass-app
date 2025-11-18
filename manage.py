#!/usr/bin/env python3
import os
import sys

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gatepass_project.settings')

    from django.core.management import execute_from_command_line

    # IMPORTANT:
    # Auto-create superuser only when running server
    if 'runserver' in sys.argv:
        # Make sure database is migrated first
        execute_from_command_line(['manage.py', 'migrate'])
        # Call auto superuser creation command
        execute_from_command_line(['manage.py', 'createsu'])

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
