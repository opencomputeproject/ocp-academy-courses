"""Serve the real course pages locally, with byte ranges for video seeking."""
import argparse
import os
import re
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CoursePreview(SimpleHTTPRequestHandler):
    def end_headers(self):
        # Course media retain stable names across editorial revisions. A local
        # preview must re-read the bytes instead of holding an earlier clip.
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def send_head(self):
        self.byte_range = None
        path = Path(self.translate_path(self.path))
        header = self.headers.get('Range')
        if not header or not path.is_file():
            return super().send_head()
        match = re.fullmatch(r'bytes=(\d*)-(\d*)', header)
        if not match or not any(match.groups()):
            self.send_error(416)
            return None
        size = path.stat().st_size
        left, right = match.groups()
        start = int(left) if left else max(0, size - int(right))
        end = min(int(right), size - 1) if left and right else size - 1
        if start > end or start >= size:
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{size}')
            self.end_headers()
            return None
        stream = path.open('rb')
        self.byte_range = start, end
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(str(path)))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(end - start + 1))
        self.send_header('Last-Modified', self.date_time_string(path.stat().st_mtime))
        self.end_headers()
        stream.seek(start)
        return stream

    def copyfile(self, source, output):
        try:
            if self.byte_range is None:
                return super().copyfile(source, output)
            remaining = self.byte_range[1] - self.byte_range[0] + 1
            while remaining:
                data = source.read(min(65536, remaining))
                if not data:
                    break
                output.write(data)
                remaining -= len(data)
        except (BrokenPipeError, ConnectionResetError):
            pass  # A normal browser seek cancels the preceding media request.


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8876)
    parser.add_argument('--directory', type=Path, default=ROOT.parents[1]/'build'/ROOT.name)
    args = parser.parse_args()
    os.chdir(args.directory.resolve())
    server = ThreadingHTTPServer(('127.0.0.1', args.port), CoursePreview)
    print(f'Course preview: http://127.0.0.1:{args.port}/index.html?review=1', flush=True)
    server.serve_forever()
