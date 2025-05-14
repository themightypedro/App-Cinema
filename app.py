from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
import qrcode
import os

# Catálogo de filmes com mais horários, gêneros e detalhes
filmes = [
    {
        "id": 1,
        "titulo": "Missão: Impossível - O Acerto Final",
        "horarios": ["15:20", "16:00", "16:30", "17:00", "18:10", "20:30", "21:30"],
        "poster": "missao.jpg",
        "audio": "DUB",
        "tipo": "LASER",
        "genero": "2025 ‧ Ação/Thriller ‧ 2h 51m",
        "sinopse": "Sinopse: Ethan e sua equipe estão em uma missão para encontrar e destruir uma IA conhecida como The Entity. A viagem ao redor do mundo dá origem a cenas de ação incríveis e mais de uma reviravolta inesperada."
    },
    {
        "id": 2,
        "titulo": "Thunderbolts*",
        "horarios": ["15:20", "16:00", "16:30", "17:00", "18:10", "20:30", "21:30"],
        "poster": "thunderbolts.jpg",
        "audio": "DUB/LEG",
        "tipo": "2D • 3D • IMAX",
        "genero": "2025 ‧ Ação/Ficção científica ‧ 2h 6m",
        "sinopse": "Sinopse: Presos em uma armadilha mortal, uma equipe nada convencional de anti-heróis embarca em uma missão perigosa que os força a confrontar os cantos mais sombrios de suas vidas."
    },
    {
        "id": 3,
        "titulo": "Divertida Mente 2",
        "horarios": ["15:20", "16:00", "17:00", "18:10", "20:30"],
        "poster": "divertidamente2.jpg",
        "audio": "DUB/LEG",
        "tipo": "2D",
        "genero": "2024 ‧ Infantil/Comédia ‧ 1h 36m",
        "sinopse": "Sinopse: Com um salto temporal, Riley se encontra mais velha, passando pela tão temida adolescência. Junto com o amadurecimento, a sala de controle também está passando por uma adaptação para dar lugar a algo totalmente inesperado: novas emoções. As já conhecidas, Alegria, Raiva, Medo, Nojinho e Tristeza não têm certeza de como se sentir quando novos inquilinos chegam ao local."
    },
    {
        "id": 4,
        "titulo": "O Lugar Silencioso: Dia Um",
        "horarios": ["16:00", "16:30", "17:00", "20:30", "21:00"],
        "poster": "silencioso.jpg",
        "audio": "DUB/LEG",
        "tipo": "LASER • 3D",
        "genero": "2024 ‧ Terror/Ficção científica ‧ 1h 39m",
        "sinopse": "Sinopse: Uma mulher luta pela sobrevivência durante uma invasão alienígena na cidade de Nova York."
    },
    {
        "id": 5,
        "titulo": "Bad Boys: Até o Fim",
        "horarios": ["15:20", "16:00", "17:00", "18:10", "21:00"],
        "poster": "badboys.jpg",
        "audio": "DUB/LEG",
        "tipo": "LASER",
        "genero": "2024 ‧ Ação/Comédia ‧ 1h 55m",
        "sinopse": "Sinopse: Os brincalhões polícias de Miami, Mike Lowrey e Marcus Burnett, embarcam em uma perigosa missão para limpar o nome do falecido capitão da polícia."
    },
    {
        "id": 6,
        "titulo": "Garfield: Fora de Casa",
        "horarios": ["15:20", "16:30", "17:00", "18:10", "20:30"],
        "poster": "garfield.jpg",
        "audio": "DUB",
        "tipo": "2D",
        "genero": "2024 ‧ Infantil/Comédia ‧ 1h 41m",
        "sinopse": "Sinopse: Garfield, o gato caseiro que odeia segundas-feiras e ama lasanha, se vê em uma aventura selvagem ao ar livre quando seu pai há muito perdido o envolve em um assalto de alto risco."
    },
    {
        "id": 7,
        "titulo": "Vingadores: Ultimato",
        "horarios": ["15:20", "16:30", "17:00", "18:10", "20:30"],
        "poster": "ultimato.jpg",
        "audio": "Dublado",
        "tipo": "2D • 3D • IMAX",
        "genero": "2019 ‧ Ação/Ficção científica ‧ 3h 1m",
        "sinopse": "Sinopse: Após Thanos eliminar metade das criaturas vivas, os Vingadores têm de lidar com a perda de amigos e entes queridos. Com Tony Stark vagando perdido no espaço sem água e comida, Steve Rogers e Natasha Romanov lideram a resistência contra o titã louco."
    },
{
        "id": 8,
        "titulo": "John Wick 4",
        "poster": "johnwick4.jpg",
        "audio": "DUB/LEG",
        "tipo": "2D",
        "genero": "2023 ‧ Ação/Thriller ‧ 2h 49m",
        "horarios": ["17:00", "16:30", "16:00", "18:00"],
        "salas": {"17:00": 7, "16:30": 7, "16:00": 1, "18:00": 8},
        "sinopse": "Sinopse: O ex-assassino de aluguel John Wick é procurado pelo mundo todo e a recompensa por sua captura aumenta cada vez mais. Wick descobre um caminho para derrotar a Alta Cúpula, mas antes de conquistar sua liberdade, ele precisa enfrentar um novo inimigo com alianças poderosas e forças que transformam velhos amigos em inimigos."
    },
{
        "id": 9,
        "titulo": "Vingadores: Guerra Infinita",
        "poster": "guerrainfinita.jpg",
        "audio": "DUB/LEG",
        "tipo": "2D • 3D • IMAX",
        "genero": "2023 ‧ Ação/Thriller ‧ 2h 49m",
        "horarios": ["17:00", "16:30", "16:00", "18:00"],
        "salas": {"17:00": 7, "16:30": 7, "16:00": 1, "18:00": 8},
        "sinopse": "Sinopse: Homem de Ferro, Capitão América, Thor, Hulk e os Vingadores se unem para combater o maligno Thanos. Em uma missão para coletar todas as seis pedras infinitas, Thanos planeja usá-las para infligir sua vontade maléfica sobre a humanidade."
    },
{
        "id": 10,
        "titulo": "Star Wars: Episódio IV - Uma Nova Esperança",
        "horarios": ["15:20", "16:00", "17:00", "18:10", "20:30"],
        "poster": "starwars77.jpg",
        "audio": "DUB/LEG",
        "tipo": "2D • IMAX",
        "genero": "1977 ‧ Ficção científica/Ação ‧ 2h 1m",
        "sinopse": "Sinopse: A princesa Leia é mantida refém pelas forças imperiais comandadas por Darth Vader. Luke Skywalker e o capitão Han Solo precisam libertá-la e restaurar a liberdade e a justiça na galáxia."
    },
{
        "id": 11,
        "titulo": "Forrest Gump - O Contador de Histórias",
        "horarios": ["15:20", "16:00", "17:00", "18:10", "20:30"],
        "poster": "forrestgump.jpg",
        "audio": "DUB/LEG",
        "tipo": "2D • IMAX",
        "genero": "1994 ‧ Comédia/Romance ‧ 2h 22m",
        "sinopse": "Sinopse: Mesmo sendo ingênuo, Forrest Gump nunca se sentiu desfavorecido. Graças ao apoio da mãe, ele teve uma vida normal. Seja no campo de futebol como um astro do esporte, lutando no Vietnã ou como capitão de um barco de pesca de camarão, Forrest inspira a todos com seu otimismo. Mas a pessoa que Forrest mais ama pode ser a mais difícil de salvar: seu amor de infância, a doce Jenny."
    },
{
        "id": 12,
        "titulo": "O Lobo de Wall Street",
        "horarios": ["15:20", "16:00", "17:00", "18:10", "20:30"],
        "poster": "lobo.jpg",
        "audio": "DUB/LEG",
        "tipo": "2D • IMAX",
        "genero": "2013 ‧ Comédia/Thriller ‧ 3h",
        "sinopse": "Sinopse: Jordan Belfort é um ambicioso corretor da bolsa de valores que cria um verdadeiro império, enriquecendo de forma rápida, porém ilegal. Ele e seus amigos mergulham em um mundo de excessos, mas seus métodos ilícitos despertam a atenção da polícia."
    },
{
        "id": 13,
        "titulo": "Capitão América: Guerra Civil",
        "horarios": ["15:20", "16:00", "17:00", "18:10", "20:30"],
        "poster": "guerracivil.jpg",
        "audio": "DUB/LEG",
        "tipo": "2D • 3D • IMAX",
        "genero": "2016 ‧ Ação/Ficção científica ‧ 2h 28m",
        "sinopse": "Sinopse: Depois do ataque de Ultron, os políticos decidem controlar os Vingadores, já que suas ações afetam toda a humanidade. A decisão coloca o Capitão América em rota de colisão com o Homem de Ferro."
    },
{
        "id": 14,
        "titulo": "Capitão América: Admirável Novo Mundo",
        "horarios": ["15:20", "16:00", "17:00", "18:10", "20:30"],
        "poster": "novomundo.jpg",
        "audio": "DUB/LEG",
        "tipo": "2D • 3D • IMAX",
        "genero": "2025 ‧ Ação/Ficção científica ‧ 1h 58m",
        "sinopse": "Sinopse: Sam se vê no meio de um incidente internacional após se encontrar com o Presidente Thaddeus Ross. Ele precisa descobrir a razão por trás de um nefasto complô global antes que o verdadeiro mentor faça o mundo inteiro ver vermelho."
    },
]

