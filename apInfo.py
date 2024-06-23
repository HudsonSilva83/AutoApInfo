from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#imports do email
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Inicialize o driver do Chrome (ou qualquer outro navegador)
# driver = webdriver.Chrome()

# Inicialize o driver do Chrome
# options = webdriver.ChromeOptions()
options = webdriver.FirefoxOptions()
options.add_argument('--headless')  # Executar em modo headless (sem interface gráfica)
# driver = webdriver.Chrome(options=options)
driver = webdriver.Firefox(options=options)



# URL da página da web que você deseja acessar
url = 'https://www.vivareal.com.br/imovel/apartamento-2-quartos-mantiqueira-bairros-belo-horizonte-com-garagem-68m2-venda-RS260000-id-2661505559/'

# Abra a URL no navegador
driver.get(url)

# Aguarde até que o elemento esteja visível

elemento = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.lead-numbers p"))
)

valor = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.XPATH, "//*[@id='js-site-main']/div[2]/div[2]/div[1]/div/div[1]/div/h3"))
)


# tratando os valores
valorTexto = valor.text
x = (slice(3,6))
sovalor = (valorTexto[x])
valorNum = int(sovalor)
texto = elemento.text

# Imprima o texto
numero = int(texto[5])
print(numero)
# Feche o navegador
driver.quit()

# Configurações do servidor SMTP do Gmail
smtp_server = 'smtp.gmail.com'
smtp_port = 587  # Porta para TLS

# Informações da conta de email
import os

# Informações da conta de email
sender_email = os.getenv('SENDER_EMAIL')
sender_password = os.getenv('SENDER_PASSWORD')
receiver_email = os.getenv('RECEIVER_EMAIL')



#sender_email = 't800.hma@gmail.com'
#sender_password = 'lqceveoatljdctvm'  # Recomenda-se usar variáveis de ambiente para senhas
# Destinatário
#receiver_email = 'hu.psilva@gmail.com'

# Mensagem de email
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = 'Atualização de Valores'

# Corpo do email
if valorNum > 260:
    body = f"O valor foi aumentado para {valorNum} mil. Mais de {numero} pessoas interessadas neste imóvel nas últimas horas."
elif valorNum < 260:
    body = f"O valor foi diminuído para {valorNum} mil. Mais de {numero} pessoas interessadas neste imóvel nas últimas horas."
else:
    body = f"O valor foi mantido em {valorNum} mil. Mais de {numero} pessoas interessadas neste imóvel nas últimas horas."

message.attach(MIMEText(body, 'plain'))

# Conexão e envio do email
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    print('Email enviado com sucesso!')
except Exception as e:
    print(f'Erro ao enviar email: {str(e)}')
finally:
    server.quit()