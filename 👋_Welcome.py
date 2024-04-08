"""
Copyright (C) 2023, Matthew Adams

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or 
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

A copy of the licence is provided with this program. If you are unable
to view it, please see https://www.gnu.org/licenses/
"""

import requests
import streamlit as st
import os

# Récupérer l'e-mail à partir de la variable d'environnement
email = os.getenv("STREAMLIT_EMAIL")

# Si l'e-mail n'est pas défini, demandez-le à l'utilisateur
if email is None:
    email = os.getenv("STREAMLIT_EMAIL")

# ------------------ Streamlit UI Configuration ------------------ #




# Télécharger l'image SVG localement
url = "https://trknmgl-paygen.replit.app/trkn.svg"
response = requests.get(url)
with open("trkn.svg", "wb") as f:
    f.write(response.content)
    email="jeremydiliotti@gmail.com"
# Configurer la page avec l'icône SVG local
st.set_page_config(
    page_title="AttackGen by trhacknon",
    page_icon="trkno.svg"
)


# ------------------ Sidebar ------------------ #
with st.sidebar:
    # Ajoutez vos styles CSS pour personnaliser la barre latérale ici

    st.markdown(
        """
        <style>
        /* Styles pour la barre latérale */
        .sidebar .sidebar-content {
            background-color: #00ffff !important; /* Couleur de fond */
            color: #000000 !important; /* Couleur du texte */
            border-right: 2px solid #00ff00 !important; /* Bordure de côté */
        }
        .sidebar .sidebar-content .sidebar-section .sidebar-section-content {
            padding: 20px !important; /* Espacement interne */
        }
        .sidebar .sidebar-content .sidebar-section .sidebar-section-content .stMarkdown a {
            color: #ff6200 !important; /* Couleur des liens */
        }
        /* Style pour le titre 'Setup' */
        .sidebar .sidebar-content .sidebar-section:nth-child(1) .sidebar-section-content .stMarkdown h3 {
            color: #00ffb7 !important; /* Couleur du titre */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Votre contenu de la barre latérale ici
    st.sidebar.markdown("### <span style='color: #1DB954;'>Setup</span>", unsafe_allow_html=True)
    # Add model selection input field to the sidebar
    model_provider = st.selectbox(
        "Select your preferred model provider:",
        ["OpenAI API", "Azure OpenAI Service", "Mistral API", "Ollama"],
        key="model_provider",
        help="Select the model provider you would like to use. This will determine the models available for selection.",
    )

    # Save the selected model provider to the session state
    st.session_state["chosen_model_provider"] = model_provider

    if model_provider == "OpenAI API":
        # Add OpenAI API key input field to the sidebar
        st.session_state["openai_api_key"] = st.text_input(
            "Enter your OpenAI API key:",
            type="password",
            help="You can find your OpenAI API key on the [OpenAI dashboard](https://platform.openai.com/account/api-keys).",
        )

        # Add model selection input field to the sidebar
        model_name = st.selectbox(
            "Select the model you would like to use:",
            ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"],
            key="selected_model",
            help="OpenAI have moved to continuous model upgrades so `gpt-3.5-turbo`, `gpt-4` and `gpt-4-turbo-preview` point to the latest available version of each model.",
        )
        st.session_state["model_name"] = model_name

    if model_provider == "Azure OpenAI Service":
        # Add Azure OpenAI API key input field to the sidebar
        st.session_state["AZURE_OPENAI_API_KEY"] = st.text_input(
            "Azure OpenAI API key:",
            type="password",
            help="You can find your Azure OpenAI API key on the [Azure portal](https://portal.azure.com/).",
        )
        
        # Add Azure OpenAI endpoint input field to the sidebar
        st.session_state["AZURE_OPENAI_ENDPOINT"] = st.text_input(
            "Azure OpenAI endpoint:",
            help="Example endpoint: https://YOUR_RESOURCE_NAME.openai.azure.com/",
        )

        # Add Azure OpenAI deployment name input field to the sidebar
        st.session_state["azure_deployment"] = st.text_input(
            "Deployment name:",
        )
        
        # Add API version dropdown selector to the sidebar
        st.session_state["openai_api_version"] = st.selectbox("API version:", ["2023-12-01-preview", "2023-05-15"], key="api_version", help="Select OpenAI API version used by your deployment.")

    if model_provider == "Mistral API":
        # Add Mistral API key input field to the sidebar
        st.session_state["MISTRAL_API_KEY"] = st.text_input(
            "Enter your Mistral API key:",
            type="password",
            help="You can generate a Mistral API key in the [Mistral console](https://console.mistral.ai/api-keys/).",
        )

        # Add model selection input field to the sidebar
        st.session_state["mistral_model"] = st.selectbox(
            "Select the model you would like to use:",
            ["mistral-large-latest", "mistral-medium-latest", "mistral-small-latest", "open-mixtral-8x7b" ],
            key="selected_model",
        )


    if model_provider == "Ollama":
        # Make a request to the Ollama API to get the list of available models
        try:
            response = requests.get("http://localhost:11434/api/tags")
            response.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xx
        except requests.exceptions.RequestException as e:
            st.error("Ollama endpoint not found, please select a different model provider.")
            response = None

        if response:
            data = response.json()
            available_models = [model["name"] for model in data["models"]]
            # Add model selection input field to the sidebar
            ollama_model = st.selectbox(
            "Select the model you would like to use:",
            available_models,
            key="selected_model",
            )
            st.session_state["ollama_model"] = ollama_model

    st.markdown("""---""")

    # Add the drop-down selectors for Industry and Company Size
    industry = st.selectbox(
    "Select your company's industry:",
    sorted(['Aerospace / Defense', 'Agriculture / Food Services', 
            'Automotive', 'Construction', 'Education', 
            'Energy / Utilities', 'Finance / Banking', 
            'Government / Public Sector', 'Healthcare', 
            'Hospitality / Tourism', 'Insurance', 
            'Legal Services', 'Manufacturing', 
            'Media / Entertainment', 'Non-profit', 
            'Real Estate', 'Retail / E-commerce', 
            'Technology / IT', 'Telecommunication', 
            'Transportation / Logistics'])
    , placeholder="Select Industry")
    st.session_state["industry"] = industry

    company_size = st.selectbox("Select your company's size:", ['Small (1-50 employees)', 'Medium (51-200 employees)', 'Large (201-1,000 employees)', 'Enterprise (1,001-10,000 employees)', 'Large Enterprise (10,000+ employees)'], placeholder="Select Company Size")
    st.session_state["company_size"] = company_size

    st.sidebar.markdown("---")

    st.sidebar.markdown("### <span style='color: #1DB954;'>About trhacknon</span>", unsafe_allow_html=True)        
    
    st.sidebar.markdown("Modded by [trhacknon](https://www.linkedin.com/in/)")

    st.sidebar.markdown(
        "⭐ Star on GitHub: [![Star on GitHub](https://img.shields.io/github/stars/tucommenceapousser/attackgen?style=social)](https://github.com/tucommenceapousser/attackgen)"
    )


# ------------------ Main App UI ------------------ #

st.markdown("# <span style='color: #1DB954;'>AttackGen by trhacknon 👾</span>", unsafe_allow_html=True)
st.markdown("<span style='color: #1DB954;'> **Use MITRE ATT&CK and Large Language Models to generate attack scenarios for incident response testing.**</span>", unsafe_allow_html=True)
st.markdown("<a href='https://trknmgl-paygen.replit.app/trkn.svg' style='display: inline-block; width: 50%; transform: scale(0.5);'><img src='https://trknmgl-paygen.replit.app/trkn.svg' alt='Click to see the source'></a>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""          
            ### Welcome to AttackGen by trhacknon!
            
            The MITRE ATT&CK framework is a powerful tool for understanding the tactics, techniques, and procedures (TTPs) used by threat actors; however, it can be difficult to translate this information into realistic scenarios for testing.

            AttackGen solves this problem by using large language models to quickly generate attack scenarios based on a selection of a threat actor group's known techniques.
            """)

