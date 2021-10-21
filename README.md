# ErrorLoggingMiddleware
Error logging middleware with stand-lone app to perform CRUD operations on the stored database.


Error Logging Middleware with CRUD operation app
================================================

A simple Django Middleware for error logging.

In a nutshell, the Middleware intercepts a response by a view and look up from settings.py file of yourProject.
On match it stores status code and error message in database and updates response status code to 200 and message to "Error"


Quick Start
-----------

**1. Fetch project from git :**

    Download zip/git pull

**2. Include "errorMgmt" to your INSTALLED_APPS in yourProject/seetings.py:**


    INSTALLED_APPS = [
        ...
        'errorMgmt',
    ]

**3. Include "ErrorLogMiddleware" as last element to your MIDDLEWARE_CLASSES in yourProject/seetings.py:**

    MIDDLEWARE_CLASSES = (
        ...
        'errorMgmt.middleware.error_logging.ErrorLogMiddleware'
    )


**4. Add status codes to watch for in yourProject/setting.py**

    STATUS_CODES = [
          402,
          400,
          500,
          201
      ]

**5. Add URLs for CRUD operations in yourProject/urls.py**

  urlpatterns = [
      ...
      path('', include('errorMgmt.urls')),
  ]

**6. Run below commands to create database elements to store error details.**
  
  	Python manage.py makemigrations
    Python manage.py migrate
  
 **7. Start your development server and wait for the view exceptions (or not).**


API Usage
-----------

**1. Make request on http://127.0.0.1:8000 :**

    1.1) GET status 200 success | status 404 No matching records founds
        a) fetch all records    - /fetch/
        b) fetch by status code - /fetch/?sc=XXX
        c) fetch by ID          - /fetch/?id=XXX
        
        Response Body - JSON format
        [
          {
        		"status": 499,
        		"error": "Client machine down"
          }
        ]
    
    1.2) DELETE status 202 success | status 404 No matching records founds
        a) fetch by status code - /del/?sc=XXX
        b) fetch by ID          - /del/?id=XXX
    
    
    1.3) PUT status 201 created | status 400 Invalid input
        a) modify by status code - /modify/?sc=XXX
        b) modify by ID          - /modify/?id=XXX
        
        Request Body - JSON format
        [
          {
        		"status": 499,
        		"error": "Client machine down"
          }
        ]
    
    1.4) POST status 201 created | status 400 Invalid input
        a) create entry - /createlog/
        Request Body - JSON format
        [
          {
        		"status": 499,
        		"error": "Client machine down"
          }
        ]
