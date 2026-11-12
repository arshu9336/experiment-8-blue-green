import os
from http.server import BaseHTTPRequestHandler, HTTPServer

COLOR = os.getenv("COLOR", "BLUE").upper()
VERSION = os.getenv("APP_VERSION", "1.0")
BUILD = os.getenv("BUILD_NUMBER", "local")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
            return

        if self.path == "/version":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                f'{{"environment":"{COLOR}","version":"{VERSION}","build":"{BUILD}","status":"healthy"}}'.encode()
            )
            return

        bg = "#1769ff" if COLOR == "BLUE" else "#16a36a"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>DeployFlow | Blue-Green Dashboard</title>
          <style>
            * {{ box-sizing: border-box; }}
            body {{
              margin: 0; font-family: Arial, sans-serif;
              background: #0b1220; color: #f8fafc;
            }}
            header {{
              padding: 25px 8%; border-bottom: 1px solid #263449;
              display: flex; justify-content: space-between; align-items: center;
            }}
            .logo {{ font-size: 23px; font-weight: bold; }}
            main {{ max-width: 950px; margin: 65px auto; padding: 20px; }}
            .tag {{ color: #94a3b8; letter-spacing: 3px; }}
            h1 {{ font-size: clamp(34px, 6vw, 55px); }}
            .card {{
              background: #172337; padding: 35px;
              border-radius: 18px; margin-top: 35px;
              border: 1px solid #334155;
            }}
            .environment {{
              display: inline-block; background: {bg};
              padding: 12px 28px; border-radius: 30px;
              font-size: 23px; font-weight: bold;
            }}
            .grid {{
              display: grid; grid-template-columns: repeat(auto-fit,minmax(180px,1fr));
              gap: 15px; margin-top: 30px;
            }}
            .item {{
              background: #0f1b2e; padding: 22px;
              border-radius: 12px;
            }}
            .value {{ font-size: 22px; font-weight: bold; margin-top: 12px; }}
            .healthy {{ color: #4ade80; }}
            footer {{ color: #94a3b8; margin-top: 40px; }}
          </style>
        </head>
        <body>
          <header>
            <div class="logo">DeployFlow</div>
            <div>DevOps Deployment Platform</div>
          </header>
          <main>
            <div class="tag">EXPERIMENT 08 / AUTOMATED DEPLOYMENT</div>
            <h1>Blue-Green Deployment</h1>
            <p>Seamless application releases powered by Jenkins,
               Docker and Kubernetes.</p>
            <section class="card">
              <p>ACTIVE APPLICATION ENVIRONMENT</p>
              <div class="environment">{COLOR}</div>
              <div class="grid">
                <div class="item">
                  <div>Application Version</div>
                  <div class="value">{VERSION}</div>
                </div>
                <div class="item">
                  <div>Build Number</div>
                  <div class="value">{BUILD}</div>
                </div>
                <div class="item">
                  <div>Deployment Health</div>
                  <div class="value healthy">HEALTHY</div>
                </div>
              </div>
            </section>
            <footer>
              Automated Blue-Green Deployment | Jenkins + Docker + Kubernetes
            </footer>
          </main>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
