import streamlit as st
import random

# Titre de l'application
st.markdown("""
    <h1 style="color: #1f77b4;">TenX</h1> <h3>your AI prodectivity tool</h3>
""", unsafe_allow_html=True)
st.subheader("Trouvez les concurrents d'une entreprise en utilisant l'IA et des API.")


# Fonction simulée pour récupérer les concurrents
def query_backend_simulated(company_name):
    try:
        # Simule l'appel à un back-end pour obtenir des concurrents
        # Ici, on génère des concurrents factices basés sur le nom de l'entreprise
        competitors = [
            f"{company_name} Concurrent A",
            f"{company_name} Concurrent B",
            f"{company_name} Concurrent C"
        ]
        return {"competitors": competitors}
    except Exception as e:
        # En cas d'erreur, retourner un message d'erreur
        return {"error": f"Erreur lors de la récupération des concurrents : {str(e)}"}


# Vérification du statut du back-end (simulée ici)
def check_backend_status():
    # Simuler une vérification d'état du back-end (ici, une condition aléatoire)
    return random.choice([True, False])  # True ou False de manière aléatoire pour tester


# Entrée utilisateur pour le nom de l'entreprise
company_name = st.text_input("Entrez le nom de l'entreprise :", placeholder="Exemple : Google")

# Bouton pour analyser les concurrents
if st.button("Analyser les concurrents"):
    if company_name:
        st.write(f"Recherche des concurrents pour **{company_name}**...")

        # Vérifier si le back-end est opérationnel (en simulant ici)
        if check_backend_status():
            # Simuler l'appel au back-end pour obtenir les concurrents
            data = query_backend_simulated(company_name)

            if "error" in data:
                st.warning(data["error"])  # Afficher le message d'erreur si l'API échoue
            else:
                st.success("Concurrents trouvés !")
                for competitor in data["competitors"]:
                    st.write(f"- {competitor}")
        else:
            st.warning("Le back-end est actuellement hors service. Affichage de données simulées.")
            # Afficher des données simulées si le back-end est hors service
            st.write("- Concurrent 1 : Microsoft")
            st.write("- Concurrent 2 : Amazon")
            st.write("- Concurrent 3 : Apple")
    else:
        st.warning("Veuillez entrer le nom d'une entreprise.")

# Option pour voir les détails d'un concurrent
if company_name:
    with st.expander("Voir les détails des concurrents"):
        st.write("Détails supplémentaires sur les concurrents ici...")
        # Vous pouvez ajouter des liens, graphiques, etc.
