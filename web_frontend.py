from flask import Flask, jsonify
import slack2linkedin

app = Flask(__name__)

INDEX_HTML = """\
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>Slack2LinkedIn</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2em; }
        textarea { width: 100%; height: 200px; margin-top: 1em; }
        button { margin-top: 1em; }
    </style>
</head>
<body>
    <h1>Slack2LinkedIn</h1>
    <button id='convert'>Convert clipboard</button>
    <textarea id='text'></textarea>
    <button id='copy'>Copy to clipboard</button>
    <script>
        document.getElementById('convert').onclick = async function() {
            const res = await fetch('/convert');
            const data = await res.json();
            document.getElementById('text').value = data.text;
        };
        document.getElementById('copy').onclick = function() {
            const text = document.getElementById('text').value;
            navigator.clipboard.writeText(text);
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return INDEX_HTML

@app.route('/convert')
def convert():
    text, _ = slack2linkedin.convert_clipboard()
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(debug=True)

