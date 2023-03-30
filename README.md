## Installation

Make sure you have [Poetry](https://python-poetry.org/docs/#installation) installed.

Clone the repository:

```bash
git clone https://github.com/kamuda1/prompt_library_catalogue.git
cd prompt_library_catalogue
```

Install the project and its dependencies:
```bash
poetry install
```

Activate the virtual environment:
```bash
poetry shell
```

Run the project:
```bash
python main.py
```

## Usage
    1. In the application, use the "Browse" button to navigate to the directory containing the files you want to view.

    2. The left-hand side listbox will populate with the filenames (for non-CSV files) and the "prompt" column values (for CSV files).

    3. Click on an item in the list to display its content in the text area on the right-hand side of the UI.

    4. To sort the files by content similarity, click the "Order by Similarity" button. The list will update to display the files in descending order of similarity to the currently displayed text.

## License

This project is open-source and available under the MIT License.