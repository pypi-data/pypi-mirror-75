import os

from dotenv import load_dotenv
from py2neo import Graph

from ae_env_manager import AeEnvManager, AE_ENV_TYPE
#from .ae_get_data import ae_data_manager #am = ae_data_manager.instance()
# from .ae_telegram_message import ae_tele_message

# bolt_url_sb ='bolt://34.239.207.167:35634'
# pw_sb = 'meeting-dot-scissors'
# g_sb = Graph(bolt_url_sb, auth=(user_name, pw_sb))
from ae_logger import ae_log


def get_LEADER(l_graphs):
    for g in l_graphs:
        check_str = str(g.run('call dbms.cluster.role("neo4j")').to_table())
        print(check_str)
        if 'LEADER' in check_str:
            ae_log.debug(f'current LEADER on neo4j is {g}')
            return g
    print('something wrong')

    return 'something wrong'

def send_dataframe(graph, df, statement):
    print(f'sending dataframe of {df.shape}')
    # tx = graph.auto() # v5에 들어간 내용
    tx = graph.begin(autocommit=True)
    params = df.to_dict(orient='records')

    print(
        tx.evaluate(statement, parameters = {"params" : params})
    )
def get_batches(l, batch_size = 100):
    return ((i, l[i:i+batch_size]) for i in range(0, len(l), batch_size))

def send_dataframe_batch(graph, df, statement, batch_size):
    # dataframe is indexed with numerical indexes
    # lis_edge = df.to_dict(orient='records')

    batches = get_batches(df, batch_size)
    for i, df in batches:
        print(f'batch size {df.shape}')
        send_dataframe(graph, df, statement)


if __name__ == '__main__':
    AeEnvManager.instance().set_env_path(AE_ENV_TYPE.AE_ENV_ALL, os.path.join('..', '.env'))
    telegram_env_path = AeEnvManager.instance().get_env_path(AE_ENV_TYPE.AE_ENV_ALL)
    if os.path.exists(telegram_env_path):
        load_dotenv(dotenv_path=telegram_env_path, encoding='utf-8')

    user_name = os.getenv('NEO4J_USER_NAME')
    password = os.getenv('NEO4J_PASSWORD')
    bolt_url_1 = os.getenv('NEO4J_BOLT_URL_1')
    bolt_url_2 = os.getenv('NEO4J_BOLT_URL_2')
    bolt_url_3 = os.getenv('NEO4J_BOLT_URL_3')
    g_1 = Graph(bolt_url_1, auth=(user_name, password))
    g_2 = Graph(bolt_url_2, auth=(user_name, password))
    g_3 = Graph(bolt_url_3, auth=(user_name, password))

    l_graphs = [g_1, g_2, g_3]
    g_l = get_LEADER(l_graphs)
    # date_ref = pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d')
    # date_ref = pd.Timestamp.now(tz='Asia/Seoul').strftime('%Y%m%d')
    print(g_l)