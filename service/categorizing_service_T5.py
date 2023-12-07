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
            input_text = f"Classify the following sentence: '{text}' as one of the following: {category_str}."
            input_ids = self.tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.model.generate(input_ids, max_length=50)
            label = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Check if the label contains any of the specified categories
            predicted_categories = [category for category in categories if category.lower() in label.lower()]
            
            if predicted_categories:
                labels.append(predicted_categories)
            else:
                labels.append(['Does not belong to any category'])
        
        return labels

# Example usage
categorizing_service = CategorizingUsingTransformersService()
categories = ["Productivity", "Teamwork"]
text_samples = ["She is good", "She delivers all tasks on time", "I tried contacting her but she didn't reply for 2 days and this was blocking me for 2 days and made me late"]

# Call the method with the desired arguments
category_labels = categorizing_service.categorize_text(categories, text_samples)
print("Category Labels:", category_labels)
