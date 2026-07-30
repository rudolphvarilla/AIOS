"""
===========================================================
AIOS Keyword Exporter
core/keywords/tools/exporter.py
===========================================================

Converts reviewed keywords into production registry format.

Version 1
Currently exports registry text only.

Future
• Write Python registry modules
• Version history
• Backup previous registry
• Merge manual keywords
• Git integration
===========================================================
"""

class KeywordExporter:

    def export(self, reviewed):

        output = {}

        for domain, keywords in reviewed.items():

            lines = []

            lines.append(f"{domain.upper()}_KEYWORDS = {{")

            for keyword in keywords:

                lines.append(f'    "{keyword}",')

            lines.append("}")

            output[domain] = "\n".join(lines)

        return output