from django.shortcuts import render
from .models import LikeRecord, LikeCount
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse

def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def SucceedResponse(like_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['like_num'] = like_num
    return JsonResponse(data)

def like_change(request):
    print(request.GET)
    # 判断是否登录
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, '尚未登录')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except:
        return ErrorResponse(401, '点赞对象不存在')

    if request.GET.get('is_like') == 'true':
        # 点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 未点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_num +=1
            like_count.save()
            return SucceedResponse(like_count.like_num)
        else:
            # 已经点赞
            return ErrorResponse('402', '你已经点赞')
    else:
        # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.like_num -=1
                like_count.save()
                return SucceedResponse(like_count.like_num)
            else:
                return ErrorResponse(404, '数据出错')
        else:
            return ErrorResponse(403, '你未点赞')