from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from .models import *


from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import get_messages
# Create your views here.
from django.core.exceptions import PermissionDenied

from django.http import JsonResponse
from .decorators import redirect_if_authenticated



from twilio.rest import Client



account_sid = 'ACcc2543589bc9989478d117aa1772aeca'
auth_token = '35424683da5f91014950165839420196'
client = Client(account_sid, auth_token)


def send_sms(body):
    try:
        client = Client(account_sid, auth_token)

        message = client.messages.create(
        from_='+12513194915',
        to='+639913226415',
        body = body
        )
        
        print(message.sid)

        return message

    except Exception as e:
        print(f"Error sending SMS: {str(e)}")
        return None




@redirect_if_authenticated
def login_page(request):
    return render(request, 'base/login.html')

@redirect_if_authenticated
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log in the user
                if user.is_staff:
                    return redirect('dashboard')
                elif not user.is_active:
                    messages.error(request, 'Your account is currently inactive. Please contact the administrator for approval.')
                else:
                    return redirect('index')
            else:
                messages.info(request, 'Username or password is incorrect')

        except PermissionError:
            messages.error(request, 'An unexpected error occurred during login.')

    return render(request, 'base/login.html', context={'messages': get_messages(request)})


def logout_user(request):
    logout(request)

    return redirect('login')

@redirect_if_authenticated
def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('student_number')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        student_number = request.POST.get('student_number')
        phone_number = request.POST.get('phone_number')
        course = request.POST.get('course')
        batch = request.POST.get('batch')
        proof = request.FILES.get('proof')
        employment = request.POST.get('employment')

        try:
            # Create a new user
            user = User.objects.create_user(
                username=username,
                first_name=firstname,
                last_name=lastname,
                email=email,
                password=username,  # Use username as password
                is_active=False  # User is inactive until approved
            )

            # Create Alumni record
            alumni = Alumni.objects.create(
                user=user,
                student_number=student_number,
                phone_number=f"+63{phone_number}",
                course=course,
                batch=batch,
                proof=proof,
                employment=employment,
            )

            # Send confirmation email
            subject = 'Registration Confirmation'
            message = f'Dear {firstname} {lastname},\n\nThank you for registering with us. Your registration is still pending and waiting for approval.\n\n'
            message += f'Username: {username}\n'
            message += f'Password: {username}\n\n'
            message += 'Best regards,\nNJ Valdez College Foundation'

            from_email = settings.EMAIL_HOST_USER
            to_email = [email]

            send_mail(subject, message, from_email, to_email)

            send_sms('New request waiting for approval!')
           
            messages.success(request, 'Registration successful. Please check your email for confirmation.')
            return redirect('register')  # Redirect to a success page after registration

        except IntegrityError as e:
            messages.error(request, 'Registration failed. Please try again.')

    return render(request, 'base/register.html')



def index(request):
    jobs = Job.objects.all()
    context = {
        'jobs': jobs,
    }
    return render(request, 'base/index.html', context)


@login_required(login_url='login')
def alumni_profile(request):
    alumni = get_object_or_404(Alumni, user=request.user)
    requests_ = Request.objects.filter(alumni = alumni)
    context = {
        'alumni': alumni,
        'requests': requests_,
    }
    return render(request, 'base/alumni_profile.html', context)

@login_required(login_url='login')
def edit_avatar(request):
    alumni = get_object_or_404(Alumni, user=request.user)

    if request.method == 'POST':
        avatar = request.FILES.get('avatar')
        alumni.avatar = avatar
        alumni.save()

    return redirect('alumni-profile')

@login_required(login_url='login')
def profile(request):
    user = User.objects.get(username = request.user)
    
    context = {
        'user': user,
    }
    return render(request, 'base/profile.html', context)



@login_required(login_url='login')
def dashboard(request):
    alumni = Alumni.objects.all()
    tor = Request.objects.filter(file_type = 'Transcript of Records')
    diploma = Request.objects.filter(file_type = 'Diploma')
    jobs = Job.objects.all()

    context = {
        'alumni': alumni,
        'tor': tor,
        'diploma': diploma,
        'jobs': jobs,
        'tor_pending': tor.filter(status = 'Pending'),
        'diploma_pending': diploma.filter(status = 'Pending'),
        'job_pending': jobs.filter(verified = False)
    }
    return render(request, 'base/dashboard.html', context)

@login_required(login_url='login')
def alumni(request):
    alumni = Alumni.objects.all()
    context = {
        'alumni': alumni
    }
    return render(request, 'base/alumni.html', context)
@login_required(login_url='login')
def transcript(request):
    requests_ = Request.objects.filter(file_type = 'Transcript of Records')

    context = {
        'tor': requests_
    }
    return render(request, 'base/transcript.html', context)
@login_required(login_url='login')
def diploma(request):
    requests_ = Request.objects.filter(file_type = 'Diploma')

    context = { 
        'diploma' : requests_
    }
    return render(request, 'base/diploma.html', context)
@login_required(login_url='login')
def jobs(request):
    jobs = Job.objects.all()
    context = {
        'jobs': jobs
    }
    return render(request, 'base/jobs.html', context)


