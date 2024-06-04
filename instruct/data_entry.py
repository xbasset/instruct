import jsonlines
from datetime import datetime
from pathlib import Path
import filecmp

class DataEntry:
    def __init__(self, instruct_file_path, query=None, response=None, evaluation=None, model=None):
        try:
            self.instruct_file_path = Path(instruct_file_path)
            self.instruct_file_name = self.instruct_file_path.stem
            self.query = query
            self.response = response
            self.evaluation = evaluation
            self.model = model
            self.dateCreated = datetime.now().isoformat()
            self.default_path = Path.home() / ".instruct" / "dataset"
            self.dataset_path = self.default_path / self.instruct_file_name
            self.version_path = self._determine_version_path()
        except Exception as e:
            print(f"Error initializing DataEntry: {e}")
            raise e

    def _determine_version_path(self):
        if not self.dataset_path.exists():
            self.dataset_path.mkdir(parents=True, exist_ok=True)
        
        versions = sorted([d for d in self.dataset_path.iterdir() if d.is_dir() and d.name.isdigit()], key=lambda x: int(x.name))
        
        if not versions:
            new_version_path = self.dataset_path / "1"
            new_version_path.mkdir()
            return new_version_path
        
        latest_version_path = versions[-1]
        latest_instruct_file = latest_version_path / self.instruct_file_path.name
        
        current_instruct_file_path = self.instruct_file_path
        
        # compare the content of the latest instruct file with the current instruct file
        if latest_instruct_file.exists() and filecmp.cmp(latest_instruct_file, current_instruct_file_path, shallow=False):
            return latest_version_path
        else:
            new_version_number = int(latest_version_path.name) + 1
            new_version_path = self.dataset_path / str(new_version_number)
            new_version_path.mkdir()
            return new_version_path

    def _save_current_instruct_file(self):
        instruct_file_path = self.version_path / self.instruct_file_path.name
        if not instruct_file_path.exists():
            with open(instruct_file_path, 'w') as instruct_file:
                # read the file self.instruct_file_name and write its content to instruct_file
                with open(self.instruct_file_path, 'r') as f:
                    instruct_file.write(f.read())
        return instruct_file_path

    def save(self):
        # if the file data.jsonl does not exist, create it and write the data
        # otherwise, append the data to the file
        jsonl_file_path = self.version_path / 'data.jsonl'
        with jsonlines.open(jsonl_file_path, mode='a') as writer:
            writer.write({
                "query": self.query,
                "response": self.response,
                "evaluation": self.evaluation,
                "model": self.model,
                "dateCreated": self.dateCreated
            })
        self._save_current_instruct_file()

