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

 7- using Openssl to generate self-signed certificate for DEV env, that can help you test how your application behaves when served over HTTPS. 

 8- useing  login_manager.session_protection = "strong" in DEV env to test how the session protection behaves in development environment before deploying to production to understand its impact on user experience.
 Note: It’s important to strike a balance between security and usability. For most applications, "basic" session protection might be sufficient, but if you require higher security (e.g., for sensitive applications), "strong" session protection is a better choice. And Be aware that enabling "strong" session protection might sometimes log users out if their IP address changes frequently (e.g., mobile users switching between Wi-Fi and cellular networks).

 9- Graph GI
 10- FAST API
 11- Create a Test Project.
 What to Test
- Unit Tests

Models: Ensure that your models are correctly defined and can perform CRUD operations.
Forms: Verify form validation and error handling.
Utilities/Helpers: Test any utility functions or helper methods used in your application.


- Integration Tests
Views/Endpoints: Test that your routes return the expected status codes and data.
Database Interactions: Verify that data is correctly inserted, updated, and deleted in the database.
User Authentication: Test login, logout, and protected routes.


- Functional Tests
Full User Scenarios: Simulate real user actions and ensure the application behaves as expected.
Forms and Input: Test form submissions, validations, and error messages.


- Regression Tests
Ensure that new changes do not break existing functionality.


- Security Tests
CSRF Protection: Ensure that forms are protected against CSRF attacks.
Input Validation: Test for SQL injection, XSS, and other security vulnerabilities.

Full test Lifecycle:
- Setup: The fixture app() is called, Flask app is created, and the database schema is set up within the application context.
- Yield: The app instance is yielded to the test function test_example().
- Test Execution: The test function runs using the app instance.
- Teardown: After the test function completes, control returns to the fixture, which then executes the code after the yield (dropping the database tables).

client Fixture
The client fixture provides a test client for the Flask application. This test client allows you to simulate HTTP requests to your Flask application without having to run a live server. This is useful for testing routes, request handling, and responses.

runner Fixture
The runner fixture provides a test command-line interface (CLI) runner. This allows you to invoke Flask CLI commands in a testing context. This is useful for testing custom management commands or other CLI-related functionality.

- new end point has generated which gives abilities for admins to communicate with each other seperately or as a group via creating a chating room.
each one can join the room by providing a room code generated when a room created by one of the admins

For production env we are planning to use : 
Eventlet library which is generally easier to set up and can handle many concurrent connections efficiently. It is a good choice for applications where ease of use and simplicity are important.
It's a Python library designed to handle concurrent network applications efficiently by using coroutines (lightweight threads) and non-blocking I/O.
