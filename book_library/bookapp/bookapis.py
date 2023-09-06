# Get the ISBN for the book

import os
key = os.environ.get('Google_Cloud_API_Key')

key = 'AIzaSyDxM0hcZbiTkjMmR6-japeENTi5418T6Wk'

import requests

def get_isbn_from_title(title, api_key):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"intitle:{title}",
        "key": api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if "items" in data:
            book = data["items"][0]
            volume_info = book.get("volumeInfo", {})
            isbn = volume_info.get("industryIdentifiers", [])
            for identifier in isbn:
                if identifier["type"] == "ISBN_13":
                    return identifier["identifier"]

        return "ISBN not found"
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
def get_book_info_from_isbn(isbn, api_key):
    base_url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"isbn:{isbn}",
        "key": api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if "items" in data:
            book = data["items"][0]
            volume_info = book.get("volumeInfo", {})
            title = volume_info.get("title", "Title not found")
            subtitle = volume_info.get("subtitle", "Subtitle not found")
            image_links = volume_info.get("imageLinks", {})
            image_url = image_links.get("thumbnail", "Image not found")

            return title, subtitle, image_url

        return "Book not found"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    api_key = key  
    book_title = input("Enter the book title: ")
    isbn = get_isbn_from_title(book_title, api_key)
    print(f"ISBN for '{book_title}': {isbn}")

def get_data_from_isbn(isbn, api_key):
    
    return(isbn.data())