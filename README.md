# Topic Modeling and Visualization of ArXiv Papers

This project leverages topic modeling techniques to analyze research papers from [arXiv](https://arxiv.org). The dataset used for this project is sourced from the arXiv.org repository, which includes research papers across a wide range of scientific disciplines. The project implements topic modeling using Latent Dirichlet Allocation (LDA) and Term Frequency Inverse Document Frequency (TF-IDF), performed using Python and SpaCy for natural language processing.

## Features

- **Topic Modeling**: Uses Latent Dirichlet Allocation (LDA) to uncover topics in research papers over multiple years.
- **Interactive Visualizations**: Provides interactive graphs (e.g., bar plots, heatmaps) to explore the trends in topics over time.
- **Year & Category Filtering**: Users can filter topics by year and category, allowing for a detailed analysis of the research landscape.
- **Topic Exploration**: Users can explore topics in more detail, with top words and their distributions.

## Backend

The backend of the project is built with Python, utilizing the SpaCy library for natural language processing. The backend is responsible for processing the raw data from arXiv, performing exploratory data analysis (EDA), and running the topic modeling algorithm.

### Technologies Used:

- **Python**: For data processing, analysis, and LDA implementation.
- **SpaCy**: A natural language processing library used to preprocess the data (tokenization, lemmatization).
- **scikit-learn**: For LDA (Latent Dirichlet Allocation).
- **Matplotlib / Plotly**: For visualization of topics and trends.

## Frontend

The frontend is built with React and uses Plotly for interactive data visualizations. It includes various charts like bar plots, scatter plots, and heatmaps, which display the results of topic modeling. The user can filter topics by year and category and explore the trends visually.

### Key Features of the Frontend:

- **React**: For building the user interface.
- **React Plotly**: For creating interactive charts and visualizations.
- **CSS Grid**: For organizing content in a responsive and organized layout.

## Project Setup

### Backend Setup:

1. Clone the repository to your local machine.

   ```bash
   git clone <repository-url>
   ```

2. Navigate to the backend directory:

   ```bash
   cd backend
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Python script to process the arXiv data and perform topic modeling.

### Frontend Setup:

1. Clone the repository to your local machine.

   ```bash
   git clone <repository-url>
   ```

2. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

3. Install the required dependencies:

   ```bash
   npm install
   ```

4. Start the frontend server:

   ```bash
   npm start
   ```

## Sample Data

The dataset used in this project consists of research papers from [arXiv](https://arxiv.org). The data was collected across several years, covering different scientific categories such as Artificial Intelligence, Computer Vision, and Machine Learning. This data is processed to uncover the main topics and their evolution over time.
