# Chatbot code --> Written by Pejman Ebrahimi --> email: pejman.ebrahimi77@gmail.com 
import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load model and tokenizer
def load_model():
    model_name = "Qwen/Qwen2.5-3B-Instruct"
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    return model, tokenizer

# Generate response
def generate_response(model, tokenizer, message, history):
    # Format conversation history for the model
    messages = [
        {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."}
    ]
    
    # Add conversation history
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
    
    # Add current message
    messages.append({"role": "user", "content": message})
    
    # Apply chat template
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    # Generate response
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512,
        temperature=0.7,
        do_sample=True
    )
    
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    return response

# Chatbot function
def chatbot(message, history):
    response = generate_response(model, tokenizer, message, history)
    return response

# Load model and tokenizer
print("Loading model and tokenizer...")
model, tokenizer = load_model()
print("Model loaded successfully!")

# UI
demo = gr.ChatInterface(
    fn=chatbot,
    title="Qwen2.5-3B-Instruct General Chatbot",
    description="This is a general chatbot powered by Qwen2.5-3B-Instruct to answer your questions.",
    examples=["Tell me about consumer sustainable behavior", 
              "How AI games can help consumer sustainable behavior?", 
              "How parents can encourage chldren to support sustainable purchase?"],
    theme="soft"
)

demo.launch(share=True)