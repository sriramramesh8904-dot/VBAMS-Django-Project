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
from django.db.models import Q
User = get_user_model()

@login_required(login_url='/')
def ADD_DRIVER(request):
    
    if request.method == "POST":
        did = request.POST.get('driverid')
        pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobilenumber = request.POST.get('mobilenumber')
        address = request.POST.get('address')
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('add_driver')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists')
            return redirect('add_driver')
        else:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                user_type=2,
                profile_pic=pic,
            )
            user.set_password(password)
            user.save()

            

            driver = Driver(
                admin=user,
                driverid=did,
                mobilenumber=mobilenumber,
                address=address,
            )
            driver.save()

            messages.success(request, 'Driver details added Successfully')
            return redirect('add_driver')
    return render(request, 'admin/add-driver.html')

@login_required(login_url='/')
def MANAGEDRIVER(request):
    driver_list = Driver.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(driver_list, 10)  # Show 10 drivers per page

    try:
        drivers = paginator.page(page)
    except PageNotAnInteger:
        drivers = paginator.page(1)
    except EmptyPage:
        drivers = paginator.page(paginator.num_pages)

    context = {'drivers': drivers}
    return render(request, 'admin/manage-driver.html', context)



@login_required(login_url='/')
def DELETE_DRIVER(request, id):
    try:
        driver = get_object_or_404(Driver, id=id)
        custom_user = driver.admin  # Access the related CustomUser
        driver.delete()  # This will also delete the associated CustomUser because of the on_delete=models.CASCADE
        custom_user.delete()
        messages.success(request, 'Record deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting record: {e}')
    return redirect('manage_driver')


@login_required(login_url='/')
def UPDATE_DRIVER(request,id):
    drivers = Driver.objects.get(id=id)
    
    context = {
         'dri':drivers,
    }

    return render(request,'admin/edit-driver-details.html',context)


