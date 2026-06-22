import json
from dataclasses import dataclass
from enum import Enum
from typing import List

class ComplianceStatus(Enum):
    COMPLIANT = 1
    NON_COMPLIANT = 2
    UNKNOWN = 3

@dataclass
class ChecklistItem:
    name: str
    description: str
    status: ComplianceStatus

class VaultCal:
    def __init__(self):
        self.checklist = [
            ChecklistItem("TLS enabled", "Transport Layer Security is enabled", ComplianceStatus.UNKNOWN),
            ChecklistItem("Data encryption at rest", "Data is encrypted at rest", ComplianceStatus.UNKNOWN),
        ]

    def verify_checklist(self):
        # Simulate verification process
        for item in self.checklist:
            if item.name == "TLS enabled":
                item.status = ComplianceStatus.COMPLIANT
            elif item.name == "Data encryption at rest":
                item.status = ComplianceStatus.COMPLIANT

    def export_to_pdf(self):
        # Simulate export to PDF process
        pdf_content = ""
        for item in self.checklist:
            pdf_content += f"{item.name}: {item.status.name}\n"
        return pdf_content

    def get_checklist(self):
        return self.checklist
