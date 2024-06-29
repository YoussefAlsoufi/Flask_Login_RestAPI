# Flask_Login_RestAPI

Features : 
1- Sign up / Login pages with Customizing the Login Process 
  - when a user attempts to access a login_required view without being logged in, Flask-Login will flash a message and redirect them to the log in view. (If the login view is not set, it will abort with a 401 error.)
  with config parameters: 
        
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=60) 
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=30)
    so, The user will remain logged in for 60 seconds if they select the "remember me" option during login. This means that even if the user closes the browser, they will remain logged in for this duration.
    and the session will expire 30 seconds after being created. This is useful for controlling how long a session should last before requiring the user to log in again, regardless of activity.


2- Edit personal info with only freash login.
 -  When a user logs in, their session is marked as “fresh,” which indicates that they actually authenticated on that session. When their session is destroyed and they are logged back in with a “remember me” cookie, it is marked as “non-fresh.” login_required does not differentiate between freshness, which is fine for most pages. However, sensitive actions like changing one’s personal information should require a fresh login. (Actions like changing one’s password should always require a password re-entry regardless.)
  fresh_login_required, in addition to verifying that the user is logged in, will also ensure that their login is fresh. If not, it will send them to a page where they can re-enter their credentials. You can customize its behavior in the same ways as you can customize login_required, by setting LoginManager.refresh_view, needs_refresh_message, and needs_refresh_message_category.

3- users list category appears only in case an admin logs in.

4- super admins have access to update the roles of users.

5- Flask app is connected to sql server.

6- The add_note function handles the form submission for adding new notes. It ensures that:

 - Only logged-in users can add notes.
 - The note content is not empty.
 - Successfully adds a new note to the database.
 - Provides appropriate feedback to the user through flash messages.
 - Redirects to the same page to display the updated list of notes and the add note form. 