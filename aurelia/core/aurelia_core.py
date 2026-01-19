"""
AURELIA CORE SYSTEM — Version 0.1
Author: Hikmet Pınarbaş
AI Assistant: GPT-5

📘 Purpose:
Acts as the neural bridge connecting all Aurelia modules (PreMatch, PostMatch, Individual, etc.)
Each module communicates through the Meaning Transfer Protocol (MTP) and shares contextual awareness.

💡 Scientific Foundation:
- Rein & Memmert (2016), "Big Data and Tactical Analysis in Football"
- Liu et al. (2019), "Spatiotemporal Data and Team Dynamics"
- Dawkins (1982), "The Extended Phenotype"
- Popper (1959), "Logic of Scientific Discovery"
"""

import os
import json
import importlib
from datetime import datetime

class AureliaCore:
    def __init__(self, data_path="./AURELIA_DATA", config_file="aurelia_config.json"):
        self.data_path = data_path
        self.config = self.load_config(config_file)
        self.memory_file = os.path.join(self.data_path, "match_memory.json")
        self.modules = {}
        self.initialize_memory()

    def load_config(self, config_file):
        """Load or create system configuration."""
        try:
            with open(config_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            config = {"active_modules": ["pre_match", "post_match", "team", "video", "body", "general"]}
            with open(config_file, "w") as f:
                json.dump(config, f, indent=4)
            return config

    def initialize_memory(self):
        """Create or load historical match memory."""
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, "w") as f:
                json.dump({}, f)

    def register_module(self, name):
        """Dynamically import and register modules."""
        try:
            module = importlib.import_module(f"aurelia.modules.{name}")
            self.modules[name] = module
            print(f"[AURELIA] Module '{name}' loaded successfully.")
        except Exception as e:
            print(f"[ERROR] Could not load module {name}: {e}")

    def connect_all_modules(self):
        """Load all active modules defined in config."""
        for name in self.config["active_modules"]:
            self.register_module(name)

    def fetch_last_match(self):
        """Retrieve last processed match info from memory."""
        with open(self.memory_file, "r") as f:
            memory = json.load(f)
        if memory:
            last_key = sorted(memory.keys())[-1]
            return memory[last_key]
        return None

    def process_new_match(self, match_file):
        """
        Automatically determines file type and triggers relevant modules.
        """
        print(f"[AURELIA] Processing new file: {match_file}")
        if match_file.endswith(".xlsx"):
            self.trigger_pipeline("pre_match", match_file)
            self.trigger_pipeline("post_match", match_file)
        elif match_file.endswith(".csv") or match_file.endswith(".xml"):
            self.trigger_pipeline("post_match", match_file)
        else:
            print("[AURELIA] Unsupported file format.")

    def trigger_pipeline(self, module_name, file_path):
        """Executes a specific module on the given file."""
        try:
            mod = self.modules.get(module_name)
            if not mod:
                print(f"[WARN] Module '{module_name}' not loaded.")
                return
            print(f"[AURELIA] Running {module_name} on {file_path} ...")
            mod.run(file_path)
        except Exception as e:
            print(f"[ERROR] {module_name} failed: {e}")

    def record_match_result(self, match_id, data):
        """Save processed match results to memory."""
        with open(self.memory_file, "r") as f:
            memory = json.load(f)
        memory[str(match_id)] = {"timestamp": datetime.now().isoformat(), "summary": data}
        with open(self.memory_file, "w") as f:
            json.dump(memory, f, indent=4)
        print(f"[AURELIA] Match {match_id} saved to memory.")