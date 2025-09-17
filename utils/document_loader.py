# Copyright 2025 Alex Erofeev / AIGENTTO
# Created by Alex Erofeev at AIGENTTO (http://aigentto.com/)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from pathlib import Path

def load_all_documents(folder: str) -> list[dict]:
    """
    Loads all .txt files from a folder and returns a list of dictionaries:
    {"name": <filename>, "text": <content>}
    """
    docs = []
    for path in Path(folder).glob("*.txt"):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        docs.append({"name": path.name, "text": text})
    return docs
