import streamlit as st
import pandas as pd
import io

st.title("Response Time Analysis")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        # Step 1: Load CSV, skipping the first 4 rows
        df = pd.read_csv(uploaded_file, skiprows=3)

        # Step 2: Get only columns S and T (index 18 and 19)
        df = df.iloc[:, [18, 19]]
        df.columns = ['ResponseTime', 'Correct']

        # Step 3: Filter for correct responses
        df_correct = df[df['Correct'] == 1]

        # Step 4: Calculate statistics
        mean_rt = df_correct['ResponseTime'].mean()
        std_rt = df_correct['ResponseTime'].std()
        num_correct = len(df_correct)
        percent_accuracy = num_correct / 80

        # Step 5: Display results
        result_df = pd.DataFrame({
            'Mean RT': [mean_rt],
            'SD RT': [std_rt],
            'Accurate Responses': [num_correct],
            'Percent Accuracy': [percent_accuracy]
        })

        st.success("✅ Analysis complete")
        st.dataframe(result_df)

        # Step 6: Provide download option
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            result_df.to_excel(writer, index=False)
        st.download_button(
            label="Download Excel File",
            data=output.getvalue(),
            file_name='VS results.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

    except Exception as e:
        st.error(f"❌ Something went wrong: {e}")
