# License Checker

The License Checker is a Python script designed to help developers check the licenses of dependencies in their projects. It supports Python, Node.js, Ruby, and Java projects. The script can generate reports in HTML or PDF format, highlighting any potentially incompatible licenses.

## Features

- **Multi-language Support**: Works with Python, Node.js, Ruby, and Java projects.
- **License Compatibility Check**: Identifies dependencies with GPL or AGPL licenses, which may be incompatible with commercial use.
- **Report Generation**: Generates detailed reports in HTML or PDF format.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/makalin/license-checker.git
   cd license-checker
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.x installed. Then, install the required Python packages:
   ```bash
   pip install weasyprint
   ```

3. **Install External Tools**:
   Depending on the project type, you may need to install additional tools:
   - **Python**: Install `pip-licenses`:
     ```bash
     pip install pip-licenses
     ```
   - **Node.js**: Install `license-checker`:
     ```bash
     npm install -g license-checker
     ```
   - **Ruby**: Install `license_finder`:
     ```bash
     gem install license_finder
     ```
   - **Java**: Ensure `mvn` (Maven) is installed and the `license-maven-plugin` is configured in your `pom.xml`.

## Usage

1. **Run the Script**:
   ```bash
   python license_checker.py
   ```

2. **Enter Project Type**:
   When prompted, enter the type of project you are checking (`python`, `node`, `ruby`, or `java`).

3. **Generate Report**:
   After the script checks the licenses, it will prompt you to generate a report in either HTML or PDF format.

## Example

```bash
$ python license_checker.py
Enter project type (python/node/ruby/java): python
Found 15 dependencies.
No incompatible licenses found. Your project is compliant!
Generate report in HTML or PDF? (html/pdf): pdf
PDF report generated: license_report.pdf
```

## Report Samples

- **HTML Report**: `license_report.html`
- **PDF Report**: `license_report.pdf`

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
