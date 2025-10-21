import logging
from django.core.exceptions import ObjectDoesNotExist
from .models import Booking, Driver

logger = logging.getLogger(__name__)
def new_bookings(request):
    if request.user.is_authenticated:
        try:
            driver_admin = Driver.objects.get(admin=request.user)
            
            # Filter for assigned bookings with status 'Approved'
            assign_bookings = Booking.objects.filter(status='Approved', assignto=driver_admin)
        
            logger.debug(f"Found {assign_bookings.count()} assigned bookings for user {request.user}")
            
            return {
                'assign_bookings': assign_bookings,
            }
        except ObjectDoesNotExist:
            logger.warning(f"No Driver found for user {request.user}")
            return {
                'assign_bookings': [],
            }
    else:
        logger.info("User is not authenticated")
    return {}



def new_bookings1(request):
    if request.user.is_authenticated:
        try:
            new_bookings1 = Booking.objects.filter(status='')

            logger.debug(f"Found {new_bookings1.count()} new bookings for user {request.user}")

            return {
                'new_bookings1': new_bookings1,
            }
        except ObjectDoesNotExist:
            logger.warning(f"No Driver found for user {request.user}")
            return {
                'new_bookings1': [],
            }
    else:
        logger.info("User is not authenticated")
    return {}
