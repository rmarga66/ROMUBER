import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Configuration de l'email d'envoi
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "romainmargalet@gmail.com"
EMAIL_PASSWORD = "oipm xjxx lyab obeq"  # Remplacez par votre mot de passe (ou utilisez une méthode sécurisée)

# Fonction pour envoyer un email
def envoyer_email(destinataire, sujet, contenu):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = destinataire
        msg["Subject"] = sujet

        msg.attach(MIMEText(contenu, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, destinataire, msg.as_string())

        return True
    except Exception as e:
        st.error(f"Erreur lors de l'envoi de l'email : {e}")
        return False

# Interface Streamlit
st.set_page_config(page_title="ROMUBER", layout="wide")  # Met une mise en page large

st.title("ROMUBER - Interface de réservation")

# Formulaire utilisateur
with st.form("formulaire_demande"):
    nom = st.text_input("Nom :")
    prenom = st.text_input("Prénom :")
    telephone = st.text_input("Téléphone :")
    email = st.text_input("Email :")

    st.markdown("### Choix de prestations :")
    prestation1 = st.checkbox("Prestation 1")
    prestation2 = st.checkbox("Prestation 2")
    prestation3 = st.checkbox("Prestation 3")

    commentaires = st.text_area("Commentaires :")

    date_heure = st.date_input("Date souhaitée :")
    heure = st.time_input("Heure souhaitée :")

    submit = st.form_submit_button("Envoyer la demande")

# Gestion de la soumission du formulaire
if submit:
    if not (nom and prenom and telephone and email):
        st.error("Veuillez remplir tous les champs obligatoires.")
    else:
        # Création du récapitulatif
        prestations_choisies = []
        if prestation1:
            prestations_choisies.append("Prestation 1")
        if prestation2:
            prestations_choisies.append("Prestation 2")
        if prestation3:
            prestations_choisies.append("Prestation 3")

        recapitulatif = f"""
        Bonjour {prenom} {nom},

        Voici un récapitulatif de votre demande :
        - Téléphone : {telephone}
        - Email : {email}
        - Prestations choisies : {', '.join(prestations_choisies) if prestations_choisies else 'Aucune'}
        - Commentaires : {commentaires}
        - Date et heure : {date_heure} à {heure}

        Bien à vous,
        ROMUBER
        """

        # Envoi de l'email
        if envoyer_email(
            destinataire=email,
            sujet="Récapitulatif de votre demande - ROMUBER",
            contenu=recapitulatif.replace('\n', '<br>'),
        ):
            st.success("Votre demande a été envoyée avec succès !")
        else:
            st.error("Une erreur est survenue lors de l'envoi de votre demande.")
