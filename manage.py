#!/usr/bin/env python
import os
import sys
from user_center.settings import development
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "user_center.settings.development")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
