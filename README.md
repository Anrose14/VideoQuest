# VideoQuest
A Question Answering System for Youtube Videos

- The Flask application that is given has a system architecture that is designed to enable smooth user interaction with YouTube video material by utilizing natural language processing (NLP) capabilities. The program runs mostly on a client-server architecture, which is accessed by users via a web browser. Several routes are built inside the Flask application to handle different features, such question answering, video summarizing, and display of the home page.

- The incorporation of pretrained natural language processing (NLP) models, such as DistilBERT for question answering and T5 for text summarization, is a crucial element of the system design. The Flask application loads and initializes these models, which are then in charge of things like tokenization, model inference, and result interpretation. They process text inputs like user inquiries and video transcripts and provide useful outputs like text summaries and response to queries. By using cutting-edge NLP algorithms, the program is better able to comprehend and analyze YouTube video material, giving users insightful information.
The program connects with various APIs and services in addition to NLP components to retrieve information and transcripts from YouTube videos. For instance, it uses user-provided video URLs to collect transcripts using the YouTube Data API. 

- Using HTML templates, the application's user interface is produced and sent to the client browser using Flask's template rendering system. In order to encourage user involvement and engagement, these templates include dynamic features like form inputs, result displays, and interactive components. They also specify the structure, layout, and content of the web pages that are shown to users.

**How to run the code ?**
- Clone the repository locally or download the zip file
- pip install -r requirements.txt
- run app.py (necassary requirements should be downloaded)
