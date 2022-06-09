from flask import current_app

def post_progress(content):
    # logging the content
    print(content)
    current_app.logger.info(content)

    return "suerte con eso"