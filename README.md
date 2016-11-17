
Drcrhono Birthday reminder is a Django app that facilitates doctors to greet their patients on their birthdays with ease!

**Technologies used to build this application include:**
* Python 2.7
* Django 1.9
* jQuery

**Additional Dependancies:**
* DrChrono API

In `settings.py`:
* You can fetch the CLIENT_DATA and CLIENT_SECRET by logging in to your Drchrono API Management.
* Update 'redirect_url' with your url for redirecting (will be http://localhost:port_no./oauth if run locally).
* Change your email settings accordingly.


**Run the following command daily to ensure patients receive the email exactly on their birthdays:**
```sh
python manage.py send_emails
```      
 
 
direct check: https://drchronobirthdayreminder.herokuapp.com/
      
