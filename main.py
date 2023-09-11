import os
import json
import jinja2
from datetime import datetime as dt

from render.lattes_graph import generate_graph


def render_experience_template(template):
    fig, html = generate_graph()

    with open(os.path.join('templates', 'lattes_graph.html'), 'w', encoding='utf-8') as write_file:
        write_file.write(html)

    now = dt.now()
    content = template.render(date_generated=now.strftime('%B %d, %Y'))
    return content


def render_highlights_template(template):
    with open(os.path.join('resources', 'highlights.json'), 'r', encoding='utf-8') as read_file:
        highlights = json.load(read_file)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates/')
    )
    card = env.get_template('highlights_card.html')
    cards = []
    for highlight in highlights:
        rendered = card.render(
            **highlight,
        )
        cards += [rendered]

    content = template.render(highlights_cards=''.join(cards))
    return content


def default_render(template):
    return template.render()


def main():
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates/')
    )

    names = {
        'index.html': default_render,
        'experience.html': render_experience_template,
        'highlights.html': render_highlights_template,
        'contact.html': default_render
    }

    for name, func in names.items():
        template = env.get_template(name)
        content = func(template)

        with open(os.path.join('docs', name), 'w', encoding='utf-8') as write_file:
            write_file.write(content)


if __name__ == '__main__':
    main()
