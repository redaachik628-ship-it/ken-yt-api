# احفظ هذا الملف باسم app.py وارفع على السيرفر
from flask import Flask, request, send_file, jsonify
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    download_type = request.args.get('type') # 'video' or 'audio'

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        # إعدادات التحميل بناءً على اختيار المستخدم (صوت أو فيديو)
        if download_type == 'audio':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        else:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
            }

        # إنشاء مجلد التحميلات إذا لم يكن موجوداً
        os.makedirs('downloads', exist_ok=True)

        # تحميل الفيديو باستخدام مكتبة yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            # جلب مسار الملف الذي تم تحميله
            downloaded_file_path = ydl.prepare_filename(info_dict)
            
            if download_type == 'audio':
                downloaded_file_path = downloaded_file_path.rsplit('.', 1)[0] + '.mp3'

        # إرسال الملف للمستخدم لكي يتم تحميله على هاتفه
        return send_file(downloaded_file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

