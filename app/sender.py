import psycopg2
from bottle import request, run, route

DNS = 'dbname=email_sender user=postgres host=db'
SQL = 'INSERT INTO emails (assunto, mensagem) VALUES (%s, %s)'


def register_message(assunto, mensagem):
    conn = psycopg2.connect(DNS)
    cur = conn.cursor()
    cur.execute(SQL, (assunto, mensagem))
    conn.commit()
    cur.close()
    conn.close()

    print('Mensagem Registrada !')


@route('/', method='POST')
def send():
    assunto = request.forms.get('assunto')
    mensagem = request.forms.get('mensagem')

    register_message(assunto, mensagem)

    return 'Mensagem enfileirada ! Assunto: {} Mensagem: {}'.format(
        assunto, mensagem
    )


# class Sender(Bottle):
#     def __init__(self):
#         super().__init__()
#         self.route('/', method='POST', callback=self.send)

#         redis_host = os.getenv('REDIS_HOST', 'queue')
#         self.fila = redis.StrictRedis(host=redis_host, port=6379, db=0)

#         db_host = os.getenv('DB_HOST', 'db')
#         db_user = os.getenv('DB_USER', 'postgres')
#         db_name = os.getenv('DB_NAME', 'sender')
#         dsn = f'dbname={db_name} user={db_user} host={db_host}'
#         self.conn = psycopg2.connect(dsn)

#     def register_message(self, assunto, mensagem):
#         SQL = 'INSERT INTO emails (assunto, mensagem) VALUES (%s, %s)'
#         cur = self.conn.cursor()
#         cur.execute(SQL, (assunto, mensagem))
#         self.conn.commit()
#         cur.close()

#         msg = {'assunto': assunto, 'mensagem': mensagem}
#         self.fila.rpush('sender', json.dumps(msg))

#         print('Mensagem registrada !')

#     def send(self):
#         assunto = request.forms.get('assunto')
#         mensagem = request.forms.get('mensagem')

#         self.register_message(assunto, mensagem)
#         return 'Mensagem enfileirada ! Assunto: {} Mensagem: {}'.format(
#             assunto, mensagem
#         )

if __name__ == '__main__':
    # sender = Sender()
    run(host='0.0.0.0', port=8080, debug=True)
