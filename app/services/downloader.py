import yt_dlp
import os
from datetime import datetime
from app.services.history import HistoryManager

# CONVERSION
def format_filesize(bytes_size):
    if not bytes_size:
        return "Bilinmiyor"
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0

def format_duration(seconds):
    if not seconds: return "00:00"
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{f'{h:d}:' if h else ''}{m:02d}:{s:02d}"

def format_views(count):
    if not count: return "0"
    for unit, divisor in [('B',1000000000), ('M',1000000), ('K',1000)]:
        if count>= divisor:
            return f"{count/divisor:.1f}{unit}"
    return str(count)

# VIDEO ANALYZE
def fetch_video_info(url):
    ydl_opts = { 'quiet': True, 'no_warnings': True }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        
        thumbnails = info.get('thumbnails', [])
        thumbnail_url = thumbnails[-1]['url'] if thumbnails else info.get('thumbnail')
        
        qualities = []
        formats = info.get('formats', [])
        
        for f in formats:
            if f.get('ext') != 'mp4': continue
            if f.get('vcodec') == 'none': continue
            if f.get('protocol') not in ['https', 'http', 'm3u8_native', 'm3u8']: continue
            
            height = f.get('height')
            if not height or height <= 0: continue

            filesize = f.get('filesize') or f.get('filesize_approx')
            note = f.get('format_note', '')
            resolution_label = str(note) if note and 'p' in str(note) else f"{height}p"

            fmt_id = f['format_id']
            if f.get('acodec') == 'none':
                fmt_id = f"{fmt_id}+bestaudio"

            qualities.append({
                "format_id": fmt_id,
                "resolution": resolution_label,
                "filesize": format_filesize(filesize),
                "height": height
            })
        
        qualities = sorted(qualities, key=lambda x: x['height'], reverse=True)
        
        seen_resolutions = set()
        unique_qualities = []
        for q in qualities:
            if q['resolution'] not in seen_resolutions:
                unique_qualities.append(q)
                seen_resolutions.add(q['resolution'])

        return {
            "status": "success",
            "title": info.get('title'),
            "thumbnail": thumbnail_url,
            "duration": format_duration(info.get('duration')),
            "views": format_views(info.get('view_count')),
            "channel": info.get('uploader'),
            "video_id": info.get('id'),
            "qualities": unique_qualities
        }

download_tasks = {}
# PROGRESS HOOK
def download_worker(task_id: str, url: str, type: str, title: str, thumbnail: str, format_id: str = None):
    try:
        download_tasks[task_id] = {
            "status": "processing",
            "progress": "0%",
            "filepath": None
        }

        def progress_hook(d):
            if d['status'] == 'downloading':
                try:
                    p = d.get('_percent_str', '0%').replace('%','')
                    download_tasks[task_id]["progress"] = f"{float(p):.1f}%"
                except:
                    pass
            elif d['status'] == 'finished':
                download_tasks[task_id]["progress"] = "100%"

        output_template = f"downloads/{task_id}.%(ext)s"
        os.makedirs("downloads", exist_ok=True)

        ydl_opts = {
            'quiet': True,
            'outtmpl': output_template,
            'progress_hooks': [progress_hook],
            'nocheckcertificate': True,
        }

        if type == 'audio':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        elif format_id:
            ydl_opts.update({
                'format': format_id,
                'merge_output_format': 'mp4'
            })
        else:
            ydl_opts.update({
                'format': 'best[ext=mp4]/best',
                'merge_output_format': 'mp4'
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Check file existence fallback
            if not os.path.exists(filename):
                for f in os.listdir("downloads"):
                    if f.startswith(task_id):
                        filename = os.path.join("downloads", f)
                        break
            
            download_tasks[task_id]["status"] = "completed"
            download_tasks[task_id]["filepath"] = filename
            
            # Add to History only on success
            HistoryManager.save({
                "id": task_id,
                "title": title,
                "thumbnail": thumbnail,
                "type": type,
                "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
                "url": url,
                "file_path": filename
            })

    except Exception as e:
        download_tasks[task_id]["status"] = "error"
        download_tasks[task_id]["error"] = str(e)