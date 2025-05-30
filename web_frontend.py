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
        body {
            font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', 'Fira Sans', Ubuntu, Oxygen, 'Oxygen Sans', Cantarell, 'Droid Sans', 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol', 'Lucida Grande', Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 20px 0; /* Symmetric vertical padding */
            background-color: #f3f2ef; /* LinkedIn background color */
            color: rgba(0,0,0,0.9); /* LinkedIn primary text color */
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: #ffffff; /* LinkedIn card background */
            padding: 24px;
            border-radius: 8px;
            box-shadow: 0 0 0 1px rgba(0,0,0,.15), 0 2px 3px rgba(0,0,0,.2); /* LinkedIn card shadow */
            width: 100%;
            max-width: 550px; /* Slightly adjust max-width */
            box-sizing: border-box;
        }
        h1 {
            color: rgba(0,0,0,0.9);
            font-size: 28px; /* LinkedIn-like heading size */
            font-weight: 600; /* LinkedIn heading weight */
            text-align: center;
            margin-bottom: 24px;
        }
        textarea {
            width: 100%; /* Full width within container */
            box-sizing: border-box; /* Include padding and border in the element's total width and height */
            height: 180px; /* Adjust height */
            margin-top: 16px; /* LinkedIn-like spacing */
            padding: 10px 12px;
            border: 1px solid rgba(0,0,0,0.15); /* LinkedIn input border */
            border-radius: 4px;
            font-size: 12px; /* LinkedIn input font size */
            line-height: 1.5;
            resize: vertical;
        }
        textarea:focus {
            outline: none;
            border-color: #0073b1; /* LinkedIn blue for focus */
            box-shadow: 0 0 0 1px #0073b1;
        }
        button {
            margin-top: 16px; /* LinkedIn-like spacing */
            padding: 10px 18px;
            background-color: #0073b1; /* LinkedIn primary button blue */
            color: white;
            border: none;
            border-radius: 4px; /* Slightly more rounded buttons */
            cursor: pointer;
            font-size: 16px; /* LinkedIn button font size */
            font-weight: 600; /* LinkedIn button font weight */
            transition: background-color 0.2s ease-in-out;
            display: inline-flex; /* Align icon and text if an icon was present */
            align-items: center;
            justify-content: center;
        }
        button:hover {
            background-color: #006097; /* Darker shade for hover */
        }
        button:disabled {
            background-color: #a0a0a0; /* Greyed out for disabled */
            color: #e0e0e0;
            cursor: not-allowed;
        }
        .button-group {
            display: flex;
            justify-content: flex-end; /* Align copy button to the right */
            margin-top: 20px;
        }
        #convert {
             width: 100%; /* Make convert button full width */
             margin-bottom: 8px; /* Add some space below convert button */
        }
        /* Toast Notification Styles */
        .toast {
            visibility: hidden; /* Hidden by default */
            min-width: 250px; /* Set a default minimum width */
            margin-left: -125px; /* Divide value of min-width by 2 */
            background-color: #333; /* Black background color */
            color: #fff; /* White text color */
            text-align: center; /* Centered text */
            border-radius: 4px; /* Rounded borders */
            padding: 16px; /* Padding */
            position: fixed; /* Sit on top of the page */
            z-index: 1; /* Add a z-index if needed */
            left: 50%; /* Center the snackbar */
            bottom: 30px; /* 30px from the bottom */
            font-size: 17px; /* Set a font-size */
        }

        /* Show the toast notification */
        .toast.show {
            visibility: visible; /* Show the toast */
            /* Add animation: Take 0.5 seconds to fade in and out the toast.
            However, delay the fade out process for 2.5 seconds */
            -webkit-animation: fadein 0.5s, fadeout 0.5s 2.5s;
            animation: fadein 0.5s, fadeout 0.5s 2.5s;
        }

        /* Animations to fade the toast in and out */
        @-webkit-keyframes fadein {
            from {bottom: 0; opacity: 0;}
            to {bottom: 30px; opacity: 1;}
        }

        @keyframes fadein {
            from {bottom: 0; opacity: 0;}
            to {bottom: 30px; opacity: 1;}
        }

        @-webkit-keyframes fadeout {
            from {bottom: 30px; opacity: 1;}
            to {bottom: 0; opacity: 0;}
        }

        @keyframes fadeout {
            from {bottom: 30px; opacity: 1;}
            to {bottom: 0; opacity: 0;}
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Slack2LinkedIn</h1>
        <button id='convert'>Convert Slack Text from Clipboard</button>
        <textarea id='text' placeholder="Your converted LinkedIn-style post will appear here..."></textarea>
        <div class="button-group">
            <button id='copy' disabled>Copy to Clipboard</button>
        </div>
    </div>
    <div id="toast" class="toast">Copied to clipboard!</div>
    <script>
        const textElement = document.getElementById('text');
        const copyButton = document.getElementById('copy');
        const toastElement = document.getElementById('toast');

        function updateCopyButtonState() {
            if (textElement.value.trim() === '') {
                copyButton.disabled = true;
            } else {
                copyButton.disabled = false;
            }
        }

        document.getElementById('convert').onclick = async function() {
            const res = await fetch('/convert');
            const data = await res.json();
            textElement.value = data.text;
            updateCopyButtonState(); // Update button state after conversion
        };
        copyButton.onclick = function() {
            navigator.clipboard.writeText(textElement.value);
            toastElement.className = "toast show";
            setTimeout(function(){ toastElement.className = toastElement.className.replace("show", ""); }, 3000);
        };

        textElement.addEventListener('input', updateCopyButtonState);

        // Initial check in case the textarea has pre-filled content (though unlikely here)
        updateCopyButtonState();
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
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=False, use_reloader=False)

