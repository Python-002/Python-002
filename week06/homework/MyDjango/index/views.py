from django.shortcuts import render

# Create your views here.
from .models import MovieTbl

def movies_short(request):
    # 获取request的查询内容
    q = request.GET.get('q')
    shorts = MovieTbl.objects.all()
    # 多条件筛选，实现查询功能
    if q:
        conditions = {
            'movie_star__gt':3,
            'movie_comment__icontains':q
        }
    else:
        conditions = {'movie_star__gt':3}
    good_shorts = shorts.filter(**conditions)

    return render(request,'index.html',locals())
