from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import current_user, login_required
from app.models import Post, User
from .forms import PostForm

ig = Blueprint('ig', __name__, template_folder='ig_templates')

@ig.route('/posts/create', methods=["GET", "POST"])
@login_required
def createPost():
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post = Post(title, img_url, caption, current_user.id)

            post.saveToDB()

            return redirect(url_for('homePage'))

    return render_template('create_post.html', form = form)

@ig.route('/posts')
def viewPosts():
    posts = Post.query.order_by(Post.date_created).all()[::-1]
    for p in posts:
        p.like_counter = len(p.liked.all())
    return render_template('feed.html', posts=posts)

@ig.route('/posts/<int:post_id>')
def viewSinglePost(post_id):
    # post = Post.query.filter_by(id = post_id).first()

    post = Post.query.get(post_id)

    if post:
        return render_template('single_post.html', post = post)
    else:
        return redirect(url_for('ig.viewPosts'))

@ig.route('/posts/<int:post_id>/update', methods=["GET", "POST"])
@login_required
def updatePost(post_id):
    post = Post.query.filter_by(id = post_id).first()
    if current_user.id != post.user_id:
        print("You cannot update another user's posts.")
        return redirect(url_for('ig.viewPosts'))

    form = PostForm()

    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post.updateInfo(title,img_url,caption)

            post.saveChanges()

            return redirect(url_for('ig.viewSinglePost', post_id=post_id))

    return render_template('update_post.html', form = form, post = post)

@ig.route('/posts/<int:post_id>/delete', methods=["GET"])
def deletePost(post_id):
    post = Post.query.get(post_id)
    if current_user.id == post.user_id:
        post.deleteFromDB()
    else:
        print("You cannot delete another user's posts.")
    return redirect(url_for('ig.viewPosts'))
    

@ig.route('/follow/<int:user_id>')
@login_required
def followUser(user_id):
    user = User.query.get(user_id)
    if user:

        current_user.follow(user)
        flash(f'Successfully followed {user.username}.', 'success')
    else:
        flash(f'That user does not exist', 'danger')

    return redirect(url_for('homePage'))

@ig.route('/unfollow/<int:user_id>')
@login_required
def unfollowUser(user_id):
    user = User.query.get(user_id)
    if user:
        current_user.unfollow(user)
        flash(f'Successfully unfollowed {user.username}.', 'success')
    else:
        flash(f'That user does not exist', 'danger')

    return redirect(url_for('homePage'))

@ig.route('/like/<int:post_id>')
def likePost(post_id):
    post = Post.query.get(post_id)
    my_likes = current_user.liked
    if post in my_likes:
        flash('You already liked that!', 'danger')
    else:
        post.like(current_user)

    return redirect(url_for('ig.viewPosts'))