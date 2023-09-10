import os
from datetime import datetime as dt
import jinja2


def main():
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates/')
    )

    names = ['contact.html', 'index.html']

    for name in names:
        content = env.get_template(name)
        content = content.render()

        with open(os.path.join('docs', name), 'w', encoding='utf-8') as write_file:
            write_file.write(content)

    exit(0)


    experience_template = env.get_template('experience.html')


    with open(os.path.join('resources', 'lattes_graph.html'), 'r', encoding='utf-8') as read_file:
        lattes_graph = read_file.read()

    now = dt.now()

    content = experience_template.render(
        navigation_bar=navbar.render(),
        date_generated=now.strftime('%B %d, %Y'),
        lattes_graph=lattes_graph,
    )
    with open(os.path.join('docs', 'experience.html'), 'w', encoding='utf-8') as write_file:
        write_file.write(content)


if __name__ == '__main__':
    main()