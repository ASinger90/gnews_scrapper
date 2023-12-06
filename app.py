import streamlit as st
import numpy as np
from gnews import GNews
import pandas as pd
from io import StringIO
from io import BytesIO
import io

buffer = io.BytesIO()

st.title('GNews Keyword Scrapper, Gets last 30days top 10 news by kewords')
uploaded_file = st.file_uploader("Upload keywords as xlsx", type=["xlsx"])
if uploaded_file is not None:

        # Read the Excel file into a DataFrame
    df = pd.read_excel(uploaded_file, engine='openpyxl')

        # Display the DataFrame
    st.subheader("Uploaded Keywords:")
    st.write(df)
        
    
    #df =pd.read_excel('keywords.xlsx')
    df_scrapped = pd.DataFrame(columns=['title', 'description','published date', 'url','publisher','keyword'])

    google_news = GNews()
    google_news.period = '30d'  # News from last 7 days
    google_news.max_results = 10  # number of responses across a keyword
#google_news.country = 'United States'  # News from a specific country 
    google_news.language = 'english'  # News in a specific language

    for index, row in df.iterrows():
        news = google_news.get_news(row['keyword'])
        keyword = row['keyword']
        for i in range(len(news)):
            news[i]['keyword']=keyword 

        df_news = pd.DataFrame(news)
        df_scrapped = pd.concat([df_scrapped, df_news])
    
# Download button
    #    st.subheader("Download GNews Data as Excel")
#        download_button = st.button("Download Excel")
        
#        if download_button:
            # Create a link for the user to download the DataFrame as an Excel file
 #           excel_buffer = df_scrapped.to_excel(index=False, engine='openpyxl')
  #          b64 = base64.b64encode(excel_buffer.encode()).decode()
   #         href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="gnews.xlsx">Download Excel File</a>'
    #        st.markdown(href, unsafe_allow_html=True)
    st.subheader("Download GNews Data as Excel")
    
    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        writer.close()
        processed_data = output.getvalue()
        return processed_data
    
    df_xlsx = to_excel(df_scrapped)
    st.download_button(label='📥 Download Gnews Result',
                                data=df_xlsx ,
                                file_name= 'gnews.xlsx')
        #download2 = st.download_button(
        #    label="Download data as Excel",
        #    data=buffer,
        #    file_name='gnews.xlsx',
        #    mime='application/vnd.ms-excel'
        #)

