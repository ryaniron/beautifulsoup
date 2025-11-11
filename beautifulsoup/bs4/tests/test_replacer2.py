from bs4 import BeautifulSoup
from bs4.soup_replacer import SoupReplacer

def test_simple_replace():
    html = "<b>Hi</b><b>There</b>"
    soup = BeautifulSoup(html, "html.parser", replacer=SoupReplacer("b", "blockquote"))
    assert soup.find("b") is None
    assert len(soup.find_all("blockquote")) == 2

def test_name_xformer():
    html = "<b>Bold</b><i>Italic</i>"
    replacer = SoupReplacer(name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name)
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)
    assert soup.find("blockquote").text == "Bold"

def test_attrs_xformer():
    html = '<p class="intro">Hello</p>'
    replacer = SoupReplacer(attrs_xformer=lambda tag: {**tag.attrs, "data-id": "1"})
    soup = BeautifulSoup(html, "html.parser", replacer=replacer)
    p = soup.find("p")
    assert p["data-id"] == "1"

def test_xformer_remove_class():
    html = '<div class="x">content</div>'
    def remove_class(tag):
        tag.attrs.pop("class", None)
    soup = BeautifulSoup(html, "html.parser", replacer=SoupReplacer(xformer=remove_class))
    div = soup.find("div")
    assert "class" not in div.attrs

def test_combined_transformers():
    html = '<b class="y">text</b>'
    def name_fx(tag): return "strong"
    def attr_fx(tag): return {"data-new": "ok"}
    soup = BeautifulSoup(html, "html.parser",
                         replacer=SoupReplacer(name_xformer=name_fx, attrs_xformer=attr_fx))
    strong = soup.find("strong")
    assert strong["data-new"] == "ok"

def test_side_effect_logger():
    html = "<h1>Title</h1>"
    seen = []
    def log(tag): seen.append(tag.name)
    BeautifulSoup(html, "html.parser", replacer=SoupReplacer(xformer=log))
    assert "h1" in seen
