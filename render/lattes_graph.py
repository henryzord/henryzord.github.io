import bs4
import os

import pandas as pd
from plotly import graph_objs as go
import plotly.express as px
from datetime import datetime as dt


def get_formation_data(particle, nivel):
    ano_inicio = particle.attrs['ANO-DE-INICIO']
    ano_conclusao = particle.attrs['ANO-DE-CONCLUSAO'] if len(particle.attrs['ANO-DE-CONCLUSAO']) > 0 else dt.now().year

    data_inicio = f'{ano_inicio}-01-01'
    data_fim = f'{ano_conclusao}-01-01'

    if 'NOME-CURSO' in particle.attrs:
        curso = particle.attrs['NOME-CURSO']
        str_curso = f'{nivel} em {curso}'
    else:
        str_curso = nivel

    res = [particle.attrs['NOME-INSTITUICAO'], data_inicio, data_fim, str_curso, 'Formação']

    return res


def tabulate_text(text, max_width=40):
    particles = text.split(' ')
    processed = []
    counter = 0
    for p in particles:
        counter += len(p)
        if counter >= max_width:
            processed += [p + '<br>']
            counter = 0
        else:
            processed += [p]

    return ' '.join(processed)


def remove_special_characters(text):
    return text.strip().replace('&quot;', '\"').replace('&#10;', ' ').strip()


def build_other_info_string(enq_func, other_info, max_width=40):
    newline = '<br>' if len(other_info) > max_width else ''

    specs = newline + (enq_func if len(enq_func) > 0 else '')
    specs += f': {other_info}' if len(other_info) > 0 else ''

    return specs


def main():
    encoding = 'ISO-8859-1'
    with open(os.path.join('resources', 'curriculo.xml'), 'r', encoding=encoding) as read_file:
        specs = read_file.read()

    bs_data = bs4.BeautifulSoup(specs.encode(encoding), 'xml', from_encoding=encoding)

    formacoes = bs_data.find('FORMACAO-ACADEMICA-TITULACAO')

    l_df = []

    l_df += [get_formation_data(formacoes.find('GRADUACAO'), 'Graduação')]
    l_df += [get_formation_data(formacoes.find('MESTRADO'), 'Mestrado')]
    l_df += [get_formation_data(formacoes.find('DOUTORADO'), 'Doutorado')]

    atuacoes = bs_data.find('ATUACOES-PROFISSIONAIS')
    p_atuacoes = atuacoes.findAll('ATUACAO-PROFISSIONAL')

    for atuacao in p_atuacoes:
        nome_inst = atuacao.attrs['NOME-INSTITUICAO']
        vinculos = atuacao.findAll('VINCULOS')
        for vinc in vinculos:
            mes_inicio = vinc.attrs['MES-INICIO'] if len(vinc.attrs['MES-INICIO']) > 0 else '01'
            ano_inicio = vinc.attrs['ANO-INICIO']
            mes_fim = vinc.attrs['MES-FIM'] if len(vinc.attrs['MES-FIM']) > 0 else '01'
            ano_fim = vinc.attrs['ANO-FIM'] if len(vinc.attrs['ANO-FIM']) > 0 else str(dt.now().year + 1)

            if mes_fim == mes_inicio:
                mes_fim = int(mes_fim) + 1

            enq_func = vinc.attrs['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO'].strip()
            other_info = tabulate_text(remove_special_characters(vinc.attrs['OUTRAS-INFORMACOES']))

            specs = build_other_info_string(enq_func, other_info)

            l_df += [[
                nome_inst, f'{ano_inicio}-{mes_inicio}-01', f'{ano_fim}-{mes_fim}-01', specs, 'Atuação Profissional'
            ]]

    df = pd.DataFrame(l_df, columns=['instituição', 'início', 'fim', 'Outras Informações', 'Tipo'])
    df.sort_values(by=['fim'], ascending=False, inplace=True)

    fig1 = px.timeline(
        df,
        x_start='início', x_end='fim', y='instituição', hover_data=['Outras Informações'],
        color='Tipo',
        color_discrete_map={'Atuação Profissional': '#000000', 'Formação': '#FFFFFF'}
    )

    fig = go.Figure(
        layout=go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    )

    fig.add_trace(go.Bar(fig1.data[0]))
    fig.add_trace(go.Bar(fig1.data[1]))
    fig.update_xaxes(type='date', showgrid=False)
    fig.update_yaxes(autorange='reversed', showgrid=False)  # otherwise tasks are listed from the bottom up

    html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    with open(os.path.join('resources', '../templates/lattes_graph.html'), 'w', encoding='utf-8') as write_file:
        write_file.write(html)

    fig.show()


if __name__ == '__main__':
    main()
