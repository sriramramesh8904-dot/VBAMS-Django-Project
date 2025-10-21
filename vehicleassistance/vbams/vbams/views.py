from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import  logout,login,authenticate
from django.contrib.auth.decorators import login_required
from vbamsapp.models import CustomUser,Booking,Driver
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
import random
User = get_user_model()

def BASE(request):    
       return render(request,'base.html')


def LOGIN(request):
    return render(request,'login.html')


def doLogout(request):
    logout(request)
    return redirect('login')

def doLogin(request):
    if request.method == 'POST':
        user = authenticate(request,
                                         username=request.POST.get('username'),
                                         password=request.POST.get('password')
                                         )
        if user!=None:
            login(request,user)
            user_type = user.user_type
            if user_type == '1':
                 return redirect('dashboard')
            elif user_type == '2':
                 return redirect('dashboard')
           
            
            
        else:
                messages.error(request,'Username or Password is not valid')
                return redirect('login')
    else:
            messages.error(request,'Username or Password is not valid')
            return redirect('login')

login_required(login_url='/')
def DASHBOARD(request):
    driver_count = Driver.objects.count()

    # More efficient way to get all counts in one query
    booking_counts = Booking.objects.aggregate(
        newbookingcount=Count('id', filter=Q(status='')),
        approvedbookingcount=Count('id', filter=Q(status='Approved')),
        otwbookingcount=Count('id', filter=Q(status='On The Way')),
        compbookingcount=Count('id', filter=Q(status='Completed')),
        rejbookingcount=Count('id', filter=Q(status='Rejected')),
    )

    context = {
        'driver_count':driver_count,
    }
    context.update(booking_counts)

    return render(request,'dashboard.html',context)


def PROFILE(request):
    user = get_object_or_404(CustomUser, id=request.user.id)
    driver = Driver.objects.filter(admin=request.user.id).first()
    context = {
        "user": user,
        "driver": driver,
    }
    return render(request, 'profile.html', context)




@login_required(login_url='/')
def PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if not request.user.is_superuser:
            # If the user is not an admin, redirect them or show an error
            messages.error(request, "You do not have permission to update profiles.")
            return redirect('profile')

        try:
            # Retrieve the CustomUser object
            customuser = CustomUser.objects.get(id=request.user.id)

            # Update CustomUser profile
            customuser.first_name = first_name
            customuser.last_name = last_name

            if profile_pic:
                customuser.profile_pic = profile_pic

            customuser.save()
            messages.success(request, "Your profile has been updated successfully")

        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist")
        except Exception as e:
            messages.error(request, f"Profile update failed: {e}")

        # Redirect to the profile page after processing
        return redirect('profile')

    # Render the profile page if not a POST request
    return render(request, 'profile.html')



@login_required(login_url = '/')
def CHANGE_PASSWORD(request):
     context ={}
     ch = User.objects.filter(id = request.user.id)
     
     if len(ch)>0:
            data = User.objects.get(id = request.user.id)
            context["data"]:data            
     if request.method == "POST":        
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
          user.set_password(new_pas)
          user.save()
          messages.success(request,'Password Change  Succeesfully!!!')
          user = User.objects.get(username=un)
          login(request,user)
        else:
          messages.success(request,'Current Password wrong!!!')
          return redirect("change_password")
     return render(request,'change-password.html')


def USERBASE(request):
    
    return render(request, 'userbase.html')

def Index(request):
    if request.method == "POST":
        # Generate a random booking number
        bookingnumber = random.randint(100000000, 999999999)
        
        # Get the form data
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        mobilenumber = request.POST.get('mobilenumber')
        pickuplocation = request.POST.get('pickuplocation')
        destination = request.POST.get('destination')
        pickupdate = request.POST.get('pickupdate')
        pickuptime = request.POST.get('pickuptime')

        # Create a new booking instance
        bookingreq = Booking(
            fullname=fullname,
            email=email,
            mobilenumber=mobilenumber,
            pickuplocation=pickuplocation,
            destination=destination,
            pickupdate=pickupdate,
            pickuptime=pickuptime,
            bookingnumber=bookingnumber
        )
        
        # Save the booking to the database
        bookingreq.save()
        
        # Display a success message and redirect to the thank you page
        
        return redirect('thankyou')

    return render(request, 'index.html')

def Thankyou(request):   
    # Fetch the most recent booking
    booking = Booking.objects.order_by('-id').first()

    # Pass the booking to the template
    context = {
        'booking': booking,
    }
    return render(request, 'thankyou.html', context)


def Aboutus(request):
    
    return render(request, 'aboutus.html')

def Contactus(request):
    return render(request, 'contactus.html')