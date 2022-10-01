1. Clone the project.
2. Create a Virtual Environment with the package of your choice such as venv (python -m venv venv) in the project folder.
3. "Pip install requirements.txt" to install all the required packages.
4. Setup the database of your choice in Settings.py.
5. Run "python manage.py makemigrations" and then "python manage.py migrate".
6. Then, Run "python manage.py runserver".
7. Go to POSTMAN or any other API testing tool and start using the API.
8. The two roles in the system have been implemented LIBRARIAN and MEMBER.
9. User can register/login to get the JWT access and refresh tokens.
10. They have been configured for 30 minutes and can be configured in settings.py.

## Endpoints
    Register using username, password and role("LIBRARIAN" or "MEMBER")
    path('register/',RegisterAPI.as_view(), name='register'),
    Login using username, password
    path('login/', LoginAPI.as_view(), name='login'),

#   Role Restricted view(need to be logged in and have the correct permissions)
    view all members and create new members as a LIBRARIAN
    path('members/', MemberViewAPI.as_view(), name='member-list'),
    view particular members and update them as LIBRARIAN or view self as MEMBER
    path('members/<str:id>/', MemberOpsAPI.as_view(), name='member-operations'),
    view all books or create books as LIBRARIAN
    path('localhost:8000/books/', BooksView.as_view(), name = 'books'),
    view a single book details, update, or delete it as LIBRARIAN
    path('localhost:8000/books/<str:id>/', BookView.as_view(), name = 'book'),
    BORROW or RETURN book as MEMBER
    path('localhost:8000/books/<str:id>/issue/', BookIssueView.as_view(), name = 'issue'),