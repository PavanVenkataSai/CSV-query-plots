## CSV-query-plots
After downloading the folder, follow the instructions given below:

1. Create a virtual environment in VS Code (python -m venv <environment_name>)
2. To activate the virtual environment (./<environment_name>/Scripts/activate)
3. Download the required libraries from requirements.txt (pip install -r requirements.txt)
4. Create an account in ngrok and get the auth_token and paste it in <AT> variable in Improved_CSV_QUERY.ipynb 
5. Run Improved_CSV_QUERY.ipynb in Google Colab
6. Improved_CSV_QUERY.ipynb gives a ngrok link, which needs to be pasted in sql_plots.py file in <ngrok_url> variable
7. Run sql_plots.py file in the terminal (streamlit run sql_plots.py)

These are the sample questions for train.csv in the folder:

1. Display the name, age whose name is equal to 'Braund, Mr. Owen Harris'
2. Display the name, age with Pclass equal to 1 and age more than or equal to 25
3. Count the number of people whose sex is 'male'
4. What is the total fare of each pclass alone
