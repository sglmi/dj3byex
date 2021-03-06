from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings


from .forms import EmailPostForm, CommentForm
from .models import Post, Comment


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        status="published",
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == "POST":
        # create comment form with received data
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comment_form": comment_form,
            "comments": comments,
            "new_comment": new_comment,
        },
    )


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/post/list.html", {"page": page, "posts": posts})


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="published")
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # forma data
            name = form.cleaned_data["name"]
            to = form.cleaned_data["to"]
            comments = form.cleaned_data["comment"]

            # email message construction
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{name} recommends you to read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{name}'s comments {comments}"

            # send mail
            send_mail(subject, message, settings.EMAIL_HOST_USER, [to])
            sent = True

        else:
            # the form is invalid!
            pass
    else:
        form = EmailPostForm()

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )
