from flask import request, render_template, current_app, jsonify, send_file, flash
from app import app
from app.library.controller import DownloadBook


@app.route("/search-books")
def search_books():
    base_url = current_app.config["BASE_URI"]
    search_url = current_app.config["SEARCH_URI"]
    search_query = request.args.get("query", "").lower()
    
    if not search_query:
        flash('Enter a search query', 'error')
        return render_template('index.html')
    else:
        search_url = str(search_url).format(base_url, search_query.replace(" ", "+"))
        data = DownloadBook.search_books(search_url, search_query)
    # books = DownloadBook.rank_list(data, search_query)
    if not len(data):
        flash('Could not find book. Check name of book again or it may not be available', 'error')
        return render_template('index.html')
    else:
        return render_template('index.html', books=data)


@app.route("/get-book", methods=["POST"])
def download_book():
    url = request.form["url"]
    base_url = current_app.config["BASE_URI"]
    url = base_url + url
    book, name = DownloadBook.get_book(url)
    return send_file(book, as_attachment=True, attachment_filename=name)
