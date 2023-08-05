def image_url(url):
    from requests import get

    response = get("https://images.google.com/searchbyimage", allow_redirects=False, params={
        "image_url": url, "encoded_image": "", "image_content": ""
    })

    response.raise_for_status()
    return response.headers.get("Location")
