from django.shortcuts import render, redirect
from django.db import connection


def register(request):
    """Handle student registration."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not name or not email or not password:
            return render(request, 'register.html', {'error': 'All fields are required.'})

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO student (name, email, password) VALUES (%s, %s, %s)",
                [name, email, password]
            )
        return redirect('login')
    return render(request, 'register.html')


def login_page(request):
    """Handle student login."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM student WHERE email = %s AND password = %s",
                [email, password]
            )
            user = cursor.fetchone()

        if user:
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password. Please try again.'})
    return render(request, 'login.html')


def dashboard(request):
    """Show all registered students."""
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM student")
        students = cursor.fetchall()

    return render(request, 'dashboard.html', {'students': students})


def edit_student(request, id):
    """Edit an existing student record."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not name or not email:
            # Fetch student again to re-populate the form
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM student WHERE id = %s", [id])
                student = cursor.fetchone()
            return render(request, 'edit_student.html', {
                'student': student,
                'error': 'Name and email are required.'
            })

        if password:
            # Update password only if a new one is provided
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE student SET name=%s, email=%s, password=%s WHERE id=%s",
                    [name, email, password, id]
                )
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE student SET name=%s, email=%s WHERE id=%s",
                    [name, email, id]
                )

        return redirect('dashboard')

    # GET: load student data into form
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM student WHERE id = %s", [id])
        student = cursor.fetchone()

    if not student:
        return redirect('dashboard')

    return render(request, 'edit_student.html', {'student': student})


def delete_student(request, id):
    """Delete a student record."""
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM student WHERE id = %s", [id])
    return redirect('dashboard')