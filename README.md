# slack2linkedin
A script converting HTML- or RTF-formatted text to unicode text. In particular, you can convert text copied from slack into properly formatted LinkedIn posts with preserved styling, e.g. bold and italic text.

## Usage

### uv

Before the first run, execute the following command with your shell in the project root directory to make the file executable:

```bash
chmod +x slack2linkedin.py
```

In order to run the program simply run

```bash
./slack2linkedin.py
```

uv will automatically install all necessary dependencies in the background.

### pip

If you are not using uv to manage your python installations, manually install the dependencies using

```bash
pip install -r requirements.txt
```

Then you can run the script as you would any python program

```bash
python slack2linkedin.py
```

### pipx

To run the script with temporary dependencies run

```bash
pipx run --spec emoji,beautifulsoup4,PyQt5 python slack2linkedin.py
```

### Web Frontend

To start a small local web interface run

```bash
python web_frontend.py
```

Open your browser at `http://127.0.0.1:5000` and use the **Convert** button to
grab the clipboard text and convert it. The resulting text is shown in a
textarea where it can be edited. Clicking **Copy to clipboard** writes the
content back to your clipboard.
