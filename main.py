from flask import Flask, render_template_string, request, send_file
import moviepy.editor as mp
import os

app = Flask(__name__)

# वीडियो प्रोसेसिंग फंक्शन
def process_video(input_path, mode):
    video = mp.VideoFileClip(input_path)
    
    # मोड के आधार पर क्लिप काटें
    if mode == 'shorts':
        # शॉर्ट्स के लिए 45 सेकंड का सबसे इंटेंस हिस्सा (शुरुआत से)
        clip = video.subclip(0, 45)
    else:
        # लॉन्ग फॉर्म के लिए 5 मिनट के बड़े हिस्से
        clip = video.subclip(0, 300)
    
    # वायरल लुक: ज़ूम (1.1x) और कलर कॉन्ट्रास्ट (1.2x)
    clip = clip.resize(1.1).fx(mp.vfx.colorx, 1.2)
    
    # टेक्स्ट ओवरले: वायरल स्टाइल
    txt = mp.TextClip("INTENSE MOMENT | MUST WATCH", fontsize=50, color='yellow', font='Arial-Bold', bg_color='black')
    txt = txt.set_position(('center', 'top')).set_duration(clip.duration)
    
    # फाइनल कंपोजिट
    result = mp.CompositeVideoClip([clip, txt])
    output_path = "output_viral.mp4"
    result.write_videofile(output_path, codec="libx264")
    return output_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        mode = request.form.get('mode')
        file.save('raw.mp4')
        output = process_video('raw.mp4', mode)
        return send_file(output, as_attachment=True)
    
    # वेबसाइट का सिंपल और क्लीन डिजाइन
    return """
    <body style="background:#111; color:white; text-align:center; padding:50px; font-family:sans-serif;">
        <h1>Viral Bodycam Engine</h1>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file" required><br><br>
            <select name="mode">
                <option value="shorts">Shorts Mode (Viral Clips)</option>
                <option value="long">Long-form Mode (Narrative)</option>
            </select><br><br>
            <button type="submit" style="padding:15px 30px; background:red; border:none; color:white; font-weight:bold; cursor:pointer;">Generate Viral Video</button>
        </form>
    </body>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

