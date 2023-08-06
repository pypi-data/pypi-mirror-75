from html.parser import HTMLParser
import unicodedata
from urllib.parse import parse_qs, urlencode, urlparse

from jinja2.utils import escape as html_escape, urlize
from slugify import slugify as _slugify
from inflection import humanize, titleize

__all__ = [
    'embed_video_url',
    'humanize_status',
    'plural',
    'remove_accents',
    'remove_markup',
    'slugify',
    'text_to_html',
    'yes_no'
]


def embed_video_url(url):
    """Return the embed video URL for any given youtube or vimeo URL"""

    # Define a table of supported video serving domains
    domains = {
        'www.youtube.com': 'youtube',
        'youtu.be': 'youtube',
        'vimeo.com': 'vimeo',
        'player.vimeo.com': 'vimeo'
    }

    # Parse the domain
    parts = urlparse(url)
    params = parse_qs(parts.query)

    # Check the URL domain is supported
    if parts.netloc not in domains:
        return None

    # Convert the URL
    service = domains[parts.netloc]
    video_id = None
    video_url = None

    if service == 'youtube':

        # Useful default params
        params['enablejsapi'] = 1
        params['rel'] = 0

        if parts.path == '/watch':
            if params.get('v'):
                video_id = params.pop('v')[0]
        else:
            video_id = parts.path[1:]

        if video_id:
            video_url = 'https://www.youtube.com/embed/' + video_id
            if params:
                video_url += '?' + urlencode(params)

    elif service == 'vimeo':
        if parts.path.split('/'):
            video_id = parts.path.split('/')[-1]

        if video_id:
            video_url = 'https://player.vimeo.com/video/' + video_id
            if params:
                video_url += '?' + urlencode(params)

    return video_url

def humanize_status(status, *overrides):
    """
    Return a human readable version of a status with the ability to specify how
    particular words should be output.

    For example:
    humanize_status('out_of_stock') // 'Out of stock'
    humanize_status('invalid_password', 'INVALID') // 'INVALID password'
    humanize_status(
        'logged_in_as_admin_user',
        'ADMIN',
        'USER'
        )  // 'Logged in as ADMIN USER'
    """

    # First humanize the status
    status = humanize(status).lower()

    # For any words which are in the override map find the lowercase equivalent,
    # then replace them with the format of the word the user has specified.
    for s in overrides:
        status = status.replace(s.lower(), s)

    # If the first character is lowercase then make it uppercase
    if status[0].islower():
        status = status[0].upper() + status[1:]

    return status

def plural(word, count, word_plural=None):
    """Return a plural version of the word if count not equal to 1"""

    if count == 1:
        return word

    if word_plural:
        return word_plural

    return word + 's'

def remove_accents(s):
    """
    Replace any accented characters with there closest non-accented equivalent.

    This code was taken from the stackoverflow answer here:
    http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string/517974#517974
    """
    nfkd_form = unicodedata.normalize('NFKD', s)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def remove_markup(s):
    """Remove HTML from a string"""
    stripper = _MLStripper()
    stripper.feed(s)
    return stripper.get_data()

def slugify(s):
    """
    Return the given string formatted as a slug
    (https://en.wikipedia.org/wiki/Semantic_URL#slug).
    """
    return _slugify(s)

def text_to_html(text, inline=False, convert_urls=True):
    """
    Return a HTML version of the specified text.

    If `inline` is True then new-lines will be converted line-breaks (`<br>`s),
    if `inline` is False then single new-lines will be converted to line-breaks
    (`<br>`s) and double new-lines will be converted to paragraphs.

    If `convert_urls` is True then URLs within the text are converted to links,
    if `convert_urls` is False then URLs are not converted.
    """

    # Strip \r from new lines
    text = text.replace('\r\n', '\n')

    if inline:
        # Convert URLs to links
        if convert_urls:
            inline_html = urlize(text)
        else:
            inline_html = str(html_escape(text))

        # Convert newlines to line-breaks / `<br>` tags
        inline_html = inline_html.replace('\n', '<br>')

        return inline_html

    else:
        # Convert the text to a list of paragraphs / <p> tags
        paragraphs = [text_to_html(p.strip(), True, convert_urls) \
            for p in text.split('\n\n') if p.strip()]

        # Join the paragraphs into a body and return it
        return '<p>' + '</p><p>'.join(paragraphs) + '</p>'

def upper_first(s):
    """
    Uppercase the first letter in a string.

    This is useful when converting a string that may already contain uppercase
    characters (for example an acronym) where calling capitalize would
    lowercase existing uppercase characters.
    """

    return s[0].upper() + s[1:]

def yes_no(value):
    """Return `'Yes'` if a value coerces to `True`, `'No'` if not."""
    return 'Yes' if value else 'No'


# -- Utils --

class _MLStripper(HTMLParser):
    """
    A HTML parser for stripping markup from a string.

    This code was taken from the stackoverflow answer here:
    https://stackoverflow.com/a/925630/4657956
    """

    def __init__(self):
        super().__init__()

        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)
