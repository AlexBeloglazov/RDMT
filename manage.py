#!/usr/bin/env python
import os
import sys
from os.path import abspath, dirname, join

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rdtm.settings")
    PROJECT_ROOT = abspath(dirname(__file__))
    apps_dir = join(PROJECT_ROOT, 'src', 'apps')
    if apps_dir not in sys.path:
        sys.path.append(apps_dir)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
