import streamlit as st
import requests
import io
import pathlib
import base64

# ------------------------------- macros ------------------------------ #

IMG_EXTENSIONS = {".jpg": "jpeg", ".jpeg" : "jpeg", ".png" : "png"}

# ------------------------- helper functions -------------------------- #

@st.cache_data
def get_base64_of_bin_file(bin_file): # loads file and converts to a base64 string
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file, brightness = 0.8): # displays the image as a background image
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        filter: brightness({brightness});
    }}
    
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0);
    }}
    
    [data-testid="stToolbar"] {{
        right: 2rem;
    }}

    /* Make other elements visible on darker background */
    .stApp h1, .stApp p, .stApp div {{
        color: white !important;
        text-shadow: 1px 1px 3px black;
    }}
    </style>
    """
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

# ----------------------------- main code ----------------------------- #

set_png_as_page_bg(".\img\photo-pile.jpeg")

st.title("Diga-me o que você vê")

st.write("Insira uma imagem e eu te direi o que eu vejo:")
uploaded_file = st.file_uploader("Insira uma imagem (apenas arquivos .png, .jpg ou .jpeg)")
if uploaded_file: # if file is uploaded, button to send image appears
    send_image = st.button("Enviar imagem")

    # check if uploaded file is an image by analysing its extension
    is_image = pathlib.Path(uploaded_file.name).suffix in [".jpg", ".jpeg", ".png"]

    if send_image and not is_image: # if detected file isn't an accepted image, send warning message
        st.markdown("## Ei! É para me enviar imagens! :unamused:")
    elif send_image: # if detected file is an image, send it to the model
        try:
            with st.spinner("Analisando a imagem recebida..."): # tells user to wait while model is generating caption
                img_type = IMG_EXTENSIONS[pathlib.Path(uploaded_file.name).suffix]
                response = requests.post(
                "http://localhost:8000/generate_caption",
                files = {"img": (uploaded_file.name, uploaded_file.getvalue(), f"image/{img_type}")}
            )
            if response.status_code == 200: # if caption is generated successfully, both image and caption are shown
                st.write("Essa é a imagem que você me mandou:")
                st.image(io.BytesIO(uploaded_file.getvalue()))
                st.write("Eu vejo nela...", response.json()["caption"])
            else: # throws an error otherwise
                raise Exception(f"Error trying to generate caption: {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}") # shows error on screen