#EDOCTORUG API VERSION 3.44 REST ENDPOINT
This django project contains rest endpoints that communicate with the yo api endpoints.

## INSTALLATION:
#### 1: cd to edoctor_airtimeapi usng the command cd edoctor_airtimeapi

#### 2: execute:
##### pip install -r requirements.txt

## GENERATE DOCUMENTATION:
#### 1: cd to edoctor_airtimeapi usng the command cd edoctor_airtimeapi

#### 2: To run the doc server execute: 
##### <p><b> &nbsp; &nbsp; python django_pydoc.py -b </b></p>

## RUN SERVER:
#### 1: cd to edoctor_airtimeapi usng the command cd edoctor_airtimeapi

#### 2: execute:
##### python manage.py runserver
or
##### ./manage.py runserver

## DEPLOY TO VERCELL
#### 1: Login to your vercel account
#### 2: Connect your github to vercel
#### 3: Create a new vercel project and name it anything you like
#### 4: Import github repository edoctAndroidAppIntern to vercel project.
#### 5: Since you will be importing a repository from an organization `EdoctorUg`, you are required to create a team to automatically upgrade to pro.
`soo, After Importing the repository from the organization, the next page will have the create team and configure project views.`<br/>
        - <b>`Click on create team and follow the prompts to create a team.`<\b><br\>
`NB: if you are not importing from an organization, then this step is not necessary`
#### 6: In the Configure Project Page:
        1 - Give your project any name of choice.

        2 - In the ``Framework Preset``, choose `other`.

        3 - In the `Root Directory settings`:

            - Set `Root Directory` to `Edoctor_AirtimeAPI/edoctor_airtimeapi` 
            then press continue

        4 - In the Build and Output Settings:

            - set the Build Command to python manage.py runserver after toggling the override
             button

            - set the Install Command to pip install -r requirements.txt after toggling 
            the associated override button.

            -  Click Deploy After Creating your team.
#### 7: After deploying click goto project.
#### 8: In the project's dashboard, you can see a log og the deployed project.
#### 9: To create the postgres db, click storage in the top menu. You will see a list of databases you can create. `click create button next to postgres to create a postgres database`.
#### 10: Give the database a name of your choice and continue. After the database has been created, click `.env.local` then `show secret` to get the database parameters.
#### 11: Update the `DATABASES` settings in `settings.py` with the database parameters
#### 12: Change the file Edoctor_AirtimeAPI/edoctor_airtimeapi/edoctor_airtimeapi/settings.py and edit the DataBase Variable such that:
DATABASES = {<br/>
    'default': {<br/>
        'ENGINE': 'django.db.backends.postgresql',<br/>
        'USER':'default',<br/>
        'HOST':"url of the postgres database",<br/>
        'PASSWORD':"password to he postgres database",<br/>
        'NAME':"name of the postgres database",<br/>
        'PORT':'port number the database is listening on'<br/>
    }
}
#### 13: Go to the project dashboard of your newly created project and import a git repository
#### 14: In the Importing Repository section, set the root directory as the Edoctor_AirtimeAPI/edoctor_airtimeapi repository directory then deploy
#### 15: Find the Postman Documentation Here: https://documenter.getpostman.com/view/32924611/2sA3QsAY55
