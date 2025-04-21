from flask import Flask, render_template, g, redirect, request

app = Flask(__name__)

def in_paragraphs(text):
    paragraphs = text.split("\n\n")
    formatted_paragraphs = [
      f'<p>{paragraph}</p>'
      for paragraph in paragraphs
      if paragraph
    ]
    return ''.join(formatted_paragraphs)

app.jinja_env.filters['in_paragraphs'] = in_paragraphs

@app.before_request
def load_contents():
    with open("book_viewer/data/toc.txt", "r") as file:
        g.contents = file.readlines()

@app.route("/")
def index():
    return render_template('home.html', contents=g.contents)

@app.route("/chapters/<page_num>")
def chapter(page_num):
    chapter_name = g.contents[int(page_num) - 1]
    chapter_title = f"Chapter {page_num}: {chapter_name}"

    with open(f"book_viewer/data/chp{page_num}.txt") as file:
        chapter = file.read()
    return render_template('chapter.html',
                            chapter_title=chapter_title,
                            contents=g.contents,
                            chapter=chapter)

@app.route("/search")
def search():
    query = request.args.get('query', '')
    matching_chapters = {}
    for chapter_number in range(1,13):
        with open(f"book_viewer/data/chp{chapter_number}.txt") as file:
            chapter = file.read()
        if query in chapter:
            chapter_name = g.contents[int(chapter_number) - 1]
            matching_chapters[chapter_number] = chapter_name

    return render_template('search.html',
                            query=query,
                            contents=g.contents,
                            matching_chapters=matching_chapters)

@app.errorhandler(404)
def page_not_found(error):
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True, port=5003)
