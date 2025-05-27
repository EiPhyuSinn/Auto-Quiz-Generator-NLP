import nltk
import re
import random
import spacy 
import string
from nltk.corpus import wordnet as wn
from collections import Counter
nltk.download('wordnet')

nlp = spacy.load('en_core_web_lg')
NER_CACHE = {}

def get_ner_list(text):
    if text not in NER_CACHE:
        doc = nlp(text)
        NER_CACHE[text] = {}
        for ent in doc.ents:
            NER_CACHE[text].setdefault(ent.label_, []).append(ent.text)
    return NER_CACHE[text]

def extract_keywords(sent):
    doc = nlp(sent)
    ner_nouns = [ent.text for ent in doc.ents if ent.label_ and nlp(ent.text)[0].pos_ == "NOUN"]
    if ner_nouns:
        return ner_nouns[0]
    nouns = [token.text for token in doc if token.pos_ == "NOUN"]
    noun_freq = Counter(nouns)
    for noun, _ in noun_freq.most_common():
        if wn.synsets(noun, pos='n'):
            return noun

    return None  # If no valid noun with synset is found

def extract_distractors(word,text):
    doc = nlp(word)
    lemma = doc[0].lemma_.lower()
    distractors = []
    if NER_CACHE:
        for key, values in NER_CACHE.items():
            if lemma in [nlp(v)[0].lemma_.lower() for v in values]:
                related_distractors = [v for v in values if nlp(v)[0].lemma_.lower() != lemma]
                if len(related_distractors) < 3:
                    synsets = wn.synsets(lemma, pos='n')
                    if synsets:
                        wn_distractors = get_distractors_wordnet(synsets[0], lemma)
                        distractors = related_distractors + wn_distractors
                        return distractors[:3]
                return related_distractors[:3]

    synsets = wn.synsets(lemma, pos='n')
    if synsets:
        distractors = get_distractors_wordnet(synsets[0], lemma)

    return distractors[:3] if distractors else []

def get_distractors_wordnet(syn, word):
    distractors = []
    word = word.lower().replace(" ", "_")
    orig_word = word
    hypernyms = syn.hypernyms()
    if not hypernyms:
        return distractors
    for item in hypernyms[0].hyponyms():
        name = item.lemmas()[0].name()
        if name == orig_word:
            continue
        name = " ".join(w.capitalize() for w in name.replace("_", " ").split())
        if name and name not in distractors:
            distractors.append(name)
    return distractors

def format_mcqs(questions):
    formatted = {}

    for qid, qdata in questions.items():
        all_options = qdata['options'] + [qdata['answer']]
        random.shuffle(all_options)

        # Map options to letters A, B, C, ...
        option_labels = list(string.ascii_uppercase)
        options = {option_labels[i]: opt for i, opt in enumerate(all_options)}

        # Find which letter is the correct answer
        correct_letter = next(k for k, v in options.items() if v == qdata['answer'])

        formatted[qid] = {
            'question': qdata['question'],
            'options': options,
            'answer': correct_letter
        }

    return formatted

def text_to_questions_pipeline(text_file,max_choice=5):
    with open(text_file, encoding="utf-8") as f:
        text = f.read()
    
    text = text.replace("\n", " ").strip()
    text = re.sub(r'\s+', ' ', text)
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents if sum(1 for token in sent if token.pos_ == 'NOUN') >= 2]
    chosen_sents = random.sample(sentences, max_choice)
    questions = {}
    for i, sent in enumerate(chosen_sents):
        keyword = extract_keywords(sent)
        if keyword:
            distractors = extract_distractors(keyword,text)
            question_sent = sent.replace(keyword, "_______")
            questions[i+1] = {
                'question': question_sent,
                'answer': keyword,
                'options': [keyword] + distractors[:3] 
            }
    return format_mcqs(questions)

if __name__ == "__main__":
    questions = text_to_questions_pipeline("input/universe.txt",max_choice=10)

    for q_id, q in questions.items():
        print(f"Q{q_id}: {q['question']}")
        for opt, val in q['options'].items():
            print(f"  {opt}) {val}")
        print(f"Answer: {q['answer']}\n")
