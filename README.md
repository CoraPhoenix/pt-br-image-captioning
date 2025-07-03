# Generating Captions in Brazilian Portuguese using a Fine-Tuned Model

## Introduction

This is a project consisting of fine-tuning an image captioning model to generate captions in Brazilian Portuguese and using the fine-tuned model in a Streamlit app.

## Used Tools and Libraries

The following tools and libraries were used to create this project:

- Kaggle Notebook to fine-tune model;
- `streamlit` and `FastAPI` libraries to develop the app;

## Step-by-Step

### 1. Defining Strategy

The main goal of the project was creating an image captioning model which would be able to generate captions in Brazilian Portuguese using only open-source tools. However, most solutions available tend to perform better on generating English-language captions. Because of that, the selected approach was fine-tuning an existing model so that it would become able to generate captions in Portuguese. 

To do that, a proper dataset and development environment were required. As the environment requires a GPU (given the image captioning models are large) and no local environment fullfils the requirements, the Kaggle Notebooks environment was used. Because of that, a Kaggle Dataset had to be used. The selected dataset was the [Flickr 8k Dataset](https://www.kaggle.com/datasets/adityajn105/flickr8k), which also required using a translation model (given the captions were in English). This also implies the quality of the fine-tuned model would rely on the quality of the translated text used to train it.

### 2. Model Fine-Tuning

In order to create the fine-tuned model, the following steps were performed:

1. Loading the dataset;
2. Translating the captions: to perform the translation, the [Helsinki's opus-mt-tc-big-en-pt](https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-en-pt) model was used;
3. Preparing the dataset;
4. Loading the model to be fine-tuned: the selected model was [Salesforce's BLIP Image Captioning](https://huggingface.co/Salesforce/blip-image-captioning-base);
5. Fine-tuning the model;
6. Saving the fine-tuned model.

The notebook used to train the model can be found [in this link](https://www.kaggle.com/code/christophercamilo/fine-tuning-an-image-captioning-model-to-pt-br), as well as in the [notebooks](/notebooks) folder.

### 3. App Creation

To create the app, `streamlit` and `FastAPI` libraries were used. The former deals with the user interface, while the latter deals with the communication between the app and the model.

## App Layout

The app has a simple layout, composed of a file uploader and a button to start the caption generation process. It also contains a few filters to prevent non-image files to be sent.

![App layout](/app_img/main_page.png)

## How it works

The app operates in a simple linear pattern:

1. User uploads image;
2. User clicks button;
3. The image content is sent through a HTTP Request to the model;
4. While the caption is being generated, a spinner shows up;
5. The model returns the caption through a HTTP response;
6. The app then exhibits the sent image with its respective caption right below.

![App operation example](/app_img/generate_caption.gif)

## Next steps

Here are the possible next steps, but suggestions are always welcome ^_^:

1. Add text-to-speech
2. Improve model

