import os
import pandas as pd
import pdfplumber
import re

# Function to extract text rows starting with P - or D - and the following row
def extract_raw_pairs(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages
        text = "\n".join(page.extract_text() for page in pages if page.extract_text())

    lines = text.split("\n")
    raw_pairs = []
    comments = []
    team_info = {"Filename": os.path.basename(pdf_path), "Plaintiff Team": None, "Defense Team": None}

    for i, line in enumerate(lines):
        if line.startswith("P -") or line.startswith("D -"):
            # Handle Opening and Closing Statements (only one score entry on the next line)
            if i + 1 < len(lines) and lines[i + 1].strip().isdigit():
                raw_pairs.append([line.strip(), lines[i + 1].strip()])
            # Handle pairs with two scores on the next line
            elif i + 1 < len(lines):
                raw_pairs.append([line.strip(), lines[i + 1].strip()])
        elif "Judge Comments" in line:
            # Capture comments associated with Plaintiff or Defense
            current_side = "Plaintiff" if "Plaintiff" in line else "Defense"
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == "" or "Judge Comments" in lines[j]:
                    break
                comments.append([current_side, lines[j].strip(), os.path.basename(pdf_path)])
        elif "Plaintiff Team Letter Code" in line and i + 1 < len(lines):
            team_info["Plaintiff Team"] = re.sub(r"^[A-Z0-9]+\s*", "", lines[i + 1].strip())
        elif "Defense Team Letter Code" in line and i + 1 < len(lines):
            team_info["Defense Team"] = re.sub(r"^[A-Z0-9]+\s*", "", lines[i + 1].strip())

    # Converting to DataFrames
    raw_df = pd.DataFrame(raw_pairs, columns=["Line 1", "Line 2"])
    raw_df["Filename"] = os.path.basename(pdf_path)  # Add filename column

    comments_df = pd.DataFrame(comments, columns=["Side", "Comment", "Filename"])
    team_info_df = pd.DataFrame([team_info])

    return raw_df, comments_df, team_info_df

# Function to split the raw pairs into a new structured DataFrame
def process_raw_pairs(raw_df):
    structured_data = []

    for index, row in raw_df.iterrows():
        line1 = row["Line 1"]
        line2 = row["Line 2"]
        filename = row["Filename"]

        # Splitting the scores from Line 2
        scores = line2.split()
        if len(scores) == 1:
            # Handle single score (Opening and Closing Statements)
            score = int(scores[0])
            structured_data.append([line1, score, filename])
        elif len(scores) >= 2:
            score1, score2 = int(scores[0]), int(scores[1])

            # Splitting Line 1 into two rows using regex to identify the second occurrence of P - or D -
            split_matches = list(re.finditer(r"(P -|D -)", line1))
            if len(split_matches) > 1:
                first_match = split_matches[0]
                second_match = split_matches[1]

                part1 = line1[:second_match.start()].strip()
                part2 = line1[second_match.start():].strip()

                # Adding the two new rows to the structured data
                structured_data.append([part1, score1, filename])
                structured_data.append([part2, score2, filename])

    # Converting to a structured DataFrame
    structured_df = pd.DataFrame(structured_data, columns=["Category", "Score", "Filename"])
    return structured_df

# Loop through all PDF files in the current directory
data_frames = []
comments_frames = []
team_info_frames = []

for file in os.listdir():
    if file.endswith(".pdf"):
        print(f"Processing file: {file}")
        raw_df, comments_df, team_info_df = extract_raw_pairs(file)
        structured_df = process_raw_pairs(raw_df)
        data_frames.append(structured_df)
        comments_frames.append(comments_df)
        team_info_frames.append(team_info_df)

# Combine all data into single DataFrames
combined_scores_df = pd.concat(data_frames, ignore_index=True)
combined_comments_df = pd.concat(comments_frames, ignore_index=True)
combined_team_info_df = pd.concat(team_info_frames, ignore_index=True)

# Join team info to scores and comments
combined_scores_df = combined_scores_df.merge(combined_team_info_df, on="Filename", how="left")
combined_comments_df = combined_comments_df.merge(combined_team_info_df, on="Filename", how="left")

# Debugging: Print the combined DataFrames
print("Combined Scores DataFrame:")
print(combined_scores_df.head())
print("Combined Comments DataFrame:")
print(combined_comments_df.head())
print("Combined Team Info DataFrame:")
print(combined_team_info_df.head())

# Save to Excel
with pd.ExcelWriter("Mock_Trial_Scores.xlsx") as writer:
    combined_scores_df.to_excel(writer, sheet_name="Scores", index=False)
    combined_comments_df.to_excel(writer, sheet_name="Comments", index=False)
    combined_team_info_df.to_excel(writer, sheet_name="Team Info", index=False)

print("Extraction complete. Data saved to Mock_Trial_Scores.xlsx.")
