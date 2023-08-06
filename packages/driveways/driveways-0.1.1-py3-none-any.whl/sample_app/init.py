
#!/usr/bin/env python

import os

import sys




def main():

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drive.settings')

    try:

        from django.core.management import execute_from_command_line

    except ImportError as exc:

        raise ImportError("Couldn't import Django.") from exc



if __name__ == '__main__':

    main()