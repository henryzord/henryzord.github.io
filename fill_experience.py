import os

import jinja2


def main():
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates/'))
    experience_template = env.get_template('template_experience.html')
    navbar = env.get_template('navigation_bar.html')  # type: jinja2.Template

    with open(os.path.join('resources', 'lattes_graph.html'), 'r', encoding='utf-8') as read_file:
        lattes_graph = read_file.read()

    content = experience_template.render(lattes_graph=lattes_graph, navigation_bar=navbar.render())
    with open('experience.html', 'w', encoding='utf-8') as write_file:
        write_file.write(content)


if __name__ == '__main__':
    main()
