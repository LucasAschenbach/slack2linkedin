# slack2linkedin
A script converting HTML- or RTF-formatted text to unicode text. In particular, you can convert text copied from slack into properly formatted LinkedIn posts with preserved styling, e.g. bold and italic text.

## Usage

### uv

Before the first run, execute the following command with your shell in the project root directory to make the file executable:

```bash
chmod +x slack2linkedin/cli.py
```

In order to run the program simply run

```bash
./slack2linkedin/cli.py
```

uv will automatically install all necessary dependencies in the background.

### pip

If you are not using uv to manage your python installations, manually install the dependencies using

```bash
pip install -r requirements.txt
```

Then you can run the script as you would any python program

```bash
python slack2linkedin/cli.py
```

### pipx

To run the script with temporary dependencies run

```bash
pipx run --spec emoji,beautifulsoup4,PyQt5 python slack2linkedin/cli.py
```

### Web Frontend

Copy the `slack2linkedin/convert.py` file to the `public/` directory.

Then, open the `public/index.html` file in your browser.

The script will be run in the browser using Pyodide.
