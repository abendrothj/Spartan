import mlx.core as mx
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_image

class VisionBrain:
    def __init__(self, model_path="mlx-community/Llama-3.2-11B-Vision-Instruct-4bit"):
        print(f"Loading Slow Brain: {model_path}...")
        self.model, self.processor = load(model_path)
        print("Slow Brain Loaded.")

    def see_and_think(self, image_path, history_context=""):
        """
        Analyzes the image and history to produce a high-level goal.
        Args:
            image_path (str): Path to the temporary screenshot.
            history_context (str): Text describing recent actions/results.
        Returns:
            str: The generated thought/plan.
        """
        
        system_prompt = (
            "You are an intelligent Minecraft Agent. "
            "Your goal is to survive and thrive. "
            "Analyze the image and the recent history. "
            "Output a concise logic chain and a final ACTION."
        )
        
        user_content = f"History: {history_context}\nWhat should I do next?"
        
        # Manual Prompt Construction for Llama 3.2 Vision
        # apply_chat_template seems to be failing to handle the list[dict] content structure correctly
        # content = f"<|image|>\n{user_content}"
        # prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{content}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        # Simpler approach matching mlx-vlm examples for Llama 3.2:
        prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n<|image|>\n{user_content}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
        
        # Explicitly load image to ensure valid data
        try:
             image = load_image(image_path)
        except Exception as e:
             return f"Error loading image: {e}"

        output = generate(self.model, self.processor, prompt, image, max_tokens=100, verbose=False)
        return output

if __name__ == "__main__":
    # fast test
    print("Testing VisionBrain initialization (requires actual model download first run)...")
    try:
        brain = VisionBrain()
        print("Success.")
    except Exception as e:
        print(f"Failed to load: {e}")
