import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

import streamlit as st


load_dotenv()


def send_email(receiver_email, file_path, insights):

    sender_email = st.secrets["EMAIL_USER"]
    app_password = st.secrets["EMAIL_PASS"]

    print("USER:", sender_email)
    print("PASS:", app_password)

    msg = EmailMessage()
    msg["Subject"] = "Reporte Automático de Ventas"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content("Adjunto encontrarás el reporte actualizado.")

    html_body = f"""
    <h2>Reporte Automático</h2>
    <p><strong>Insights Clave:</strong></p>
    <ul>
    {''.join(f'<li>{i}</li>' for i in insights)}
    </ul>
    <p>Adjunto encontrarás el reporte completo.</p>
    """

    msg.add_alternative(html_body, subtype="html")

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename=file_path.split("/")[-1]
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)