@login_required(login_url='/')
def UPDATE_DRIVER_DETAILS(request):
    if request.method == 'POST':
        dri_id = request.POST.get('d_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        mobilenumber = request.POST.get('mobilenumber')
        address = request.POST.get('address')

        try:
            driver = Driver.objects.get(id=dri_id)
            customuser = driver.admin  # Assuming 'customuser' is a ForeignKey in Driver model

            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.email = email            
            driver.mobilenumber = mobilenumber
            driver.address = address
            
            if profile_pic:
                customuser.profile_pic = profile_pic
                
            customuser.save()
            driver.save()
            
            messages.success(request, "Driver details have been updated successfully")
            return redirect('manage_driver')

        except ObjectDoesNotExist:
            messages.error(request, "Driver update failed: Driver not found.")
        except IntegrityError as e:
            if 'mobilenumber' in str(e):
                messages.error(request, "Driver update failed: Mobile number already exists.")
            else:
                messages.error(request, f"An integrity error occurred: {e}")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

    return render(request, 'admin/manage-driver.html')


@login_required(login_url='/')
def NEWBOOKINGREQUEST(request):
    br_list = Booking.objects.filter(status='')
    page = request.GET.get('page', 1)

    paginator = Paginator(br_list, 10)  # Show 10 Booking Request per page

    try:
        br = paginator.page(page)
    except PageNotAnInteger:
        br = paginator.page(1)
    except EmptyPage:
        br = paginator.page(paginator.num_pages)

    context = {'br': br}
    return render(request, 'admin/new-request.html', context)

@login_required(login_url='/')
def APPROVEDWBOOKINGREQUEST(request):
    br_list = Booking.objects.filter(status='Approved')
    page = request.GET.get('page', 1)

    paginator = Paginator(br_list, 10)  # Show 10 Booking Request per page

    try:
        br = paginator.page(page)
    except PageNotAnInteger:
        br = paginator.page(1)
    except EmptyPage:
        br = paginator.page(paginator.num_pages)

    context = {'br': br}
    return render(request, 'admin/approved-request.html', context)

@login_required(login_url='/')
def REJECTEDBOOKINGREQUEST(request):
    br_list = Booking.objects.filter(status='Rejected')
    page = request.GET.get('page', 1)

    paginator = Paginator(br_list, 10)  # Show 10 Booking Request per page

    try:
        br = paginator.page(page)
    except PageNotAnInteger:
        br = paginator.page(1)
    except EmptyPage:
        br = paginator.page(paginator.num_pages)

    context = {'br': br}
    return render(request, 'admin/rejected-request.html', context)


@login_required(login_url='/')
def ALLBOOKINGREQUEST(request):
    br_list = Booking.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(br_list, 10)  # Show 10 Booking Request per page

    try:
        br = paginator.page(page)
    except PageNotAnInteger:
        br = paginator.page(1)
    except EmptyPage:
        br = paginator.page(paginator.num_pages)

    context = {'br': br}
    return render(request, 'admin/all-request.html', context)



@login_required(login_url='/')
def UPDATE_REQUEST(request, id):
    # Fetch the booking details with the given id
    bookingdetails = get_object_or_404(Booking, id=id)
    driver_list = Driver.objects.all()

    if request.method == 'POST':
        # Get data from the POST request
        remark = request.POST.get('remark')
        status = request.POST.get('status')
        assignto_id = request.POST.get('assignto')
        
        # Update booking details
        bookingdetails.remark = remark
        bookingdetails.status = status

        # If booking is rejected, clear the assignto field
        if status.lower() == 'rejected':
            bookingdetails.assignto = None
        else:
            # Assign the selected driver
            bookingdetails.assignto_id = assignto_id
        
        bookingdetails.save()
        
        messages.success(request, "Status updated successfully")
        return redirect('all_booking_request')
    
    # Context to be passed to the template
    context = {
        'brd': bookingdetails,
        'drivers': driver_list,
    }

    return render(request, 'admin/view-booking-details.html', context)


@login_required(login_url='/')
def ONTHEWAYBOOKINGREQUEST(request):
    br_list = Booking.objects.filter(status='On The Way')
    page = request.GET.get('page', 1)

    paginator = Paginator(br_list, 10)  # Show 10 Booking Requests per page

    try:
        br = paginator.page(page)
    except PageNotAnInteger:
        br = paginator.page(1)
    except EmptyPage:
        br = paginator.page(paginator.num_pages)

    context = {'br': br}
    return render(request, 'admin/driver-response.html', context)

@login_required(login_url='/')
def COMPLETEDTASKBOOKINGREQUEST(request):
    br_list = Booking.objects.filter(status='Completed')
    page = request.GET.get('page', 1)

    paginator = Paginator(br_list, 10)  # Show 10 Booking Requests per page

    try:
        br = paginator.page(page)
    except PageNotAnInteger:
        br = paginator.page(1)
    except EmptyPage:
        br = paginator.page(paginator.num_pages)

    context = {'br': br}
    return render(request, 'admin/driver-response.html', context)

@login_required(login_url='/')
def DRIVERRESPONSEBOOKINGDETAILS(request, id):
    # Fetch the booking details with the given id
    bookingdetails = get_object_or_404(Booking, id=id)
    # Fetch tracking history for the booking
    tracking_history = Tracking.objects.filter(booking_id=bookingdetails).order_by('creationdate_at')
    
    # Context to be passed to the template
    context = {
        'brd': bookingdetails,
        'tracking_history': tracking_history
    }

    return render(request, 'admin/driver-response-booking-details.html', context)

@login_required(login_url='/')
def Search_Booking_Request(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        if query:
            # Filter records where fullname, bookingnumber, or mobilenumber contains the query
            booking_search = Booking.objects.filter(
                bookingnumber__icontains=query
            ) | Booking.objects.filter(
                fullname__icontains=query
            ) | Booking.objects.filter(
                mobilenumber__icontains=query
            )
            
            messages.success(request, f"Search results for '{query}'")
            return render(request, 'admin/search-booking-request.html', {'booking_search': booking_search, 'query': query})
        else:
            messages.warning(request, "No search query provided.")
            return render(request, 'admin/search-booking-request.html', {})

@login_required(login_url='/')
def Between_Date_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    bookings = []

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'admin/between-dates-report.html', {'bookings': bookings, 'error_message': 'Invalid date format'})

        # Filter bookings between the given date range
        bookings = Booking.objects.filter(bookingdate_at__range=(start_date, end_date))

    return render(request, 'admin/between-dates-report.html', {'bookings': bookings, 'start_date': start_date, 'end_date': end_date})





@login_required(login_url='/')
def Driverwise_Booking_Report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    driver_data = []
    drivers = Driver.objects.all()

    if start_date and end_date:
        # Validate the date inputs
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format')
            return render(request, 'admin/driverwise-booking-report.html', {'driver_data': driver_data})

        for driver in drivers:
            bookings = Booking.objects.filter(updated_at__range=(start_date, end_date), assignto=driver)
            assigned_count = bookings.filter(status='Approved').count()
            ontheway_count = bookings.filter(status='On The Way').count()
            completed_count = bookings.filter(status='Completed').count()

            # Adjust remaining count to always include 'On The Way' and 'Assigned' bookings
            remaining_count = assigned_count + ontheway_count

            driver_data.append({
                'driver': driver,
                'assigned_count': assigned_count,
                'completed_count': completed_count,
                'remaining_count': remaining_count,
                'ontheway_count':ontheway_count,
            })

    context = {
        'driver_data': driver_data,
        'start_date': start_date,
        'end_date': end_date
    }

    return render(request, 'admin/driverwise-booking-report.html', context)
