from html.parser import HTMLParser
from pathlib import Path


class ShopChecker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.headings = 0

    def handle_starttag(self, tag, attributes):
        assert tag != "script", "JavaScript is not allowed"
        self.headings += tag == "h1"
        for name, value in attributes:
            assert not name.startswith("on"), "JavaScript events are not allowed"
            if value:
                assert not value.strip().lower().startswith("javascript:"), "JavaScript URLs are not allowed"
            if name == "id":
                self.ids.append(value)
            if name == "href" and value and value.startswith("#"):
                self.links.append(value[1:])


folder = Path(__file__).parent
checker = ShopChecker()
checker.feed((folder / "index.html").read_text(encoding="utf-8"))
assert checker.headings == 1, "The page must contain one h1"
assert len(checker.ids) == len(set(checker.ids)), "Duplicate IDs found"
assert all(link in checker.ids for link in checker.links), "An internal link has no destination"
assert not list(folder.rglob("*.js")), "JavaScript files are not allowed"
assert (folder / "style.css").is_file(), "The stylesheet is missing"
print("Task rules and internal links passed")
