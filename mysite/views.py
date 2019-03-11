import datetime
from django.utils import timezone
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType

from read_statistics.utils import get_seven_days_read_data, get_hot_data
from blog.models import Blog

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    week_ago = today - datetime.timedelta(days=7)
    month_ago = today - datetime.timedelta(days=30)
    context = {}
    context['dates'] = dates
    context['read_nums'] = read_nums
    context['tody_hot_blogs'] = get_hot_data(Blog, begin_time=today, end_time=today)
    context['yesterday_hot_blogs'] = get_hot_data(Blog, begin_time=yesterday, end_time=yesterday)
    context['week_ago_hot_blogs'] = get_hot_data(Blog, begin_time=week_ago, end_time=yesterday, cache_name='week')
    context['month_ago_hot_blogs'] = get_hot_data(Blog, begin_time=month_ago, end_time=yesterday, cache_name='month')
    return render(request, 'home.html', context)

