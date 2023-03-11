import json

from models import Author, Quote

with open("authors.json", "r") as file:
    data = json.load(file)

for author in data:
    Author(fullname=author["fullname"],
           born_date=author["born_date"],
           born_location=author["born_location"],
           description=author["description"]).save()


authors = Author.objects()


with open("quotes.json", "r", encoding="utf-8") as file:
    data = json.load(file)

for quot in data:
    for author in authors:
        if author.fullname == quot["author"]:
            author_reference_obj = author
    
    Quote(tags=quot["tags"],
          author=author_reference_obj,
          quote=quot["quote"]).save()
