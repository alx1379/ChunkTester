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


INSTRUCTION_PATTERNS = [
    r"purpose(.*?)document[:：]",              # Purpose of the document: ...
    r"this document is intended(.*?)\.",      # This document is intended for...
    r"you must(.*?)\.",                       # You must comply with...
    r"please note(.*?)\.",                    # Please note that...
    r"it is important to note(.*?)\.",        # It is important to note that...
    r"the document contains(.*?)\.",          # The document contains information...
    r"this document(.*?)\.",                  # This document regulates...
    r"user manual",                           # Headers
    r"instruction manual",
    r"this document is intended for.*",
    r"it should be noted that.*",
]
