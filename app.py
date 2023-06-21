from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    """
    Renders the main page of the blog application.
    :return: Rendered HTML template
    """
    blog_posts = fetch_data()
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle the addition of a new blog post.
    """
    if request.method == 'POST':
        blog_posts = fetch_data()
        author = request.form["author"]
        title = request.form["title"]
        content = request.form["content"]
        new_post = {
            "id": blog_posts[-1]["id"] + 1,
            "author": author,
            "title": title,
            "content": content
        }
        blog_posts.append(new_post)
        update_data(blog_posts)

        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Delete a blog post based on its ID
    :param post_id: The ID of the blog post to delete
    :return: A redirect response to the index page after the post has been deleted.
    """
    blog_posts = fetch_data()
    post_to_delete = fetch_post_by_id(post_id)
    blog_posts.remove(post_to_delete)
    update_data(blog_posts)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Handle the update of a blog post.
    """
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        blog_posts = fetch_data()
        for blog_post in blog_posts:
            if blog_post["id"] == post_id:
                blog_post["author"] = request.form["author"]
                blog_post["title"] = request.form["title"]
                blog_post["content"] = request.form["content"]
        update_data(blog_posts)
        # Redirect back to index
        return redirect(url_for('index'))
    # Else, it's a GET request
    # So display the update.html page
    else:
        return render_template('update.html', post=post)


def fetch_data():
    """
    Fetch the blog post from a JSON file.
    :return:  A Python object containing the blog post data read from the 'data.json' file.
    """
    with open("data.json", "r") as fileobj:
        data = json.load(fileobj)
        return data


def update_data(data):
    """
    Update the contents of a JSON file with the provided data.
    """
    with open("data.json", "w") as fileobj:
        json.dump(data, fileobj)


def fetch_post_by_id(post_id):
    """
    Fetch a blog post by its ID.
    :param post_id: The ID of the blog post to fetch
    :return: The blog post if it matches the ID.
    """
    blog_posts = fetch_data()
    for post in blog_posts:
        if post["id"] == post_id:
            return post


if __name__ == '__main__':
    app.run(debug=True)