if st.session_state.get('chosen_model_provider') == "Azure OpenAI Service":
    st.markdown("""          
            ### Getting Started

            1. Enter the details of your Azure OpenAI Service model deployment, including the API key, endpoint, deployment name, and API version. 
            2. Select your industry and company size from the sidebar. 
            2. Go to the `Threat Group Scenarios` page to generate a scenario based on a threat actor group's known techniques, or go to the `Custom Scenarios` page to generate a scenario based on your own selection of ATT&CK techniques.
            """)
    
elif st.session_state.get('chosen_model_provider') == "Mistral API":
    st.markdown("""          
            ### Getting Started

            1. Enter your Mistral API key, then select your preferred model, industry, and company size from the sidebar. 
            2. Go to the `Threat Group Scenarios` page to generate a scenario based on a threat actor group's known techniques, or go to the `Custom Scenarios` page to generate a scenario based on your own selection of ATT&CK techniques.
            """)

elif st.session_state.get('chosen_model_provider') == "Ollama":
    st.markdown("""          
            ### Getting Started

            1. Select your locally hosted model from the sidebar, then enter the details of the application you would like to threat model.
            2. Go to the `Threat Group Scenarios` page to generate a scenario based on a threat actor group's known techniques, or go to the `Custom Scenarios` page to generate a scenario based on your own selection of ATT&CK techniques.
            """)

else:
    st.markdown("""
            ### Getting Started

            1. Enter your OpenAI API key, then select your preferred model, industry, and company size from the sidebar. 
            2. Go to the `Threat Group Scenarios` page to generate a scenario based on a threat actor group's known techniques, or go to the `Custom Scenarios` page to generate a scenario based on your own selection of ATT&CK techniques.
            """)