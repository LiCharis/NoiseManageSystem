from django.shortcuts import render, HttpResponse
from user.models import User
from data.models import Data
from loudness.models import Loudness
from sharpness.models import Sharpness
from volatility.models import Volatility
from clarity.models import Clarity

def dashboard(request):
    user_count = User.objects.count()
    data_count = Data.objects.count()
    loudness_count = Loudness.objects.count()
    sharpness_count = Sharpness.objects.count()
    volatility_count = Volatility.objects.count()
    clarity_count = Clarity.objects.count()

    context = {'user_count': user_count, 'data_count': data_count, 'loudness_count': loudness_count,
               'sharpness_count': sharpness_count, 'volatility_count': volatility_count,
               'clarity_count': clarity_count}
    print("hello")
    return render(request, 'ManageSystem/dashboard.html', locals())


