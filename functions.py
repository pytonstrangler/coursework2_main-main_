import json


def open_json(file) -> list:
    """
    функция производит чтение данных из .json файла

    :param file: файл .json, который необходимо прочитать

    :return: Данные из файла .json
    """
    with open(file, encoding="utf-8") as f:
        json_data = json.load(f)
    return json_data


def load_posts():
    return open_json('data/posts.json')


def write_json(file, data) -> None:
    """
    функция производит запись данных в .json файл

    :param file: файл .json, в который необходимо записать данные
    :param data:  данные, которые необходимо записать
    :return: None
    """
    with open(file, encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def comments_count(posts_data, comments_data) -> list:
    """
    функция производит подсчет количества комментариев к постам

    :param posts_data: данные о размещенных на сайте постах из data.json
    :param comments_data: данные о комментариях ко всем постам из файла comments.json
    :return: обновленный список post_data с количеством комментариев для каждого поста
    """
    comments_match = []
    for post in posts_data:
        for comment in comments_data:
            if comment["post_id"] == post["pk"]:
                comments_match.append(post["pk"])
            post["comments"] = comments_match.count(post["pk"])

    return posts_data


def string_crop(posts_data) -> list:
    """
    функция производит сокращение строки до 50 символов

    :param posts_data: данные о постах, в которых необходимо сократить строку
    :return: обновленный post-data
    """
    for post in posts_data:
        post["content"] = post["content"][:100]

    return posts_data


def get_post_by_pk(posts_data, pk) -> dict:  # убрал  -> dict после скобок
    """
        функция отдает пост, который соответствует определенному идентификатору

        :param posts_data: данные о размещенных на сайте постах из data.json
        :param pk: параметр, соответствующий идентификатору
        :return: пост, соответствующий введенному идентификатору
        """
    output_post = {}
    for post in posts_data:
        if pk == post["pk"]:
            output_post = post

    return output_post


def new_get_post_by_pk(pk):
    for post in load_posts():
        if post["pk"] == pk:
            return post


def get_posts_by_user(posts_data, user_name) -> list:
    """
    функция отдает пост, который соответствует определенному пользователю

    :param posts_data: данные о размещенных на сайте постах из data.json
    :param user_name: параметр, соответствующий пользователю
    :return: пост, соответствующий введенному пользователю
    """
    output_post = []
    is_exists = False
    for post in posts_data:
        if user_name == post["poster_name"]:
            is_exists = True
            output_post.append(post)

    if not is_exists:
        raise ValueError
    return output_post


def get_comments_by_post_id(comment_data: dict, id_post: int) -> list:
    output_post = []
    for post in comment_data:
        if id_post == post["post_id"]:
            output_post.append(post)

    # if not output_post:
    #     raise ValueError

    return output_post


def search_for_posts(post_data: list, query: str) -> list:
    output_post = []
    for post in post_data:
        if query.lower() in post["content"]:
            output_post.append(post)
    return output_post


def get_tags(post) -> list:
    tags = []
    text = post["content"].split(" ")
    for word in text:
        if "#" in word:
            tag = word.replace("#", "")
            tags.append(tag)

    return tags
