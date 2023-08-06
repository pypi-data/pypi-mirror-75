from manhattan.formatters.text import remove_markup

__all__ = ['flows_to_text']


def flows_to_text(flows):
    """Convert HTML within a list of flows to text"""

    # Build a list of text snippets from the HTML contents
    texts = []
    for snippets in flows.values():
        for snippet in snippets:
            for content in snippet['local_contents'].values():
                if type(content) is list:
                    continue

                text = remove_markup(content).strip()
                if text:
                    texts.append(text)

    return ' '.join(texts)

