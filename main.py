import os
import jinja2
from datetime import datetime as dt


def render_experience_template(content):
    with open(os.path.join('resources', 'lattes_graph.html'), 'r', encoding='utf-8') as read_file:
        lattes_graph = read_file.read()

    now = dt.now()
    content = content.render(
        date_generated=now.strftime('%B %d, %Y'),
        lattes_graph=lattes_graph,
    )
    return content


def main():
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates/')
    )

    names = ['index.html', 'experience.html', 'highlights.html', 'contact.html']

    for name in names:
        template = env.get_template(name)

        if name == 'experience.html':
            content = render_experience_template(template)
        else:
            content = template.render()

        with open(os.path.join('docs', name), 'w', encoding='utf-8') as write_file:
            write_file.write(content)


if __name__ == '__main__':
    main()
