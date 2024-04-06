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

import streamlit as st
import requests

# ------------------ Streamlit UI Configuration ------------------ #
# Spécifier le titre de la page HTML
st.markdown("<title>AttackGen by trhacknon</title>", unsafe_allow_html=True)

# Modifier le titre de la page lors du partage
st.set_page_config(
    page_title="AttackGen by trhacknon",
    page_icon="👾",
)


# ------------------ Sidebar ------------------ #

with st.sidebar:
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

    st.sidebar.markdown("### <span style='color: #1DB954;'>About</span>", unsafe_allow_html=True)        
    
    st.sidebar.markdown("Modded by [trhacknon](https://www.linkedin.com/in/)")

    st.sidebar.markdown(
        "⭐ Star on GitHub: [![Star on GitHub](https://img.shields.io/github/stars/tucommenceapousser/attackgen?style=social)](https://github.com/tucommenceapousser/attackgen)"
    )


# ------------------ Main App UI ------------------ #

st.markdown("# <span style='color: #1DB954;'>AttackGen by trhacknon 👾</span>", unsafe_allow_html=True)
st.markdown("<span style='color: #1DB954;'> **Use MITRE ATT&CK and Large Language Models to generate attack scenarios for incident response testing.**</span>", unsafe_allow_html=True)
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
