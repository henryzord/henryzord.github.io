import os

from jinja2 import Environment, FileSystemLoader
import click
import yaml


def main():
    env = Environment(loader=FileSystemLoader('templates/'))
    template = env.get_template('template_experience.html')

    with open(os.path.join('resources', 'lattes_graph.html'), 'r', encoding='utf-8') as read_file:
        code = read_file.read()

    content = template.render(lattes_graph=code)
    with open('experience.html', 'w', encoding='utf-8') as write_file:
        write_file.write(content)


if __name__ == '__main__':
    main()
