from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib import messages
from django.contrib.auth import  logout,login,authenticate
from django.contrib.auth.decorators import login_required
from vbamsapp.models import CustomUser,Driver,Booking,Tracking
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from datetime import datetime
User = get_user_model()

def DRIVER_PROFILE(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    driver = Driver.objects.filter(admin=request.user.id).first()
    context = {
        "user": user,
        "driver": driver,
    }
    return render(request, 'driver/driver-profile.html', context)



@login_required(login_url='/')
def DRIVER_PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        mobilenumber = request.POST.get('mobilenumber')

        try:
            # Retrieve the CustomUser object
            customuser = CustomUser.objects.get(id=request.user.id)
            # Retrieve the Driver profile associated with the user
            driver = Driver.objects.filter(admin=request.user.id).first()

            # Update CustomUser profile
            customuser.first_name = first_name
            customuser.last_name = last_name

            if profile_pic:
                customuser.profile_pic = profile_pic

            customuser.save()




            # Check and update Driver profile if it exists
            if driver:
                driver.address = address
                driver.mobilenumber = mobilenumber
                driver.save()
                messages.success(request, "Your profile has been updated successfully")


        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist")
        except Exception as e:
            messages.error(request, f"Profile update failed: {e}")

        # Redirect to the profile page after processing
        return redirect('driver-profile')

    # Render the profile page if not a POST request
    return render(request, 'driver/driver-profile.html')


@login_required(login_url='/')
def ASSIGNWBOOKINGREQUEST(request):
    # Get the logged-in user's corresponding Driver instance
    driver_admin = get_object_or_404(Driver, admin=request.user)
    br_list = Booking.objects.filter(status='Approved', assignto=driver_admin)
    page = request.GET.get('page', 1)

    paginator = Paginator(br_list, 10)  # Show 10 Booking Requests per page

    try:
        br = paginator.page(page)
    except PageNotAnInteger:
        br = paginator.page(1)
    except EmptyPage:
        br = paginator.page(paginator.num_pages)

    context = {'br': br}
    return render(request, 'driver/assign-booking-request.html', context)

@login_required(login_url='/')
def ASSIGN_UPDATE_REQUEST(request, id):
    # Fetch the booking details with the given id
    bookingdetails = get_object_or_404(Booking, id=id)

    if request.method == 'POST':
        # Get data from the POST request
        remark = request.POST.get('remark')
        status = request.POST.get('status')
        
        # Update booking details
        bookingdetails.remark = remark
        bookingdetails.status = status
        bookingdetails.save()
        
        # Create a new tracking record to maintain history
        Tracking.objects.create(
            booking_id=bookingdetails,
            remark=remark,
            status=status
        )
        
        messages.success(request, "Status updated successfully")
        return redirect('all_assign_booking_request')
    
    # Fetch tracking history for the booking
    tracking_history = Tracking.objects.filter(booking_id=bookingdetails).order_by('creationdate_at')
    
    # Context to be passed to the template
    context = {
        'brd': bookingdetails,
        'tracking_history': tracking_history
    }

    return render(request, 'driver/view-assign-booking-details.html', context)



@login_required(login_url='/')
def OTWBOOKINGREQUEST(request):
    # Get the logged-in user's corresponding Driver instance
    driver_admin = get_object_or_404(Driver, admin=request.user)
    br_list = Booking.objects.filter(status='On The Way', assignto=driver_admin)
    page = request.GET.get('page', 1)

    paginator = Paginator(br_list, 10)  # Show 10 Booking Requests per page

    try:
        br = paginator.page(page)
    except PageNotAnInteger:
        br = paginator.page(1)
    except EmptyPage:
        br = paginator.page(paginator.num_pages)

    context = {'br': br}
    return render(request, 'driver/assign-booking-request.html', context)

@login_required(login_url='/')
def COMPBOOKINGREQUEST(request):
    # Get the logged-in user's corresponding Driver instance
    driver_admin = get_object_or_404(Driver, admin=request.user)
    br_list = Booking.objects.filter(status='Completed', assignto=driver_admin)
    page = request.GET.get('page', 1)

    paginator = Paginator(br_list, 10)  # Show 10 Booking Requests per page

    try:
        br = paginator.page(page)
    except PageNotAnInteger:
        br = paginator.page(1)
    except EmptyPage:
        br = paginator.page(paginator.num_pages)

    context = {'br': br}
    return render(request, 'driver/assign-booking-request.html', context)

@login_required(login_url='/')
def ALLASSIGNBOOKINGREQUEST(request):
    # Get the logged-in user's corresponding Driver instance
    driver_admin = get_object_or_404(Driver, admin=request.user)
    br_list = Booking.objects.filter(assignto=driver_admin)
    page = request.GET.get('page', 1)

    paginator = Paginator(br_list, 10)  # Show 10 Booking Requests per page

    try:
        br = paginator.page(page)
    except PageNotAnInteger:
        br = paginator.page(1)
    except EmptyPage:
        br = paginator.page(paginator.num_pages)

    context = {'br': br}
    return render(request, 'driver/assign-booking-request.html', context)

@login_required(login_url='/')
def Search_Booking(request):
    try:
        driver_admin = Driver.objects.get(admin=request.user)
    except Driver.DoesNotExist:
        messages.error(request, "Driver not found.")
        return redirect('search_booking')  # Redirect to a fallback view or error page
    
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname, bookingnumber, or mobilenumber contains the query
            booking_search = Booking.objects.filter(
                assignto=driver_admin
            ).filter(
                bookingnumber__icontains=query
            ) | Booking.objects.filter(
                assignto=driver_admin
            ).filter(
                fullname__icontains=query
            ) | Booking.objects.filter(
                assignto=driver_admin
            ).filter(
                mobilenumber__icontains=query
            )
            
            messages.success(request, f"Search results for '{query}'")
            return render(request, 'driver/search-booking.html', {'booking_search': booking_search, 'query': query})
        else:
            messages.warning(request, "No search query provided.")
            return render(request, 'driver/search-booking.html', {})







@login_required(login_url='/')
def Between_Date_Booking_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    # Initialize variables
    bookings = []
    assigned_count = 0
    ontheway_count = 0
    completed_count = 0
    remaining_count = 0

    # Get the current driver's admin object
    try:
        driver_admin = Driver.objects.get(admin=request.user)
    except Driver.DoesNotExist:
        messages.error(request, "Driver not found.")
        return redirect('booking-report')  # Redirect to a fallback view or error page

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'driver/between-date-booking-report.html', {'error_message': 'Invalid date format'})

        # Filter bookings between the given date range
        bookings = Booking.objects.filter(updated_at__range=(start_date, end_date), assignto=driver_admin)

        # Get the count of each status
        assigned_count = bookings.filter(status='Approved').count()
        ontheway_count = bookings.filter(status='On The Way').count()
        completed_count = bookings.filter(status='Completed').count()

        # Adjust remaining count to always include 'On The Way' and 'Assigned' bookings
        remaining_count = assigned_count + ontheway_count

        print(f"DEBUG: Assigned Count: {assigned_count}")
        print(f"DEBUG: On The Way Count: {ontheway_count}")
        print(f"DEBUG: Completed Count: {completed_count}")
        print(f"DEBUG: Remaining Count: {remaining_count}")

    context = {
        'bookings': bookings,
        'start_date': start_date,
        'end_date': end_date,
        'assigned_count': assigned_count,
        'ontheway_count': ontheway_count,
        'completed_count': completed_count,
        'remaining_count': remaining_count,
    }

    return render(request, 'driver/between-date-booking-report.html', context)






