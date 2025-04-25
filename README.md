# slack2linkedin
A script converting HTML- or RTD-formatted text to unicode text. In particular, you can convert text copied from slack into properly formatted LinkedIn posts.

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