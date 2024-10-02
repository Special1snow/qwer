
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate similarity between user skills and job skills
def calculate_similarity(user_skills, job_skills):
    return np.linalg.norm(np.array(user_skills) - np.array(job_skills))

# Function to load and process the uploaded data
def load_data():
    uploaded_file = st.file_uploader("Upload your Excel file for HR solution", type=["xlsx"])
    if uploaded_file is not None:
        xls = pd.ExcelFile(uploaded_file)
        skillset_df = pd.read_excel(xls, sheet_name='직무별SkillSet')
        self_review_df = pd.read_excel(xls, sheet_name='Self Review')
        return skillset_df, self_review_df
    return None, None

# Main function to run the Streamlit app
def main():
    st.title("HR Skillset Matching Tool with Sunburst Chart")

    # Load data
    skillset_df, self_review_df = load_data()
    
    if skillset_df is not None and self_review_df is not None:
        st.success("Data loaded successfully!")
        
        # Align skills between "직무별SkillSet" and "Self Review"
        matching_skills = skillset_df['General Skill'].isin(self_review_df['General Skill'])
        filtered_skillset_df = skillset_df[matching_skills]
        filtered_self_review_df = self_review_df[self_review_df['General Skill'].isin(filtered_skillset_df['General Skill'])]
        
        # Extract relevant data
        job_titles = filtered_skillset_df.columns[3:]
        filtered_user_skill_scores = filtered_self_review_df['환산점수'].tolist()
        
        # Find the most suitable job for the user
        best_match = None
        best_score = float('inf')
        
        for job in job_titles:
            job_skill_scores = filtered_skillset_df[job].tolist()
            similarity_score = calculate_similarity(filtered_user_skill_scores, job_skill_scores)
            
            if similarity_score < best_score:
                best_score = similarity_score
                best_match = job

        st.write(f"The most suitable job for the user is: **{best_match}**")

        # Generate Sunburst Chart
        matched_job_skills = filtered_skillset_df[['General Skill', best_match]]
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.bar(
            range(len(matched_job_skills)),
            matched_job_skills[best_match],
            tick_label=matched_job_skills['General Skill']
        )
        ax.set_title(f"Sunburst Chart - Best Matched Job: {best_match}")
        st.pyplot(fig)

    else:
        st.warning("Please upload an Excel file to proceed.")

if __name__ == "__main__":
    main()
