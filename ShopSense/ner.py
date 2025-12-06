import spacy

# Load spaCy transformer NER
nlp = spacy.load("en_core_web_lg")

def ner_extract(text: str):
    doc = nlp(text)
    ents = []
    for ent in doc.ents:
        ents.append({"text": ent.text, "label": ent.label_})
    return ents
