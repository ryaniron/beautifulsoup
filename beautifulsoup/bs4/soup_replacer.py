class SoupReplacer:
    """
    A tag transformation helper used by BeautifulSoup during parsing.

    Two usage styles:

      (1) Simple tag rename:
          replacer = SoupReplacer("b", "blockquote")

      (2) Transformer API:
          replacer = SoupReplacer(
              name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name,
              attrs_xformer=lambda tag: {**tag.attrs, "data-seen": "1"},
              xformer=lambda tag: tag.attrs.pop("class", None)
          )

    All replacements occur *during parsing*, so the parse tree
    directly contains transformed tags.
    """

    def __init__(self, og_tag=None, alt_tag=None,
                 name_xformer=None, attrs_xformer=None, xformer=None):
        # --- Simple replacement pair (Milestone 2) ---
        self.og_tag = og_tag
        self.alt_tag = alt_tag

        # --- Transformer-based API (Milestone 3) ---
        self.name_xformer = name_xformer
        self.attrs_xformer = attrs_xformer
        self.xformer = xformer

    # --- Utility methods used by the HTML parser ---
    def transform_tag(self, tag):
        """
        Apply transformations in-place to a tag object during parsing.
        Called from bs4.builder._htmlparser._handle_starttag().
        """
        # 1️ Simple legacy rename
        if self.og_tag and self.alt_tag and tag.name == self.og_tag:
            tag.name = self.alt_tag

        # 2️ Functional name transformer
        elif callable(self.name_xformer):
            new_name = self.name_xformer(tag)
            if new_name:
                tag.name = new_name

        # 3️ Functional attributes transformer
        if callable(self.attrs_xformer):
            new_attrs = self.attrs_xformer(tag)
            if isinstance(new_attrs, dict):
                tag.attrs = new_attrs

        # 4️ Generic transformer with side-effects
        if callable(self.xformer):
            self.xformer(tag)

        return tag
