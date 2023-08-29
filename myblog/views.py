from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404

from myblog.models import Post, CustomCommentForm, Comment
from django.core.cache import cache
from django.http import  JsonResponse

def post_list(request):
    # Filter posts to consider only published posts
    posts = Post.objects.filter(post_status='Published')

    paginator = Paginator(posts, 3)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts}
    return render(request, 'myblog/post_list.html', context)

def censor_bad_words(comment, bad_words):
    censored_comment = comment
    for word in bad_words:
        censored_word = '*' * len(word)
        censored_comment = censored_comment.replace(word, censored_word)
    return censored_comment


def one_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment.objects.filter(active=True, post=post)
    comment_form = CustomCommentForm()
    bad_words = ['fuck', 'nigga', 'israel','shit','Bastard','Asshole','blood']

    if request.method == 'POST':
        comment_form = CustomCommentForm(request.POST)
        if comment_form.is_valid():
            email = comment_form.cleaned_data['email']
            rate_limit_key = f'comment_rate_limit_{email}'
            if cache.get(rate_limit_key):
                return JsonResponse({'error': 'You can only post one comment every 30 seconds.'})

            new_comment = Comment(
                name=comment_form.cleaned_data['name'],
                email=email,
                body=comment_form.cleaned_data['body'],
                post=post
            )

            censored_comment_body = censor_bad_words(new_comment.body, bad_words)
            new_comment.body = censored_comment_body

            new_comment.save()
            comment_form = CustomCommentForm()

            cache.set(rate_limit_key, True, 30)

    for comment in comments:
        comment.censored_comment_text = censor_bad_words(comment.body, bad_words)

    return render(request, 'myblog/one_post.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

