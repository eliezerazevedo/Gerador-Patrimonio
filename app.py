from flask import Flask, render_template, request
import qrcode
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont
import os
import sqlite3
from datetime import datetime
import pytz  # Importando o pytz para lidar com fusos horários

# Configuração do Flask
app = Flask(__name__)

# Configuração do banco de dados SQLite
db_path = os.path.join(os.getcwd(), "db", "etiquetas.db")
os.makedirs(os.path.dirname(db_path), exist_ok=True)

def init_db():
    """Inicializa o banco de dados."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS etiquetas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INTEGER NOT NULL,
                data_hora DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

# Inicializa o banco de dados
init_db()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Obtém o número inicial e final
        numero_inicial = request.form.get("numero_inicial")
        numero_final = request.form.get("numero_final")

        # Verifica se os números foram preenchidos
        if not numero_inicial or not numero_final:
            return "Por favor, informe os números inicial e final!", 400
        
        # Converte para inteiros e valida
        try:
            numero_inicial = int(numero_inicial)
            numero_final = int(numero_final)
        except ValueError:
            return "Os números devem ser válidos!", 400

        # Gera as etiquetas para o intervalo de números
        etiquetas = []
        numeros_gerados = []
        for numero in range(numero_inicial, numero_final + 1):
            # Define o link com o número inserido
            whatsapp_link = f"https://wa.me/556232742369?text=Ol%C3%A1%2C+preciso+de+suporte+para+meu+equipamento%2C+N%C2%BA+de+patrim%C3%B4nio%3A+{numero:04}"

            # Gera o QR code com o link
            qr = qrcode.QRCode(version=1, box_size=15, border=5)
            qr.add_data(whatsapp_link)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Gera a etiqueta com o número e QR code
            etiqueta = Image.new("RGB", (600, 300), "white")
            draw = ImageDraw.Draw(etiqueta)

            # Define a fonte
            try:
                font = ImageFont.truetype("arialbd.ttf", 18)
            except IOError:
                try:
                    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 18)
                except IOError:
                    font = ImageFont.load_default()

            # Adiciona o número à etiqueta
            draw.text((185, 265), f"PAT{numero:04}", fill="black", font=font)

            # Adiciona o QR code à etiqueta
            qr_img = qr_img.resize((180, 180))
            etiqueta.paste(qr_img, (425, 135))

            # Converte a imagem para base64
            buffer = BytesIO()
            etiqueta.save(buffer, format="PNG")
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            etiquetas.append(img_base64)
            numeros_gerados.append(numero)

        # Grava os números no banco de dados com a data e hora local de São Paulo
        sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            for numero in numeros_gerados:
                # Obtém a data e hora atual no fuso horário de São Paulo
                data_hora = datetime.now(sao_paulo_tz).strftime('%d-%m-%Y %H:%M:%S')
                cursor.execute("INSERT INTO etiquetas (numero, data_hora) VALUES (?, ?)", (numero, data_hora))

            # Mantém apenas os 100 últimos registros
            cursor.execute("DELETE FROM etiquetas WHERE id NOT IN (SELECT id FROM etiquetas ORDER BY id DESC LIMIT 100)")
            conn.commit()

        # Renderiza a página de impressão
        return render_template("print.html", etiquetas=etiquetas)

    # Recupera os 100 últimos números e suas respectivas datas
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT numero, data_hora FROM etiquetas ORDER BY id DESC LIMIT 100")
        etiquetas_anteriores = cursor.fetchall()

    return render_template("index.html", etiquetas_anteriores=etiquetas_anteriores)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5997, debug=True)
