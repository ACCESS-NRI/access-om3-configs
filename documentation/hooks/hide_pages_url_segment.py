# Change the URL segment for pages in MkDocs to hide the "/pages" prefix, so that pages inside the
# "pages" directory are served directly at the root URL.
from mkdocs.plugins import event_priority
@event_priority(-100)
def on_page_markdown(markdown, *, page, config, files):
    if page.file.url.startswith("pages/"):
        page.file.url = page.file.url.removeprefix("pages/")
        page.file.dest_uri = page.file.dest_uri.removeprefix("pages/")
        page.file.abs_dest_path = page.file.abs_dest_path.removeprefix("pages/")