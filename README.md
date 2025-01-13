# Mock Trial PDF Summary

This project extracts data from University of Kentucky Mock Trial PDF ballots used in mock trial competitions. It processes scores and comments from the PDFs and saves the extracted information into an Excel file with multiple tabs for further analysis.

## Features
- Extracts quantitative scores and qualitative comments from mock trial PDF ballots.
- Processes opening statements, witness statements, and closing arguments.
- Joins extracted data with team information to identify the plaintiff and defense teams.
- Summarizes comments based on team involvement (e.g., specific team comments vs. other comments).
- Saves the data into an Excel file with separate sheets for scores, comments, team info, and summaries.

## Output
The output is saved in an Excel file named `Mock_Trial_Scores.xlsx` with the following sheets:
1. **Scores** - Contains all extracted scores along with the associated team information.
2. **Comments** - Contains all extracted comments along with the associated team information.
3. **Team Info** - Contains plaintiff and defense team names for each PDF.
4. **Russell Comments** - A summary of comments for the team named "Russell."
5. **Other Comments** - A summary of comments for all other teams.

## Usage
1. Place the PDF files in the same directory as the script.
2. Run the script using the following command:
   ```
   python main.py
   ```
3. The output Excel file (`Mock_Trial_Scores.xlsx`) will be generated in the same directory.

## File Structure
```
mock_trial_pdf_extractor/
├── main.py            # The main script to run the extraction
├── requirements.txt   # Dependencies required to run the script
├── README.md          # Project documentation
```

## Dependencies
The project requires the following Python libraries:
- `pandas`
- `pdfplumber`
- `openpyxl`

## Installation
Create a virtual environment and install the required packages using the `requirements.txt` file:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

# requirements.txt
pandas
pdfplumber
openpyxl
