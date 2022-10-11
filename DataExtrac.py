from matplotlib.pyplot import text
import spacy
from spacy import displacy

text = "These new paracetamol from Pfizer are giving me cancer."

nlp = spacy.load("en_core_sci_lg")
doc = nlp(text)
displacy.serve(doc, style="ent")


