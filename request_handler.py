""" Request Handler Module """
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from views import get_all_tags, get_single_tag, create_tag
from views import get_all_post_tags, get_single_post_tag, add_tag_to_post, remove_tag_from_post
from views.post_requests import create_post, get_all_posts, get_single_post, delete_post, update_post
from views.user import (create_user, login_user, get_all_users,
                        get_single_user, update_user, delete_user)
from views.comments import (get_all_comments, get_single_comment, create_comment,
                            delete_comment, update_comment, get_comments_for_post)
from views.category import (create_category, get_all_categories, get_single_category,
                            update_category, delete_category)


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""
        self._set_headers(200)
        response = {}

        parsed = self.parse_url(self.path)

        if '?' not in self.path:
            (resource, id) = parsed

            if resource == "users":
                if id is not None:
                    response = get_single_user(id)
                else:
                    response = get_all_users()
            if resource == "tags":
                if id is not None:
                    response = get_single_tag(id)
                else:
                    response = get_all_tags()

            if resource == "posttags":
                if id is not None:
                    response = get_single_post_tag(id)
                else:
                    response = get_all_post_tags()
            if resource == "posts":
                if id is not None:
                    response = get_single_post(id)
                else:
                    response = get_all_posts()

            if resource == "categories":
                if id is not None:
                    response = get_single_category(id)
                else:
                    response = get_all_categories()
            if resource == 'comment':
                if id is not None:
                    response = get_comments_for_post(id)
                else:
                    response = get_all_comments()

        self.wfile.write(json.dumps(response). encode())

    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        resource, _ = self.parse_url(self.path)

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)
        if resource == 'tags':
            response = create_tag(post_body)
        if resource == 'post_tags':
            response == add_tag_to_post(post_body)
        if resource == 'posts':
            resource = create_post(post_body)
        if resource == 'categories':
            response = create_category(post_body)
        if resource == 'comment':
            response = create_comment(post_body)

        self.wfile.write(response.encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # set default value of success
        success = False

        if resource == "comment":
            success = update_comment(id, post_body)
        if resource == "posts":
            success = update_post(id, post_body)

        if resource == "users":
            # will return either True or False from `update_user`
            success = update_user(id, post_body)

        if resource == "comment":
            success = update_comment(id, post_body)
        if resource == "categories":
            success = update_category(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handle DELETE Requests"""
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)

        if resource == "comment":
            delete_comment(id)
        if resource == "posts":
            delete_post(id)
        if resource == "users":
            delete_user(id)

        if resource == "comment":
            delete_comment(id)
        if resource == "categories":
            delete_category(id)

        if resource == "post_tags":
            remove_tag_from_post(id)

        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
