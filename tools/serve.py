# -*- coding: utf-8 -*-
import functools, http.server, sys
from pathlib import Path
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8871
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(Path(__file__).resolve().parent.parent / "docs"))
http.server.ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
