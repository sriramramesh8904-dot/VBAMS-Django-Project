
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views, adminviews, driverviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    path('Dashboard', views.DASHBOARD, name='dashboard'),
    path('Login', views.LOGIN, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),
    path('Profile', views.PROFILE, name='profile'),
    path('Profile/update', views.PROFILE_UPDATE, name='profile_update'),
    path('Password', views.CHANGE_PASSWORD, name='change_password'),
    path('userbase/', views.USERBASE, name='userbase'),
    path('', views.Index, name='index'),
    path('Thankyou', views.Thankyou, name='thankyou'),
     path('Aboutus', views.Aboutus, name='aboutus'),
    path('Contactus', views.Contactus, name='contactus'),

    # Admin Panel
    path('Admin/AddDriver', adminviews.ADD_DRIVER, name='add_driver'),
    path('Admin/ManageDriver', adminviews.MANAGEDRIVER, name='manage_driver'),
    path('Admin/DeleteDriver/<str:id>', adminviews.DELETE_DRIVER, name='delete_driver'),
    path('Admin/UpdateDriver/<str:id>', adminviews.UPDATE_DRIVER, name='update_driver'),
    path('Admin/UPDATE_Driver_DETAILS', adminviews.UPDATE_DRIVER_DETAILS, name='update_driver_details'),
    path('Admin/NewBookinRequest', adminviews.NEWBOOKINGREQUEST, name='new_booking_request'),
    path('Admin/ApprovedBookinRequest', adminviews.APPROVEDWBOOKINGREQUEST, name='approved_booking_request'),
    path('Admin/RejectedBookinRequest', adminviews.REJECTEDBOOKINGREQUEST, name='rejected_booking_request'),
    path('Admin/AllBookinRequest', adminviews.ALLBOOKINGREQUEST, name='all_booking_request'),
    path('Admin/UpdateRequest/<str:id>', adminviews.UPDATE_REQUEST, name='update_request'),

    path('Admin/OnthewayBookinRequest', adminviews.ONTHEWAYBOOKINGREQUEST, name='ontheway_booking_request'),
    path('Admin/CompletedTaskBookinRequest', adminviews.COMPLETEDTASKBOOKINGREQUEST, name='completedtask_booking_request'),
    path('Admin/DriverBookingResponse/<str:id>', adminviews.DRIVERRESPONSEBOOKINGDETAILS, name='driver_response_booking'),
    path('Admin/SearchBookingRequset', adminviews.Search_Booking_Request, name='search_booking_request'),
    path('Admin/BetweenDateReport', adminviews.Between_Date_Report, name='booking-bwdate-report'),
    path('Admin/DriverwiseBookingReport', adminviews.Driverwise_Booking_Report, name='driverwise-booking-report'),
    

# Driver Panel
 path('DriverProfile', driverviews.DRIVER_PROFILE, name='driver-profile'),
 path('DriverProfile/update', driverviews.DRIVER_PROFILE_UPDATE, name='driver_profile_update'),
 path('Driver/AssignBookinRequest', driverviews.ASSIGNWBOOKINGREQUEST, name='assign_booking_request'),
 path('Driver/OTWBookinRequest', driverviews.OTWBOOKINGREQUEST, name='otw_booking_request'),
 path('Driver/CompBookinRequest', driverviews.COMPBOOKINGREQUEST, name='completed_booking_request'),
 path('Driver/AllBookinRequest', driverviews.ALLASSIGNBOOKINGREQUEST, name='all_assign_booking_request'),
 path('Driver/AssignUpdateRequest/<str:id>', driverviews.ASSIGN_UPDATE_REQUEST, name='assign_update_request'),
 path('Driver/SearchBooking', driverviews.Search_Booking, name='search_booking'),
  path('Driver/BookingReport', driverviews.Between_Date_Booking_Report, name='booking-report'),
  

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
