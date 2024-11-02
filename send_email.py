from email.message import EmailMessage
import ssl
import smtplib
import pandas as pd

# Load data
planilhaDados = pd.read_csv('data.csv')

# Sender credentials and details
email_sender = ''
email_password = ''
recrutadora = "Larissa Fiore"
subject = 'Convite para Entrevista - Vaga de Vendedor, Auxiliar de Loja e Operador de Caixa'

# Set up SSL context
context = ssl.create_default_context()

# Loop through each row to send individual emails
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    
    for index, row in planilhaDados.iterrows():
        # Extract individual details for each email
        email_receiver = row['email']
        nome = row['nome']
        nome_vaga = row['nome_vaga']
        data = row['data']
        hora = row['hora']
        local = row['local']
        
        # Customize the email body with HTML content and embedded image
        body = f"""
        <html>
            <body>
                <h2>Prezado(a) {nome},</h2>
                <p>Você foi selecionado(a) para participar de uma entrevista para a vaga de <b>{nome_vaga}</b> em nossa empresa, Taco.</p>
                <p><strong>Detalhes da Entrevista:</strong></p>
                <ul>
                    <li>Data: {data}</li>
                    <li>Horário: {hora}</li>
                    <li>Local: {local}</li>
                </ul>
                <p>Por favor, confirme sua presença até a Data Limite para Confirmação.</p>
                <p>Agradecemos seu interesse em nossa empresa e esperamos por sua presença.</p>
                <p>Atenciosamente,<br>{recrutadora}</p>
                <p><img src="cid:company_logo" alt="Logo da Empresa" width="500" height="auto"></p>
            </body>
        </html>
        """
        
        # Set up the email message
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body, subtype='html')
        
        # Open image file in binary mode
        with open('taco_banner.jpg', 'rb') as img:
            em.add_attachment(img.read(), maintype='image', subtype='jpg', filename='taco_banner.jgp', cid='company_logo')
        
        # Send the email
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        print(f"Email sent to {email_receiver}")
