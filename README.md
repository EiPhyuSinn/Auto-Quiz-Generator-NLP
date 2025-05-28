# MCQ Generator from Text

This project is a **Multiple Choice Question (MCQ) Generator** built with **Streamlit**. It extracts text from `.pdf`, `.docx`, or `.txt` files, identifies key concepts, and generates MCQs automatically.

## Features

- Upload PDF, DOCX, or TXT files
- Generate up to 20 MCQs from the content
- Smart keyword extraction using spaCy
- Automatic distractor (wrong option) generation using WordNet
- Retake quiz button

## Keyword Extraction

To generate a fill-in-the-blank question, we first need to identify a key concept (the keyword) from a sentence.

- Process the text with spaCy (`en_core_web_lg` model)
- Filter out stopwords and punctuation
- Prioritize **NOUNs** that exist in WordNet as the main keyword
- If no suitable NOUN is found, consider **VERBs** or **ADJectives** with WordNet entries
- The first valid token found is chosen as the keyword

## Distractor Generation

To create incorrect options:

- Find WordNet synsets of the keyword
- Use hypernyms and hyponyms to locate related but incorrect words
- If not enough distractors are found, fill in with dummy options

## Question Format

- The sentence is turned into a question by replacing the keyword with `"_______"`
- One correct answer + up to 3 distractors = 4 shuffled options
- The correct answer is tracked for scoring
  
## UI Steps by Steps
1) Upload file and select number of MCQs
      ![Screenshot from 2025-05-28 16-19-52](https://github.com/user-attachments/assets/d4708bbd-4026-421d-9b7a-4bada058c2f2)
2) Answer questions 
      ![Screenshot from 2025-05-28 16-25-27](https://github.com/user-attachments/assets/019b57f3-76d4-4b15-838e-e5fbcbd71f13)

3) You can check the answers and retake the quiz
     ![Screenshot from 2025-05-28 16-25-36](https://github.com/user-attachments/assets/de4860c0-dbd8-4b74-9733-ca75fd5235ea)



## Installation

```bash
pip install -r requirements.txt
python -m nltk.downloader wordnet
python -m spacy download en_core_web_lg
