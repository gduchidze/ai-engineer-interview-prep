# ვარიანტი 1 – nationality classification
from transformers import pipeline

# classifier = pipeline(
#     "text-classification",
#     model="indigo-ai/BERTino-nationality-classifier"
# )

classifier = pipeline(
    "token-classification",
    model="Jean-Baptiste/roberta-large-ner-english"
)

result = classifier("Hans Mueller")
# → {"label": "Germany", "score": 0.91}