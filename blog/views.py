from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read

def get_page_list(current_num, max_num):
    l_num = max(1, current_num-2)
    r_num = min(max_num + 1, current_num + 3)
    if l_num == 1:
        r_num = min(max_num + 1, 6)
    elif r_num == max_num + 1:
        l_num = max(r_num - 5, 1)
    page_num = list(range(l_num, r_num))
    if page_num[0] >= 3:
        page_num.insert(0, '...')
    if page_num[-1] <= max_num-2:
        page_num.append('...')
    if page_num[0] != 1:
        page_num.insert(0, 1)
    if page_num[-1] != max_num:
        page_num.append(max_num)
    return page_num

def get_blogs_with_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, 7) #每页数量
    page_num = request.GET.get('page', 1) # 获取URL页面参数
    page_of_blogs = paginator.get_page(page_num)
    current_page_num = page_of_blogs.number #获取当前页
    page_range =  get_page_list(current_page_num, paginator.num_pages)
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, 
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    context = {} 
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blogs_with_common_data(request, blogs_all_list)
    
    return render(request, 'blog/blog_list.html', context)

def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blogs_with_common_data(request, blogs_all_list)

    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)

def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blogs_with_common_data(request, blogs_all_list)

    context['blog_with_date'] = '%s年%s月'%(year, month)
    return render(request, 'blog/blogs_with_date.html', context)

def blog_detial(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog)

    context = {}
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    context['blog'] =blog
    response =  render(request, 'blog/blog_detial.html', context)
    response.set_cookie(read_cookie_key, 'true')
    return response