import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification

# ---------------------------
# 1. Load model & tokenizer at module level
# ---------------------------
MODEL_PATH = "D:/Downloads/distillbert stress"

print("Loading DistilBERT model and tokenizer...")

# Tokenizer for text preprocessing
tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_PATH)

# Recreate architecture and apply dynamic quantization
base_model = DistilBertForSequenceClassification.from_pretrained(
    "distilbert-base-uncased",
    num_labels=2
)

quantized_model = torch.quantization.quantize_dynamic(
    base_model, {torch.nn.Linear}, dtype=torch.qint8
)

# Load quantized weights
quantized_model.load_state_dict(torch.load("D:\\Downloads\\quantizedbert\\distilbert-stress-quantized.pt", map_location="cpu"))
quantized_model.eval()

print("DistilBERT model loaded and ready!")

# ---------------------------
# 2. Prediction function
# ---------------------------
def predict(text):
    """
    Predicts stress from input text.
    Returns:
        - predicted label: 0 = No Stress, 1 = Stress
        - confidence percentage
    """
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=128
    )

    with torch.no_grad():
        outputs = quantized_model(**inputs)
        logits = outputs.logits
        probs = torch.softmax(logits, dim=1)
        pred_label = torch.argmax(probs, dim=1).item()
        confidence = probs[0][pred_label].item() * 100

    return pred_label, confidence

def categorize(score):
    if (score<65):
        return "Low"
    elif (score<90):
        return "Medium"
    else:
        return "High"
