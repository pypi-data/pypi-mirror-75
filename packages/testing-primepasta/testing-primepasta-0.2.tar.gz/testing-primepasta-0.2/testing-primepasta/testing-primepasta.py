import subprocess
from keyboard import press
import time

def execute(command, shouldPrint = True):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    if shouldPrint:
        for line in p.stdout.readlines():
            print(line)
        retval = p.wait()

def herokuLogin():
    execute("heroku login", False)
    time.sleep(5)
    press('enter')

def djangoDeploy(projectName, appName = ''):
    #Execute the pip freeze command to create a requirements.txt file.
    execute("pip freeze > requirements.txt")

    #Create a Procfile file and add the required line.
    with open("Procfile", "w") as f:
            f.write(f"web: gunicorn {projectName}.wsgi")

    #Create a runtime.txt file and add the required line.
    with open("runtime.txt", "w") as f:
            f.write("python-3.7.7")
    
    #Create a heroku app.
    p = subprocess.Popen(f"heroku create {appName}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    #Extract the name of the heroku app by taking the last line that heroku gives, which includes the website that the app should be on.    
    line = str(p.stdout.readlines()[-1])[10:]

    appName = ""
    for letter in line:
        if letter == '.':
            break
        appName += letter 

    lst = []

    #Make the required changes to the settings.py file. This is done by converting the whole file into a list, each element of the list, each element of the list being a line in the file.
    with open(f"{projectName}/settings.py", "r") as f:
        lst = list(f)

    #If one of the lines that we're about to add is not in the file, then we'll go ahead and make the required changes.
    #This if statement is only to ensure that if the user runs this function twice, there won't be two copies of the following lines in the file.
    if 'import django_heroku\n' not in lst:
        index = 0

        while index < len(lst):
            if lst[index].rstrip() == 'import os':
                lst.insert(index+1, 'import django_heroku\n')
            elif lst[index].rstrip() == 'MIDDLEWARE = [':
                lst.insert(index+1, "'whitenoise.middleware.WhiteNoiseMiddleware',\n")
            index += 1


        lst.append(
        f"""\nPROJECT_ROOT   =   os.path.join(os.path.abspath(__file__))
        STATIC_ROOT  =   os.path.join(PROJECT_ROOT, 'staticfiles')
        STATIC_URL = '/static/'
        # Extra lookup directories for collectstatic to find static files
        STATICFILES_DIRS = (
            os.path.join(PROJECT_ROOT, 'static'),
        )
        #  Add configuration for static files storage using whitenoise
        STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
        import dj_database_url 
        prod_db  =  dj_database_url.config(conn_max_age=500)
        DATABASES['default'].update(prod_db)
        ALLOWED_HOSTS = ['{appName}.herokuapp.com']
        django_heroku.settings(locals())\n"""
        )

    #Clear out the settings.py file.
    open(f'{projectName}/settings.py', 'w').close()

    #Now rewrite it by making each element of the modified list a line in the file.
    for line in lst:
        with open(f"{projectName}/settings.py", "a") as f:
            f.write(line)

    
    #Now deploy it to heroku
    execute('git init')
    execute(f'heroku git:remote -a {appName}')
    execute('git add .', False)
    execute('git commit -m "commit"', False)
    execute('heroku config:set     DISABLE_COLLECTSTATIC=1', False)  
    execute('git push heroku master')

    print(f"If everything's gone well, your app should be deployed to https://{appName}.heroku.com")