# Armazenar assentos ocupados
assentos_ocupados = {}

pedidos_realizados = []

@app.route('/')
def home():
    return render_template("home.html", filmes=filmes)

@app.route('/assentos/<int:filme_id>/<horario>')
def selecionar_assentos(filme_id, horario):
    filme = next((f for f in filmes if f["id"] == filme_id), None)
    chave = f"{filme_id}_{horario}"
    ocupados = assentos_ocupados.get(chave, [])
    return render_template("assentos.html", filme=filme, horario=horario, ocupados=ocupados)

@app.route('/comprar', methods=['POST'])
def comprar():
    filme_id = int(request.form['filme_id'])
    horario = request.form['horario']
    assentos = request.form['assentos'].split(',')
    chave = f"{filme_id}_{horario}"
    if chave not in assentos_ocupados:
        assentos_ocupados[chave] = []
    assentos_ocupados[chave].extend(assentos)
    filme = next((f for f in filmes if f["id"] == filme_id), None)
    valor = len(assentos) * 18  # exemplo de valor por assento
    
    dados = {
        "filme": filme['titulo'],
        "horario": horario,
        "assentos": assentos,
        "valor": valor
    }

     # Criar pasta para QR Codes se não existir
    pasta_qrcodes = os.path.join('static', 'qrcodes')
    os.makedirs(pasta_qrcodes, exist_ok=True)

    # Gerar QR Code
    qr_dados = f"Filme: {filme['titulo']}\nHorário: {horario}\nAssentos: {', '.join(assentos)}\nValor: R$ {valor:.2f}"
    qr = qrcode.make(qr_dados)
    nome_arquivo_qr = f"{filme_id}_{horario}_{'_'.join(assentos)}.png".replace(':', '-')
    caminho_qr = os.path.join(pasta_qrcodes, nome_arquivo_qr)
    qr.save(caminho_qr)

    pedidos_realizados.append({
        'filme': filme['titulo'],
        'horario': horario,
        'assentos': assentos,
        'valor': valor,
        'poster': filme['poster'],
        'filme_id': filme_id,
        'qr_code': nome_arquivo_qr  # novo campo
    })

    return render_template("pagamento.html", filme=filme, horario=horario, assentos=assentos, valor=valor, qr_code=nome_arquivo_qr)

@app.route('/meus-pedidos')
def meus_pedidos():
    return render_template('meus_pedidos.html', pedidos=pedidos_realizados, filmes=filmes)  # <-- ADICIONE filmes



if __name__ == '__main__':
    app.run(debug=True)
    