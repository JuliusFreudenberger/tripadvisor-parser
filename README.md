# TripAdvisor Parser
Get reviews from attractions in TripAdvisor.
Requests all reviews in the currently selected language in TripAdvisor and exports them in a csv file.
To mitigate commas and quotation marks in the review texts, the columns in the csv are separated with `^`.

## Usage
1. Create a file in the PWD named `urls.txt`. Place one URL per line.
2. Start the program. You do not need to pass parameters.
3. Find the csv files in the `export/` directory.
