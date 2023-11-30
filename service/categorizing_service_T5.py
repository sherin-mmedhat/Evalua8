import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

class CategorizingUsingTransformersService: 
    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
        self.model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

    def categorize_text(self, categories, text_samples):
        labels = []
        category_str = ", ".join(map(str, categories))
        
        for text in text_samples:
            input_text = f"{text}; Classify this sentence as {category_str} in one word."
            input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
            outputs = self.model.generate(input_ids)
            label = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            labels.append(label)
        
        return labels

# Example usage
categorizing_service = CategorizingUsingTransformersService()
categories = ["Advanced Productivity", "Teamwork"]
text_samples = ["I tried contacting her but she didn't reply for 2 days and this was blocking me for 2 days and made me late"]

# Call the method with the desired arguments
category_labels = categorizing_service.categorize_text(categories, text_samples)
print("Category Labels:", category_labels)
