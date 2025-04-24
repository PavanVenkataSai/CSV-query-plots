import streamlit as st
import pandas as pd
import pandasql as psql
import matplotlib.pyplot as plt
import plotly.express as px
import requests
import seaborn as sns
import plotly.graph_objects as go

# Function for creating 1D plots
def create_1d_plots(df):
    st.title("1-Dimensional Plots")
    st.sidebar.title("1-Dimensional Plots")
    
    columns = df.columns

    for col in columns:
        data_type = df[col].dtype
        num_unique_values = df[col].nunique()

        if num_unique_values == 2:
            # Binary Data: Use pie charts
            binary_data = df[col].value_counts()
            fig = px.pie(binary_data, names=binary_data.index, title=f'{col} Distribution (Binary)')
            st.plotly_chart(fig)
            st.write(f'Binary data represents the distribution of {col}.')
        elif data_type == 'object' and num_unique_values <= 10:
            # Categorical Data: Use bar charts
            fig = px.bar(df, x=col, title=f'{col} Distribution (Categorical)')
            st.plotly_chart(fig)
            st.write(f'Categorical data represents the distribution of {col}.')
        elif data_type == 'object' and num_unique_values > 10:
            # Ordinal Data: Use bar charts
            fig = px.bar(df, x=col, title=f'{col} Distribution (Ordinal)')
            st.plotly_chart(fig)
            st.write(f'Ordinal data represents the distribution of {col}.')
        elif data_type == 'int64' or data_type == 'float64':
            # Numerical Data: Use histograms
            fig = px.histogram(df, x=col, title=f'{col} Distribution (Numerical)')
            st.plotly_chart(fig)
            st.write(f'Numerical data represents the distribution of {col}.')

# Function for creating 2D plots
def create_2d_plots(df):
    st.title("2-Dimensional Plots")
    st.sidebar.title("2-Dimensional Plots")

    columns = df.columns

    for i in range(len(columns)):
        for j in range(i+1, len(columns)):
            column1 = columns[i]
            column2 = columns[j]
            data_type1 = df[column1].dtype
            data_type2 = df[column2].dtype
            num_unique_values1 = df[column1].nunique()
            num_unique_values2 = df[column2].nunique()

            if num_unique_values1 == 2 and num_unique_values2 == 2:
                # Binary Data: Use pie chart
                binary_data = df.groupby([column1, column2]).size().unstack()
                fig = px.pie(binary_data, names=binary_data.columns, title=f'{column1} vs {column2} (Binary)')
                st.plotly_chart(fig)
            elif data_type1 == 'object' and num_unique_values1 <= 10 and data_type2 == 'object' and num_unique_values2 <= 10:
                # Categorical Data: Use stacked bar chart
                categorical_data = df.groupby([column1, column2]).size().unstack()
                fig = px.bar(categorical_data, barmode='stack', title=f'{column1} vs {column2} (Categorical)')
                st.plotly_chart(fig)
            elif (data_type1 == 'int64' or data_type1 == 'float64') and (data_type2 == 'int64' or data_type2 == 'float64'):
                # Numerical Data: Use scatter plot
                fig = px.scatter(df, x=column1, y=column2, title=f'{column1} vs {column2} (Scatter Plot)')
                st.plotly_chart(fig)
            elif data_type1 == 'object' and num_unique_values1 > 10 and data_type2 == 'int64':
                # Ordinal Data vs Numerical Data: Use lollipop chart
                ordinal_data = df.groupby(column1).agg({column2: 'mean'}).reset_index()
                ordinal_data = ordinal_data.sort_values(by=column2, ascending=False)
                fig = go.Figure(data=[go.Scatter(x=ordinal_data[column1], y=ordinal_data[column2], mode='lines+markers')])
                fig.update_layout(title_text=f'{column1} vs {column2} (Lollipop Chart)')
                st.plotly_chart(fig)
            elif (data_type1 == 'int64' or data_type1 == 'float64') and data_type2 == 'object':
                # Numerical Data vs Categorical Data: Use box plot
                fig = px.box(df, x=column2, y=column1, title=f'{column1} vs {column2} (Box Plot)')
                st.plotly_chart(fig)

# Function for uploading a CSV file and asking questions
def upload_and_ask_question():
    st.sidebar.title("Uploading and Asking Question")
    st.title("Upload a CSV File and Ask a Question")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        st.success("File uploaded successfully!")

        # Load the uploaded CSV file into a Pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # Display the first few rows of the DataFrame
        st.dataframe(df.head())

        # Ask a question
        user_question = st.text_input("Ask a question")

        if user_question:
            # Create a placeholder for the loading message
            loading_message = st.empty()
            loading_message.text("Loading...")

            # Send the CSV file and user_question to the Flask API
            ngrok_url = "https://846c-34-66-107-138.ngrok-free.app/"
            upload_url = ngrok_url +"generate-sql"  # Update with your API endpoint URL
            data = {'question': user_question, 'csv_data': df.to_csv(index=False)}
            response = requests.post(upload_url, json=data)

            if response.status_code == 200:
                result = response.json()
                generated_sql = result.get('sql_query')
                loading_message.empty()  # Clear the loading message

                st.success(f"Generated SQL Query: {generated_sql}")

                sql_query = str(generated_sql)
                # Run an SQL query to filter the data
                result_df = psql.sqldf(sql_query, locals())

                # Store the result in st.session_state
                st.session_state.result = result_df

                st.table(result_df)
            else:
                loading_message.empty()  # Clear the loading message
                st.error("Error generating SQL query.")


# Main Streamlit app
def main():
    st.sidebar.title("Navigation")
    selected_option = st.sidebar.selectbox("Select an option:", ["Uploading and Asking Question", "Analytics Dashboard"])

    if selected_option == "Uploading and Asking Question":
        upload_and_ask_question()
    elif selected_option == "Analytics Dashboard":
        display_option = st.sidebar.radio("Select what to display:", ["Data Header", "Data Summary", "Dashboard"])
        if display_option == "Data Header":
            if 'result' in st.session_state:
                result = st.session_state.result
                # Display header
                st.header('Header of Dataframe')
                st.dataframe(result.head())
        elif display_option == "Data Summary":
            if 'result' in st.session_state:
                result = st.session_state.result
                # Display data summary
                st.header('Statistics of Dataframe')
                st.write(result.describe())
        elif display_option == "Dashboard":
            if 'result' in st.session_state:
                result = st.session_state.result
                dashboard_option = st.sidebar.radio("Select what to display in Dashboard:", ["1-Dimensional plots", "2-Dimensional plots"])
                if dashboard_option == "1-Dimensional plots":
                    create_1d_plots(result)
                elif dashboard_option == "2-Dimensional plots":
                    create_2d_plots(result)

if __name__ == "__main__":
    main()