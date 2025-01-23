import subprocess
import json
import os
from typing import Dict, List, Optional
from weasyprint import HTML  # For generating PDF reports

class LicenseChecker:
    def __init__(self, project_type: str):
        self.project_type = project_type

    def get_python_licenses(self) -> Dict[str, str]:
        """Fetch licenses for Python dependencies using pip-licenses."""
        try:
            result = subprocess.run(["pip-licenses", "--format=json"], capture_output=True, text=True)
            if result.returncode != 0:
                print("Error fetching Python licenses:", result.stderr)
                return {}
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error: {e}")
            return {}

    def get_node_licenses(self) -> Dict[str, str]:
        """Fetch licenses for Node.js dependencies using license-checker."""
        try:
            result = subprocess.run(["license-checker", "--json"], capture_output=True, text=True)
            if result.returncode != 0:
                print("Error fetching Node.js licenses:", result.stderr)
                return {}
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error: {e}")
            return {}

    def get_ruby_licenses(self) -> Dict[str, str]:
        """Fetch licenses for Ruby dependencies using license_finder."""
        try:
            result = subprocess.run(["license_finder", "--format=json"], capture_output=True, text=True)
            if result.returncode != 0:
                print("Error fetching Ruby licenses:", result.stderr)
                return {}
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error: {e}")
            return {}

    def get_java_licenses(self) -> Dict[str, str]:
        """Fetch licenses for Java dependencies using license-maven-plugin."""
        try:
            result = subprocess.run(["mvn", "license:add-third-party"], capture_output=True, text=True)
            if result.returncode != 0:
                print("Error fetching Java licenses:", result.stderr)
                return {}
            # Parse the generated THIRD-PARTY.txt file
            with open("THIRD-PARTY.txt", "r") as file:
                licenses = {}
                for line in file:
                    parts = line.strip().split(":")
                    if len(parts) >= 2:
                        licenses[parts[0]] = parts[1]
                return licenses
        except Exception as e:
            print(f"Error: {e}")
            return {}

    def check_license_compatibility(self, licenses: Dict[str, str]) -> List[str]:
        """Check for incompatible licenses."""
        incompatible_licenses = []
        for package, license_info in licenses.items():
            license_name = license_info.get("License", "").upper()
            if "GPL" in license_name or "AGPL" in license_name:
                incompatible_licenses.append(f"{package}: {license_name} (Incompatible with many commercial uses)")
        return incompatible_licenses

    def generate_html_report(self, licenses: Dict[str, str], incompatible: List[str]) -> str:
        """Generate an HTML report."""
        html_content = """
        <html>
        <head><title>Open Source License Compliance Report</title></head>
        <body>
        <h1>Open Source License Compliance Report</h1>
        <h2>Dependencies and Licenses</h2>
        <table border="1">
        <tr><th>Package</th><th>License</th></tr>
        """
        for package, license_info in licenses.items():
            license_name = license_info.get("License", "")
            html_content += f"<tr><td>{package}</td><td>{license_name}</td></tr>"
        html_content += "</table>"

        if incompatible:
            html_content += "<h2>Incompatible Licenses</h2><ul>"
            for issue in incompatible:
                html_content += f"<li>{issue}</li>"
            html_content += "</ul>"
        else:
            html_content += "<h2>No Incompatible Licenses Found</h2>"

        html_content += "</body></html>"
        return html_content

    def generate_pdf_report(self, html_content: str, output_file: str):
        """Generate a PDF report from HTML content."""
        HTML(string=html_content).write_pdf(output_file)

    def run(self):
        """Run the license compliance check."""
        licenses = {}
        if self.project_type == "python":
            licenses = self.get_python_licenses()
        elif self.project_type == "node":
            licenses = self.get_node_licenses()
        elif self.project_type == "ruby":
            licenses = self.get_ruby_licenses()
        elif self.project_type == "java":
            licenses = self.get_java_licenses()
        else:
            print("Unsupported project type. Use 'python', 'node', 'ruby', or 'java'.")
            return

        if not licenses:
            print("No licenses found.")
            return

        print(f"Found {len(licenses)} dependencies.")
        incompatible = self.check_license_compatibility(licenses)
        if incompatible:
            print("\nIncompatible Licenses Found:")
            for issue in incompatible:
                print(f" - {issue}")
        else:
            print("\nNo incompatible licenses found. Your project is compliant!")

        # Generate reports
        report_type = input("Generate report in HTML or PDF? (html/pdf): ").strip().lower()
        if report_type in ["html", "pdf"]:
            html_content = self.generate_html_report(licenses, incompatible)
            if report_type == "html":
                with open("license_report.html", "w") as file:
                    file.write(html_content)
                print("HTML report generated: license_report.html")
            else:
                self.generate_pdf_report(html_content, "license_report.pdf")
                print("PDF report generated: license_report.pdf")
        else:
            print("Invalid report type. No report generated.")

if __name__ == "__main__":
    project_type = input("Enter project type (python/node/ruby/java): ").strip().lower()
    checker = LicenseChecker(project_type)
    checker.run()