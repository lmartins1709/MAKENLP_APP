from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import torch

class QuestionAnsweringModel:
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None

    def load_model(self):
        if self.model is None:
            self.model = AutoModelForQuestionAnswering.from_pretrained(self.model_name)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

    def generate_answer(self, question, context):
        if self.model is None:
            raise ValueError("Model not loaded. Call load_model() first.")

        inputs = self.tokenizer(question, context, return_tensors="pt")
        outputs = self.model(**inputs)
        answer_start = torch.argmax(outputs.start_logits)
        answer_end = torch.argmax(outputs.end_logits) + 1
        answer = self.tokenizer.convert_tokens_to_string(
            self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][answer_start:answer_end])
        )
        return answer
