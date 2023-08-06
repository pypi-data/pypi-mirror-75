#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Use fontawesome icons
"""

import re
import uuid

from docutils import nodes
from docutils.parsers.rst import Directive
import docutils.parsers.rst.directives as directives

from sphinx.writers.html import HTMLTranslator
from sphinx.writers.latex import LaTeXTranslator
from sphinx.writers.texinfo import TexinfoTranslator
from sphinx.writers.text import TextTranslator
from sphinx.writers.manpage import ManualPageTranslator
from sphinx.util.osutil import relative_uri

__version_info__ = (0, 1, 3)
__version__ = '.'.join([str(val) for val in __version_info__])


class fa(nodes.General, nodes.Inline, nodes.Element):
    pass


class falink(nodes.General, nodes.Inline, nodes.Element):
    pass


def html_visit_fa(self: HTMLTranslator, node: fa) -> None:
    path = {
        'brands': self.builder.config.fa_brands_path,
        'regular': self.builder.config.fa_regular_path,
        'solid': self.builder.config.fa_solid_path,
    }[node['iconset']]

    path = relative_uri(
        self.builder.current_docname,
        self.builder.get_asset_paths()[0] + '/' + path
    )

    label_uid = uuid.uuid4()
    title = None
    options = 'role="img"'
    options += ' xmlns="http://www.w3.org/2000/svg"'
    options += ' xmlns:xlink="http://www.w3.org/1999/xlink"'
    if node.get('alt', None):
        options += ' aria-labelledby="fa_%s"' % label_uid
        title = '<title id="%s">%s</title>' % (label_uid, node['alt'])
    else:
        options += ' aria-hidden="true" xlink:title=""'

    if node.get('html_id', None):
        options += ' id="%s"' % node['html_id']

    options += ' class="fasvg %s"' % (node.get('html_class', '') or '')

    self.body.append(
        '<svg %s>' % options
    )

    if title:
        self.body.append(title)

    self.body.append(
        '<use xlink:href="%s#%s"></use></svg>' % (path, node['icon'])
    )
    raise nodes.SkipNode


def latex_visit_fa(self: LaTeXTranslator, node: fa) -> None:
    if 'alt' in node.attributes:
        self.body.append('[%s]' % node['alt'])
    raise nodes.SkipNode


def texinfo_visit_fa(self: TexinfoTranslator, node: fa) -> None:
    if 'alt' in node.attributes:
        self.body.append('[%s]' % node['alt'])
    raise nodes.SkipNode


def text_visit_fa(self: TextTranslator, node: fa) -> None:
    if 'alt' in node.attributes:
        self.add_text('[%s]' % node['alt'])
    raise nodes.SkipNode


def man_visit_fa(self: ManualPageTranslator, node: fa) -> None:
    if 'alt' in node.attributes:
        self.body.append('[%s]' % node['alt'])
    raise nodes.SkipNode


def create_fa_node(iconset, icon, html_id=None, html_class=None, alt=None):
    node = fa()
    node['iconset'] = iconset
    node['icon'] = icon
    node['html_id'] = html_id
    node['html_class'] = html_class
    node['alt'] = alt
    return node


def html_visit_falink(self: HTMLTranslator, node: fa) -> None:
    path = {
        'brands': self.builder.config.fa_brands_path,
        'regular': self.builder.config.fa_regular_path,
        'solid': self.builder.config.fa_solid_path,
    }[node['iconset']]

    path = relative_uri(
        self.builder.current_docname,
        self.builder.get_asset_paths()[0] + '/' + path
    )
    self.body.append(
        '<a class="fasvglink %s" href="%s">' %
        (node['icon'], node['url']))
    self.body.append(
        '<svg aria-hidden="true" class="icon" role="img"'
        + ' xlink:title=""'
        + ' xmlns="http://www.w3.org/2000/svg"'
        + ' xmlns:xlink="http://www.w3.org/1999/xlink">'
    )

    self.body.append(
        '<use xlink:href="%s#%s"></use>' % (path, node['icon'])
    )
    self.body.append('</svg> %s</a>' % node['text'])
    raise nodes.SkipNode


def latex_visit_falink(self: LaTeXTranslator, node: fa) -> None:
    self.body.append('\\href{%s}{%s}' % (node['url'], node['text']))
    raise nodes.SkipNode


def texinfo_visit_falink(self: TexinfoTranslator, node: fa) -> None:
    self.body.append('\\href{%s}{%s}' % (node['url'], node['text']))
    raise nodes.SkipNode


def text_visit_falink(self: TextTranslator, node: fa) -> None:
    self.add_text('%s <%s>' % (node['text'], node['url']))
    raise nodes.SkipNode


def man_visit_falink(self: ManualPageTranslator, node: fa) -> None:
    self.body.append('%s <%s>' % (node['text'], node['url']))
    raise nodes.SkipNode


def create_falink_node(iconset, text):
    node = falink()
    regex = re.compile(r'(?P<icon>[a-zA-Z-_]*):(?P<text>.*)<(?P<url>.*)>')
    parsed = regex.search(text)
    node['iconset'] = iconset
    node['icon'] = parsed.group('icon')
    node['url'] = parsed.group('url').strip()
    node['text'] = parsed.group('text').strip()
    return node


def fab(role, rawtext, text, lineno, inliner, options={}, content=[]):
    return [create_fa_node('brands', text)], []


def far(role, rawtext, text, lineno, inliner, options={}, content=[]):
    return [create_fa_node('regular', text)], []


def fas(role, rawtext, text, lineno, inliner, options={}, content=[]):
    return [create_fa_node('solid', text)], []


def fablink(role, rawtext, text, lineno, inliner, options={}, content=[]):
    return [create_falink_node('brands', text)], []


def farlink(role, rawtext, text, lineno, inliner, options={}, content=[]):
    return [create_falink_node('regular', text)], []


def faslink(role, rawtext, text, lineno, inliner, options={}, content=[]):
    return [create_falink_node('solid', text)], []


class FaDirective(Directive):

    has_content = False
    required_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        "class": directives.unchanged,
        "id": directives.unchanged,
        "alt": directives.unchanged,
    }
    iconset = None

    def run(self):
        node = create_fa_node(
            self.iconset,
            self.arguments[0],
            self.options['id'],
            self.options['class'],
            self.options['alt']
        )
        return [node]


class Fab(FaDirective):
    iconset = 'brands'


class Far(FaDirective):
    iconset = 'regular'


class Fas(FaDirective):
    iconset = 'solid'


def setup(app):
    app.add_node(
        fa,
        html=(html_visit_fa, None),
        epub=(html_visit_fa, None),
        latex=(latex_visit_fa, None),
        texinfo=(texinfo_visit_fa, None),
        text=(text_visit_fa, None),
        man=(man_visit_fa, None),
    )
    app.add_node(
        falink,
        html=(html_visit_falink, None),
        epub=(html_visit_falink, None),
        latex=(latex_visit_falink, None),
        texinfo=(texinfo_visit_falink, None),
        text=(text_visit_falink, None),
        man=(man_visit_falink, None),
    )
    app.add_config_value('fa_brands_path', 'fa/brands.svg', True)
    app.add_config_value('fa_regular_path', 'fa/regular.svg', True)
    app.add_config_value('fa_solid_path', 'fa/solid.svg', True)
    app.add_role('fab', fab)
    app.add_role('fas', fas)
    app.add_role('far', far)
    app.add_role('fablink', fablink)
    app.add_role('faslink', faslink)
    app.add_role('farlink', farlink)
    app.add_directive('fab', Fab)
    app.add_directive('fas', Fas)
    app.add_directive('far', Far)
    return {'version': __version__}
