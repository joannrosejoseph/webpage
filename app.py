from flask import Flask, render_template_string

app = Flask(__name__)

# This is the HTML, CSS, and JavaScript equivalent of your Python animation
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Love Heart</title>
    <style>
        body { 
            background-color: #060208; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            height: 100vh; 
            margin: 0; 
            font-family: Arial, sans-serif;
            overflow: hidden;
        }
        .heart {
            color: #e60d24;
            font-size: 50px;
            font-weight: bold;
            text-align: center;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); text-shadow: 0 0 10px #e60d24; }
            50% { transform: scale(1.1); text-shadow: 0 0 20px #ff1a33; }
            100% { transform: scale(1); text-shadow: 0 0 10px #e60d24; }
        }
        .phrases {
            color: #ffcccc;
            font-size: 20px;
            margin-top: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div>
        <div class="heart">❤️<br>I Love You</div>
        <div class="phrases" id="text-changer">Te amo</div>
    </div>

    <script>
        const phrases = [
            "I love you", "Seni seviyorum", "Te amo", "Je t'aime",
            "Ich liebe dich", "Ti amo", "Eu te amo", "Я тебя люблю",
            "사랑해", "愛してる", "我爱你", "मैं तुमसे प्यार करता हूँ"
        ];
        let i = 0;
        setInterval(() => {
            document.getElementById("text-changer").innerText = phrases[i];
            i = (i + 1) % phrases.length;
        }, 2000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    # Instead of running turtle, the server sends the HTML to the browser
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