@login_required(login_url='login')
def post_job(request):
    alumni = Alumni.objects.get(user = request.user )
    if request.method == 'POST':
        sector = request.POST.get('sector')
        company_name = request.POST.get('company_name')
        company_email = request.POST.get('company_email')
        job_title = request.POST.get('job_title')
        job_desc = request.POST.get('description')


      

        job = Job.objects.create(
            posted_by = alumni,
            sector = sector,
            company_name = company_name,
            company_email = company_email,
            job_title = job_title,
            description = job_desc

        )

        job.save()

        messages.success(request, 'Job post request sent successfully. Please check your email for more details.')

        subject = 'NJ Valdez Alumni Job Posting Request - Pending Approval'
                    
        message = f'Dear {request.user.first_name} {request.user.last_name},\n\nThank you for your interest in posting a job opportunity on the NJ Valdez Alumni platform. \n\nWe have received your request for the following position:\n\n Sector: {sector} \nCompany Name: {company_name} \nJob Title: {job_title}\nJob Description" {job_desc} \n\nOur team will review your job posting to ensure it adheres to our guidelines. You will be notified via email once the review process is complete.'


        from_email = settings.EMAIL_HOST_USER
        to_email = [request.user.email]

        send_mail(subject, message, from_email, to_email)
        send_sms('New request waiting for approval!')

        return redirect('index') 
    
@login_required(login_url='login')    
def request_file(request):
    alumni = Alumni.objects.get(user=request.user)

    if request.method == 'POST':
        file_type = request.POST.get('request_')  # Ensure 'file_type' matches the name attribute in your form
        reason = request.POST.get('reason')

        # Check if alumni has already requested this file type
        existing_request = Request.objects.filter(alumni=alumni, file_type=file_type).first()
        if existing_request:
            messages.error(request, f'You have already requested {file_type}. Please check your account profile for more details.')
            return redirect('index')  # Redirect to wherever appropriate

        # Create and save the request object
        request_obj = Request.objects.create(
            alumni=alumni,
            file_type=file_type,
            reason=reason
        )

        request_obj.save()

        messages.success(request, 'Request sent successfully. Please check your email for more details.')

        # Send email notification
        subject = f'NJ Valdez Alumni {file_type} request - Waiting for Approval'
        message = f'Dear {alumni.user.first_name} {alumni.user.last_name},\n\n' \
                  f'Thank you for your request to obtain your {file_type} from NJ Valdez College Foundation.\n\n' \
                  f'We have received your request and it is currently pending approval.\n\n' \
                  f'Please wait patiently while our team processes your request. Once approved, you can download your {file_type} from your alumni account.\n\n' \
                  f'Thank you for your patience and understanding.\n\n' \
                  f'Best regards,\nNJ Valdez College Foundation'

        from_email = settings.EMAIL_HOST_USER
        to_email = [alumni.user.email]

        send_mail(subject, message, from_email, to_email)
        send_sms('New request waiting for approval!')

    return redirect('index')

@login_required(login_url='login')
def approve_user(request, request_id):
    alumni = Alumni.objects.get(id = request_id )
    alumni.user.is_active = True
    alumni.user.save()

        # Email notification content
    subject = 'NJ Valdez Alumni Account Activated'
    message = f"""
    Hi {alumni.user.first_name} {alumni.user.last_name},

    Your account at Nj Valdez College Foundation has been successfully activated.

    You can now log in using your credentials.
    
    
    Username: {alumni.user.username}
    Password: {alumni.user.username}
    Email: {alumni.user.email}

    Thank you for choosing NJ Valdez College Foundation!

    Sincerely,
    NJ Valdez College Foundation
    """

    # Send email notification to the user
    send_mail(
        subject,
        message,
        'noreply@njvaldez.edu.ph', 
        [alumni.user.email],
        fail_silently=False,
    )
    return redirect('dashboard')

@login_required(login_url='login')
def approve_job(request, request_id):
    job = Job.objects.get(id = request_id )
    job.verified = True
    job.save()

    # Email notification content
    subject = 'Job Post Request Approved'
    message = f"""
    Hi {job.posted_by.user.first_name} {job.posted_by.user.last_name},

    Your job post request at Nj Valdez College Foundation has been successfully approved.

    Sincerely,
    NJ Valdez College Foundation
    """

    # Send email notification to the user
    send_mail(
        subject,
        message,
        'noreply@njvaldez.edu.ph', 
        [job.posted_by.user.email],
        fail_silently=False,
    )
    return redirect('jobs')


@login_required(login_url='login')
def approve_request(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        request_obj = get_object_or_404(Request, id=request_id)

        file = request.FILES.get('file')
        if file:
            try:
                request_obj.file = file
                request_obj.status = 'Complete'
                request_obj.save()

                # Send email
                subject = f'NJ Valdez Alumni {request_obj.file_type} - File Attached'
                message = f'Dear {request_obj.alumni.user.first_name} {request_obj.alumni.user.last_name},\n\n' \
                          f'Greetings from NJ Valdez College Foundation!\n\n' \
                          f'We are pleased to inform you that your requested {request_obj.file_type} is attached, check your alumni account to download.\n\n' \
                          f'Thank you for your patience and understanding.\n\n' \
                          f'Best regards,\nNJ Valdez College Foundation'

                from_email = settings.EMAIL_HOST_USER
                to_email = [request_obj.alumni.user.email]

                send_mail(subject, message, from_email, to_email)

                # Return success response
                return JsonResponse({'message': 'Request approved successfully'})

            except Exception as e:
                return JsonResponse({'error': f'Failed to save file or send email: {str(e)}'}, status=500)

        else:
            return JsonResponse({'error': 'File not found in request'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)