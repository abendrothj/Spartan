from datetime import datetime
import json

class EpisodicMemory:
    def __init__(self, max_context=5):
        self.history = []
        self.max_context = max_context
        
    def add_episode(self, action, result=""):
        """
        Logs an event.
        Args:
            action (str): The high level action taken (e.g. "Walk Forward")
            result (str): The visual result (e.g. "Hit Wall")
        """
        event = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "action": action,
            "result": result
        }
        self.history.append(event)
        
        # Keep size distinct
        if len(self.history) > 20:
             self.history.pop(0)

    def get_recent_context(self):
        """Returns string formatted for LLM Prompt."""
        recent = self.history[-self.max_context:]
        if not recent:
            return "No recent history."
            
        context_str = "Recent Actions:\n"
        for item in recent:
            context_str += f"- [{item['timestamp']}] Action: {item['action']} -> Result: {item['result']}\n"
            
        return context_str

if __name__ == "__main__":
    mem = EpisodicMemory()
    mem.add_episode("Walk Forward", "Smooth movement")
    mem.add_episode("Jump", "Saw Lava")
    print(mem.get_recent_context())
