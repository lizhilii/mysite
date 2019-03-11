import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from .models import ReadNum,ReadDetial


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read'%(ct.model, obj.pk)
    if not request.COOKIES.get(key):
    #    if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
    #        readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
    #    else:
    #        readnum = ReadNum(content_type=ct, object_id=obj.pk)
    #   
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
    
        date = timezone.now()
    #if ReadDetial.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():
    #    readDetial = ReadDetial.objects.get(content_type=ct, object_id=obj.pk, date=date)
    #else:
    #    readDetial = ReadDetial(content_type=ct, object_id=obj.pk, date=date)
        readDetial, created = ReadDetial.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetial.read_num +=1
        readDetial.save()

    return key

def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_detials = ReadDetial.objects.filter(content_type=content_type, date=date)
        result = read_detials.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums

def get_hot_data(obj, begin_time, end_time, cache_name=None):
    if cache_name:
        hot_datas = cache.get(cache_name)
        if hot_datas is None:
            hot_datas = obj.objects \
                           .filter(read_detial__date__gte=begin_time, read_detial__date__lte=end_time) \
                           .values('id', 'title') \
                           .annotate(read_num_sum=Sum('read_detial__read_num')) \
                           .order_by('-read_num_sum')
            cache.set(cache_name, hot_datas, 3600)
    else:
        hot_datas = obj.objects \
                   .filter(read_detial__date__gte=begin_time, read_detial__date__lte=end_time) \
                   .values('id', 'title') \
                   .annotate(read_num_sum=Sum('read_detial__read_num')) \
                   .order_by('-read_num_sum')
    return hot_datas[:7]

