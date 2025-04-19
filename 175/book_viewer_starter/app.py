from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    with open("book_viewer/data/toc.txt", "r") as file:
        contents = file.readlines()
    return render_template('index.html', contents=contents)

@app.route("/chapters/1")
def chapter():
    with open("book_viewer/data/toc.txt", "r") as file:
        contents = file.readlines()
    with open("book_viewer/data/chp1.txt") as file:
        chapter = file.read()
        chapter = chapter.split("\n\n")
    return render_template('chapter.html',
                            contents=contents,
                            chapter=chapter)

if __name__ == "__main__":
    app.run(debug=True, port=5003)
