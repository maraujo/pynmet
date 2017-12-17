import base64
import os
import requests
import pandas as pd
import datetime as dt
from bs4 import BeautifulSoup
from io import StringIO
from pathlib import Path


pg_form = 'http://www.inmet.gov.br/sonabra/pg_dspDadosCodigo_sim.php?'
pg_data = 'http://www.inmet.gov.br/sonabra/pg_downDadosCodigo_sim.php'

header = ['Temperatura', 'Temperatura_max', 'Temperatura_min', 'Umidade',
          'Umidade_max', 'Umidade_min', 'Ponto_orvalho',
          'Ponto_orvalho_max', 'Ponto_orvalho_min', 'Pressao',
          'Pressao_max', 'Pressao_min', 'Vento_velocidade', 'Vento_direcao',
          'Vento_rajada', 'Radiacao', 'Precipitacao']

rep_vals = ['\r', '\n', '\t', '////', '///', '//']

pynmet_path = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(pynmet_path, 'data', 'estacoes.csv')
sites = pd.read_csv(filepath, index_col='codigo',
                    dtype={'codigo': str, 'alt': int})


def _parse(a, b):
        return dt.datetime.strptime(''.join(map(str, [a, b])), '%d/%m/%Y%H')


def get_from_web(code, dia_i, dia_f):

    decoded = base64.b64encode(code.encode('ascii')).decode()
    est = pg_form + decoded
    session = requests.session()
    page = session.get(est)
    soup = BeautifulSoup(page.content, 'lxml')
    base64Str = str(soup.findAll('img')[0])[-11:-3]
    encoded = base64.b64decode(base64Str.encode('ascii')).decode()
    post_request = {'aleaValue': base64Str, 'dtaini': dia_i,
                    'dtafim': dia_f, 'aleaNum': encoded}
    session.post(est, post_request)
    data_str = session.get(pg_data).content.decode()
    data_str = [data_str.replace(x, '') for x in rep_vals]
    data_str = data_str.replace('<br>', '\n').replace('/,', ',')
    dados = pd.read_csv(StringIO(data_str), date_parser=_parse, index_col=0,
                        usecols=list(range(1, 20), parse_dates=[[1, 2]]))
    dados.columns = header
    dados = dados.tz_localize('UTC')
    return dados


def get_from_ldb(code, db, local=False):

    fmt = "%d/%m/%Y"
    dia_f = dt.date.today().strftime(fmt)
    db = Path(db)

    if local is True:
        try:
            dados = pd.read_hdf(db, code)
        except RuntimeWarning:
            print('Não há dados locais para a estação {}').format(code)
            dados = pd.DataFrame(columns=header)
        return dados

    if db.is_file():
        try:
            dados = pd.read_hdf(db, code)
            dia_i = dados.index.max().strftime(fmt)
        except:
            dia_i = (dt.date.today() - dt.timedelta(days=365)).strftime(fmt)
    else:
        dia_i = (dt.date.today() - dt.timedelta(days=365)).strftime(fmt)

    if 'dados' in locals():
        last_data = get_from_web(code, dia_i, dia_f)
        dados = dados.append(last_data)
        dados.to_hdf(db, str(code), format='table', dropna=True)
    else:
        dados = get_from_web(code, dia_i, dia_f)
        dados.to_hdf(db, str(code), format='table', dropna=True)
    return dados


def update_all(db=os.getenv("HOME") + '/.inmetdb.hdf'):

    for code in sites.index:
        try:
            get_from_ldb(code, db)
            print('{}: UPDATED'.format(code))
        except:
            print('{}: ERRO'.format(code))
