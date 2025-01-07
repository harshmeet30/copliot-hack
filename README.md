# HateShield
HateShield is a project designed to deal with text to provide sentimental analysis with confidence score, severity, key phrases along with counter narrative; and image content moderation to determining acceptance and rejection of the image.


## Installation

Follow these steps to set up HateShield locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/harshmeet30/copliot-hack.git
   cd copliot-hack
   ```

2. Create a virtual environment using Conda:

   ```bash
   conda create --name hateshield python=3.10
   conda activate hateshield
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Utilized Libraries
- streamlit
- azure-ai-textanalytics
- azure-data-tables
- openai
- matplotlib
- plotly
- wordcloud
- python-dotenv
- streamlit-option-menu


## Usage

After installation, you can start using HateShield by running the main script but before that include all the necessary keys and endpoints into the **.env** file:

#### For Azure Open AI
- ENDPOINT_URL=
- DEPLOYMENT_NAME=
- AZURE_OPENAI_API_KEY=

#### For Azure Content Safety
- MODERATOR_ENDPOINT=
- MODERATOR_API_KEY=

#### For Azure Language Service
- LANGUAGE_SERVICE_ENDPOINT=
- LANGUAGE_SERVICE_KEY=

#### For Azure Data Table
- TABLE_STORAGE_CONN_STRING=


After successfully updating the `.env` file you can proceed ahead with running the streamlit App.

```bash
# Run the Streamlit application
streamlit run streamlit_app.py
```

## After Successful Running 
You would be able to see a proper running web application.
![Screenshot 2025-01-07 151001](https://github.com/user-attachments/assets/6861e66d-c345-426d-9dce-939282342de0)



## Project Structure

The repository contains the following files and directories:

- `.env`: Environment variables for sensitive data and configuration.
- `counter_narrative.py`: Script for generating counter-narratives to hate speech.
- `data_storage_tbl.py`: Script for managing data storage for writing and then later reading for dashboarding purpose.
- `languageservice.py`: Script for language processing services.
- `moderator.py`: Script for moderation-related content saftety task for Image.
- `streamlit_app.py`: Streamlit-based web application for HateShield.
- `requirements.txt`: Lists all the Python dependencies for the project.


## Tools and Technologies

This project makes use of the following tools and technologies:

- **GitHub Copilot**: Utilized for code assistance and productivity enhancements.
- **Azure**: Deployed services and utilized Azure resources for scalable and efficient computing.
- **Visual Studio Code**: Employed as the primary development environment, with extensions for debugging, linting, and integration with GitHub.

