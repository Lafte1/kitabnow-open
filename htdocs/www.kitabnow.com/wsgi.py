import sys

project_home = '/home/kitabnow/htdocs/www.kitabnow.com/'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path


from main import app as application

if __name__ == "__main__":
    application.run()