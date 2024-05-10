import http.server
import socketserver
import tkinter as tk
from tkinter import messagebox
import threading

class WebServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Local Web Server")
        
        self.port_label = tk.Label(root, text="Port:")
        self.port_label.grid(row=0, column=0, padx=10, pady=10)

        self.port_entry = tk.Entry(root)
        self.port_entry.insert(0, "4488")  # Default port
        self.port_entry.grid(row=0, column=1, padx=10, pady=10)

        self.start_button = tk.Button(root, text="Start Server", command=self.start_server)
        self.start_button.grid(row=1, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(root, text="Stop Server", command=self.stop_server, state=tk.DISABLED)
        self.stop_button.grid(row=1, column=1, padx=10, pady=10)

        self.server_thread = None

    def start_server(self):
        try:
            port = int(self.port_entry.get())
            Handler = self.get_handler()

            self.httpd = socketserver.TCPServer(("", port), Handler)
            self.server_thread = threading.Thread(target=self.httpd.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()

            messagebox.showinfo("Server Info", f"Server started at localhost:{port}")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def stop_server(self):
        try:
            if self.httpd:
                self.httpd.shutdown()
                self.httpd.server_close()
                self.server_thread.join()
                messagebox.showinfo("Server Info", "Server stopped")
                self.start_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_handler(self):
        class CustomHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"<html><head><title>Login Page</title></head>")
                    self.wfile.write(b"<body>")
                    self.wfile.write(b"<h1>Login</h1>")
                    self.wfile.write(b"<form method='post' action='/login'>")
                    self.wfile.write(b"<label>Username:</label><br>")
                    self.wfile.write(b"<input type='text' name='username'><br>")
                    self.wfile.write(b"<label>Password:</label><br>")
                    self.wfile.write(b"<input type='password' name='password'><br><br>")
                    self.wfile.write(b"<input type='submit' value='Login'>")
                    self.wfile.write(b"</form>")
                    self.wfile.write(b"</body></html>")
                else:
                    super().do_GET()

            def do_POST(self):
                if self.path == '/login':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length).decode('utf-8')
                    post_data = dict(x.split('=') for x in post_data.split('&'))
                    username = post_data.get('username')
                    password = post_data.get('password')
                    if username == 'admin' and password == 'admin123':  # Replace with actual authentication logic
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(b"<html><head><title>Welcome</title></head>")
                        self.wfile.write(b"<body><h1>Welcome, admin!</h1></body></html>")
                    else:
                        self.send_response(401)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(b"<html><head><title>Unauthorized</title></head>")
                        self.wfile.write(b"<body><h1>Unauthorized Access!</h1></body></html>")
                else:
                    super().do_POST()

        return CustomHandler

def main():
    root = tk.Tk()
    app = WebServerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
