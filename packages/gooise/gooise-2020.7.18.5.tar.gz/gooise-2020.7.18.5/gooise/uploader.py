def image(path):
    from requests import post

    response = post("http://www.google.com/searchbyimage/upload", allow_redirects=False,
                    files={"encoded_image": (path, open(path, "rb")), "image_content": ""})
    response.raise_for_status()
    return response.headers.get("Location")
