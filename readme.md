README

Instruction to use this project

1. clone the project and open it in django
2. Activate the venv by running the script .env/Scripts/Activate
3. pip install all requirements from requirements.txt using python -m pip install -r requirements.txt
4. after this you should run "python manage.py makemigrations" and "python manage.py migrate"
5. run "python manage.py runserver"
6. All setup should be done and db.sqlite3 should be created

   Website Instructions
   1. go to http://127.0.0.1:8000/
   2. The webpage should load
   3. to get started click login and scroll down and click signup
   4. You now need to create a user using email and password
   5. From here you can start creating groups by click the create group link on the mainpage
   6. if you create multiple users and want to join a group login and click the join group button on the mainpage. Enter the name of the group you want to join (This is case sensitive)
   7. in the group you can toggle between showing chat messages and expense objects by clicking "show group messages" and "show group expenses"
   8. On the page showing group expenses you can add new expenses. You can also click "show balances" to see what the logged in user owes/is owed by each user in this group, Only expenses approved by all members will be loaded
   9. Paymentinformation can so far only be added via api or the admin panel. So you can either create a super user by running "python manage.py createsuperuser" and going to the admin panel. Or use the superuser to make an Api request adding paymentinformation
   10. Alternatively go to base/api/views and remove IsSuperuser from @permissionclasses for the api permission you want to change so that any user can use the api call.
   11. Edit and delete buttons appear on rooms that the currently logged in user has created if you want to change something.
   12. Any and all data can be changed via API requests as a superuser (Including changing peoples passwords, changing expenses paymentinformation and so on) 
