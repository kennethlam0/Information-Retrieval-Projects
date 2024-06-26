from document_text import document_text
# dictionary VIDEOS SUBSET!!
subset_videos = [
    "Training and Testing an Italian BERT - Transformers From Scratch #4",
    "Choosing Indexes for Similarity Search (Faiss in Python)",
    "Training BERT #4 - Train With Next Sentence Prediction (NSP)",
    "Build NLP Pipelines with HuggingFace Datasets",
    "How-to do Sentiment Analysis with Flair in Python",
    "How to Build Custom Q&A Transformer Models in Python",
    "How to Build Q&A Models in Python (Transformers)",
    "How-to Structure a Q&A ML App",
    "Streamlit for ML #5.1 - Custom React Components in Streamlit Setup",
    "Making The Most of Data: Augmented SBERT",
    "How-to use the Kaggle API in Python",
    "API Series #2 - Building an API with Flask in Python",
    "Locality Sensitive Hashing (LSH) for Search with Shingling + MinHashing (Python)",
    "How to Index Q&A Data With Haystack and Elasticsearch",
    "Training BERT #5 - Training With BertForPretraining",
    "Q&A Document Retrieval With DPR",
    "Hugging Face Datasets #2 - Dataset Builder Scripts",
    "Fast intro to multi-modal ML with OpenAI's CLIP",
    "All You Need to Know on Multilingual Sentence Vectors (1 Model, 50+ Languages)",
    "Faiss - Introduction to Similarity Search",
    "API Series #3 - How to Deploy Flask APIs to the Cloud (GCP)",
    "The NEW Match-Case Statement in Python 3.10",
    "CLIP Explained | Multi-modal ML",
    "How to build a Q&A AI in Python (Open-domain Question-Answering)",
    "Adding a tutorial option - Tkinter tutorial Python 3.4 part 19",
    "Spurious normativity enhances learning of compliance and enforcement behavior in artificial agents",
    "[ML News] Microsoft combines Images & Text | Meta makes artificial skin | Russians replicate DALL-E",
    "[ML News] DeepMind's Flamingo Image-Text model | Locked-Image Tuning | Jurassic X & MRKL",
    "The Hardware Lottery (Paper Explained)",
    "[Code] PyTorch sentiment classifier from scratch with Huggingface NLP Library (Full Tutorial)",
    "Language Models are Open Knowledge Graphs (Paper Explained)",
    "Neural Networks from Scratch - P.4 Batches, Layers, and Objects",
    "How I Read a Paper: Facebook's DETR (Video Tutorial)",
    "A. I. Learns to Play Starcraft 2 (Reinforcement Learning)",
    "SynFlow: Pruning neural networks without any data by iteratively conserving synaptic flow",
    "I COOKED A RECIPE MADE BY A.I. | Cooking with GPT-3 (Don't try this at home)",
    "Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents (+Author)",
    "[ML News] Google introduces Pathways | OpenAI solves Math Problems | Meta goes First Person",
    "Implicit MLE: Backpropagating Through Discrete Exponential Family Distributions (Paper Explained)",
    "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity",
    "Optimizing Neural Network Structures with Keras-Tuner",
    "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift",
    "GPIO Basics with LED light - Raspberry Pi and Python tutorials p.6",
    "How far can we scale up? Deep Learning's Diminishing Returns (Article Review)",
    "Line Finding with Hough Lines - Python plays Grand Theft Auto 5 p.5",
    "Pickling and Scaling - Practical Machine Learning Tutorial with Python p.6",
    "Linformer: Self-Attention with Linear Complexity (Paper Explained)",
    "BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding&Generation",
    "Naive Bayes - Natural Language Processing With Python and NLTK p.13"
]
# dictionary for our document freq
document_freq_pr = {}
# for each title and list of words in document_text
for title, list_words in document_text.items():
    # for each word in the list of words
    if not title in subset_videos:
        # IF NOT IN SUBSET, CONTINUE
        continue

    # for each word in the list of words
    for word in list_words:
        # if the word is not in the dictionary, add it 
        document_freq_pr[word] = document_freq_pr.get(word, 0) + 1

#print(document_freq_pr)

