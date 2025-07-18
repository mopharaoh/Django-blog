from django.shortcuts import render,get_object_or_404,HttpResponsePermanentRedirect
from .models import Post,Comment,Category
from .forms import Newcomment,PostSearchForm
from django.views.generic import ListView
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.core import serializers
# Create your views here.


def home(request):

    posts=Post.newmanager.all()

    return render(request,'index.html',{'posts':posts})

def post_single(request,post):
    post=get_object_or_404(Post,slug=post,status='published')

    allcomments=post.comments.filter(status=True)
    page=request.GET.get('page',1)
    paginator=Paginator(allcomments,3)

    try:
        comments=paginator.page(page)
    except PageNotAnInteger:
        comments=paginator.page(1)
    except EmptyPage:
        comments=paginator.page(paginator.num_pages)

    user_comment=None
    if request.method == 'POST':
        comment_form=Newcomment(request.POST)
        if comment_form.is_valid():
            user_comment=comment_form.save(commit=False)
            user_comment.post=post
            user_comment.save()
            return HttpResponsePermanentRedirect('/'+post.slug)
    else:
        comment_form=Newcomment()

    return render(request,'single.html',
                  {'post':post,'user_comment':user_comment,
                   'comments':comments,'comment_form':comment_form,'allcomments':allcomments})


class CatListView(ListView):
    template_name='category.html'
    context_object_name='catlist'

    def get_queryset(self):
        content={
            'cat':self.kwargs['category'],
            'posts':Post.objects.filter(category__name=self.kwargs['category']).filter(status='published')
        }
        return content


def category_list(request):
    category_list=Category.objects.exclude(name='default')
    context={
        "category_list":category_list,
    }
    return context

def postSearch(request):
    form=PostSearchForm()
    q=''
    c=''
    results=[]
    query=Q()

    if request.POST.get('action')=='post':
        search_string=str(request.POST.get('ss'))

        if search_string is not None:
            search_string=Post.objects.filter(title__contains=search_string)[:5]
            data=serializers.serialize('json',list(search_string),fields=('id','title','slug'))

        return JsonResponse({'search_string':data})
    
    if 'q' in request.GET:
        form=PostSearchForm(request.GET)
        if form.is_valid():
            q=form.cleaned_data['q']
            c=form.cleaned_data['c']
            
            if c is not None:
                query &=Q (category=c)
            if q is not None:
                query &= Q(title__contains=q)

            results=Post.objects.filter(query)


    return render(request,'search.html',
                  {'form':form,'q':q,
                   'results':results})