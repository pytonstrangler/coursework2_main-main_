from flask import *

import functions

app = Flask("mini_insta")


@app.route("/")
def main_page():
    posts_data = functions.open_json("../data/data.json")
    comments_data = functions.open_json("../data/comments.json")
    bookmarks = functions.open_json("../data/bookmarks.json")

    posts_data = functions.string_crop(posts_data)
    posts_data = functions.comments_count(posts_data, comments_data)

    bookmarks_quantity = len(bookmarks)

    return render_template("index.html", posts=posts_data, bookmarks_quantity=bookmarks_quantity)


@app.route("/posts/<postid>")
def post_page(postid):
    posts_data = functions.open_json("../data/data.json")
    comments_data = functions.open_json("../data/comments.json")
    postid = int(postid)
    output_post = functions.get_post_by_pk(posts_data, postid)
    tags = functions.get_tags(output_post)

    output_comments = functions.get_comments_by_post_id(comments_data, postid)

    comments_quantity = len(output_comments)
    return render_template("post.html", post=output_post, comments=output_comments, quantity=comments_quantity,
                           tags=tags)


@app.route("/search/")
def search_page():
    posts_data = functions.open_json('../data/data.json')
    comments_data = functions.open_json('../data/comments.json')

    s = request.args.get('s')
    if s is None:
        return 'Введите параметр для поиска'

    match = functions.search_for_posts(posts_data, s)
    posts = functions.comments_count(match, comments_data)
    if len(match):
        quantity = len(match)
        return render_template('search.html', posts=posts, s=s, quantity=quantity)
    return 'Ничего не найдено'


@app.route('/users/<username>')
def user_feed(username):
    posts_data = functions.open_json('../data/data.json')
    comments_data = functions.open_json('../data/comments.json')

    match = functions.get_posts_by_user(posts_data, username)
    posts = functions.comments_count(match, comments_data)
    print(len(posts))
    return render_template('user-feed.html', posts=posts)


@app.route('/tag/<tagname>')
def tag_page(tagname):
    posts_data = functions.open_json('../data/data.json')

    tagname = '#' + tagname
    output_posts = []
    for post in posts_data:
        text = post['content'].split(' ')
        if tagname in text:
            output_posts.append(post)

    return render_template('tag.html', output_posts=output_posts, tagname=tagname)


@app.route('/bookmarks/add/<postid>')
def add_bookmark(postid):
    postid = int(postid)
    # posts_data = functions.open_json('data/bookmarks.json')

    bookmarked_posts = functions.open_json('../data/bookmarks.json')
    for bookmark in bookmarked_posts:
        if postid == bookmark['pk']:
            return redirect('/', code=302)


@app.route('/bookmarks/remove/<postid>')
def remove_bookmark(postid):
    postid = int(postid)
    bookmarks = functions.open_json('../data/bookmarks.json')

    for bookmark in bookmarks:
        if postid == bookmark['pk']:
            bookmarks.remove(bookmark)

    functions.write_json('../data/bookmarks.json', bookmarks)
    return redirect('/', code=302)


@app.route('/api/posts/')
def api_posts():
    posts_data = functions.open_json("../data/data.json")
    return jsonify(posts_data)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


@app.errorhandler(500)
def resource_not_found(e):
    return jsonify(error=str(e)), 500


@app.route("/bookmarks")
def bookmarks_page():
    bookmarks = functions.open_json('../data/bookmarks.json')
    comments_data = functions.open_json('../data/comments.json')

    bookmarks = functions.string_crop(bookmarks)
    bookmarks = functions.comments_count(bookmarks, comments_data)

    return render_template('bookmarks.html', bookmarks=bookmarks)


if __name__ == "__main__":
    app.run(debug=True)
