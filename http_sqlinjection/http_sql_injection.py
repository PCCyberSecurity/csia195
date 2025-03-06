from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.parse
import sqlite3
import colorama

# ******** WARNING ********
# This is a vulnerable web server that is susceptible to SQL Injection attacks. It is vulnerable on purpose
# DO NOT USE IN PRODUCTION!

# Let us use colors in our text
colorama.init(autoreset=True)

def setup_database():
    print(colorama.Fore.GREEN + f"Setting up database...")
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row  # Enable column name access
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT unique, 
            password TEXT, 
            age INTEGER, 
            is_admin BOOLEAN
        )
    """)
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, age, is_admin) 
        VALUES ('admin', 'password123', 30, 1)
    """)
    cursor.execute("""
        INSERT OR IGNORE INTO users (username, password, age, is_admin) 
        VALUES ('user', 'userpass', 25, 0)
    """)
    conn.commit()
    conn.close()

setup_database()

class MyHandler(BaseHTTPRequestHandler):
    
    # HTML templates for pages
    templates = {
        "default_layout": '''
            <html>
            <head>
            <title>{{title}}</title>
            </head>
            <body>
            {{body}}
            </body>
            </html>

            ''',

        "default_page": '''
            <h2>Welcome to Friendbook</h2>
            <a href='/login'>Login</a>
            {{message}}
            ''',

        "404_page": '''
            <h2>Page Not Found!</h2>
            ''',

        "login_page": '''
            <h2>Login</h2>
            <form method="post" action="/login">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
            </form>
            ''',
        
        "profile_page": '''
            <h2>Profile Page</h2>
            <p>{{name}}</p>
            ''',
        
        "userlist_page": '''
            <h1>User List</h1>
            <table border="1">
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Age</th>
                    <th>Is Admin</th>
                </tr>
                {{user_rows}}
            </table>
        '''

    }
    
    # Build template from text
    def merge_template(self, page_template="default_page", layout="default_layout", page_values=dict()):
        if page_values is None:
            page_values = {}
        
        # Set default values for page_values
        page_values.setdefault("message", "")
        page_values.setdefault("title", "Default Title")

        # Get layout and page templates, use default if not found
        layout_html = MyHandler.templates.get(layout, MyHandler.templates["default_layout"])
        
        page_html = MyHandler.templates.get(page_template, MyHandler.templates["default_page"])
        
        # Start with our layout (whole page)
        final_html = layout_html

        # Add in our page content
        final_html = final_html.replace("{{body}}", page_html)

        # Now add in our page values
        for key, val in page_values.items():
            # We replace each item (e.g. {{name}} in the text with its value - Bob)
            final_html = final_html.replace("{{" + key + "}}", str(val))
        
        return final_html


    # Handle GET requests
    def do_GET(self):
        if self.path == "/":
            print(colorama.Fore.YELLOW + f"Serving Page: /")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.merge_template().encode())
            
        elif self.path == "/login":
            print(colorama.Fore.YELLOW + f"Serving Page: /login")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.merge_template(page_template="login_page").encode())
        elif self.path.startswith("/profile/"):
            print(colorama.Fore.YELLOW + f"Serving Page: /profile")
            profile_id = self.path.split("/profile/")[1]
            if profile_id is None or profile_id == "":  # No ID provided
                self.send_response(404)
                self.end_headers()
                self.wfile.write(self.merge_template(page_template="404_page").encode())
                return
            # ************** NOTE - We need to add validation to this!! If this is supposed to only be an integer number,
            # we could do somehitng like this: profile_id = int(profile_id)
            # Or we could also remove extra characters like ' from the string or encode it so that it doesn't
            # break the database.
            # Ultimatly - we should use "Parameterized Queries" to prevent SQL Injection

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
             # Vulnerable SQL query (do not use in production)
            conn = sqlite3.connect("users.db")
            conn.row_factory = sqlite3.Row  # Enable column name access
            cursor = conn.cursor()
            query = f"SELECT * FROM users WHERE id='{profile_id}'"
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            page_values = {
                "name": result["username"],
                "id": result["id"],
                "age": result["age"],
                "is_admin": result["is_admin"]
            }
            self.wfile.write(self.merge_template(page_template="profile_page", page_values=page_values).encode())
        
        elif self.path == "/userlist":
            print(colorama.Fore.YELLOW + f"Serving Page: /userlist")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            conn = sqlite3.connect("users.db")
            conn.row_factory = sqlite3.Row  # Enable column name access
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            conn.close()

            user_rows = ""
            for user in users:
                user_rows += f"<tr><td>{user['id']}</td><td>{user['username']}</td><td>{user['age']}</td><td>{user['is_admin']}</td></tr>"

            page_values = {
                "user_rows": user_rows
            }
            self.wfile.write(self.merge_template(page_template="userlist_page", page_values=page_values).encode())

        else:
            print(colorama.Fore.YELLOW + f"Serving Page: 404")
            self.send_response(404)
            self.end_headers()
            self.wfile.write(self.merge_template(page_template="404_page").encode())

    # Handle POST requests
    def do_POST(self):
        if self.path == "/login":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            fields = urllib.parse.parse_qs(post_data.decode())

            # Extracting user input
            username = fields.get('username', [''])[0]
            password = fields.get('password', [''])[0]

            # ************** NOTE - We need to add validation to this!! 
            # We could remove extra characters like ' from the string or encode it so that it doesn't
            # break the database.
            # Ultimatly - we should use "Parameterized Queries" to prevent SQL Injection

            # Vulnerable SQL query (do not use in production)
            conn = sqlite3.connect("users.db")
            conn.row_factory = sqlite3.Row  # Enable column name access
            cursor = conn.cursor()
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()

            if result:
                id = result["id"]
                self.send_response(302)
                self.send_header("Location", f"/profile/{id}")
                self.end_headers()
            else:
                # Invalid credentials response
                self.send_response(401)
                self.end_headers()
                self.wfile.write(b"Login failed. Invalid credentials.")
        else:
            self.send_response(404)
            self.end_headers()

# Run the server
def run(server_class=ThreadingHTTPServer, handler_class=MyHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting http server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
