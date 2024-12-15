from flask import Flask, render_template, request
import qrcode
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

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
        for numero in range(numero_inicial, numero_final + 1):
            # Define o link com o número inserido
            whatsapp_link = f"https://wa.me/556232742369?text=Ol%C3%A1%2C+preciso+de+suporte+para+meu+equipamento%2C+N%C2%BA+de+patrim%C3%B4nio%3A+{numero:04}"

            # Gera o QR code com o link
            qr = qrcode.QRCode(version=1, box_size=15, border=5)  # Aumenta o box_size para maior resolução
            qr.add_data(whatsapp_link)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Gera a etiqueta com o número e QR code
            etiqueta = Image.new("RGB", (600, 300), "white")  # Aumenta o tamanho da imagem
            draw = ImageDraw.Draw(etiqueta)

            # Define a fonte
            try:
                font = ImageFont.truetype("arialbd.ttf", 18)  # Aumenta o tamanho da fonte
            except IOError:
                try:
                    # Caso a fonte Arial não esteja disponível, tenta uma fonte sans-serif alternativa
                    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 18)  # DejaVuSans Bold, comum em sistemas Linux
                except IOError:
                    # Caso nenhuma fonte seja encontrada, utiliza a fonte padrão
                    font = ImageFont.load_default()

            # Adiciona o número à etiqueta
            draw.text((220, 220), f"PAT{numero:04}", fill="black", font=font)

            # Adiciona o QR code à etiqueta
            qr_img = qr_img.resize((180, 180))  # Ajusta o tamanho do QR code
            etiqueta.paste(qr_img, (425, 125))

            # Converte a imagem para base64
            buffer = BytesIO()
            etiqueta.save(buffer, format="PNG")
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

            etiquetas.append(img_base64)

        # Renderiza a página de impressão
        return render_template("print.html", etiquetas=etiquetas)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5478, debug=True)
