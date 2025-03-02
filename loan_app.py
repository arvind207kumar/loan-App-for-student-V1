import streamlit as st


st.title("Educational Loan Approval System")


st.header("Student Details")
name = st.text_input("Full Name")
age = st.number_input("Age", min_value=16, max_value=40)


st.header("Academic Performance")
gpa = st.number_input("GPA (out of 10)", min_value=0.0, max_value=10.0, step=0.1)
test_score = st.number_input("Standardized Test Score (out of 100)", min_value=0, max_value=100)


st.header("Competitive Exams and Achievements")
iit_jee_rank = st.number_input("IIT JEE Rank (if applicable)", min_value=0, value=0)
cat_score = st.number_input("CAT Percentile (if applicable)", min_value=0.0, max_value=100.0, value=0.0)
hackathon_wins = st.number_input("Number of Hackathons Won", min_value=0, value=0)
sports_achievements = st.text_area("Sports Achievements (if any)")


st.header("Financial and Family Details")
joint_account_with_parent = st.radio("Do you have a joint account with a parent?", ["Yes", "No"])
parent_credit_score = st.number_input("Parent's Credit Score (if joint account)", min_value=300, max_value=900, value=300)
relative_guarantor = st.radio("Do you have a relative who can act as a guarantor?", ["Yes", "No"])
relative_credit_score = st.number_input("Relative's Credit Score (if guarantor)", min_value=300, max_value=900, value=300)


st.header("Institution Details")
institution_name = st.text_input("Name of the Institution")
program = st.text_input("Program of Study")


st.header("Alternative Data")
utility_payments = st.radio("Utility Bill Payment History", ["Always On Time", "Sometimes Late", "Frequently Late"])
rental_history = st.radio("Rental Payment History", ["Always On Time", "Sometimes Late", "Frequently Late"])


st.header("Personal Statement and Recommendations")
personal_statement = st.text_area("Personal Statement (Why you deserve the loan?)")
recommendation_letter = st.file_uploader("Upload Recommendation Letter (Optional)")


st.header("Document Verification")
upload_documents = st.file_uploader("Upload Required Documents (e.g., ID, Admission Letter, etc.)", accept_multiple_files=True)


def calculate_score(gpa, test_score, iit_jee_rank, cat_score, hackathon_wins, sports_achievements, joint_account_with_parent, parent_credit_score, relative_guarantor, relative_credit_score, utility_payments, rental_history, personal_statement):
    score = 0
    
    
    score += (gpa / 10.0) * 15  # GPA contributes up to 15 points
    score += (test_score / 100) * 15  # Test score contributes up to 15 points
    
    if iit_jee_rank > 0 and iit_jee_rank <= 10000:  # Top 10,000 rank in IIT JEE
        score += 10
    if cat_score >= 90:  # CAT percentile above 90
        score += 10
    if hackathon_wins > 0:
        score += min(hackathon_wins * 2, 10)  # 2 points per hackathon win, max 10 points
    if sports_achievements.strip():  # If sports achievements are mentioned
        score += 5
    
    # Financial and Family Details (Max 30 points)
    if joint_account_with_parent == "Yes" and parent_credit_score >= 760:
        score += 15
    if relative_guarantor == "Yes" and relative_credit_score >= 760:
        score += 15
    
    # Alternative Data (Max 20 points)
    if utility_payments == "Always On Time":
        score += 10
    elif utility_payments == "Sometimes Late":
        score += 5
    else:
        score += 0
    
    if rental_history == "Always On Time":
        score += 10
    elif rental_history == "Sometimes Late":
        score += 5
    else:
        score += 0
    
    # Personal Statement and Recommendations (Max 20 points)
    if personal_statement and len(personal_statement) > 100:  # Basic check for effort
        score += 20
    
    return score

# Loan Approval Logic
def approve_loan(score):
    threshold = 60  # Minimum score required for approval
    return score >= threshold

# Calculate Score and Display Result
if st.button("Submit"):
    if not upload_documents:
        st.warning("Please upload the required documents for verification.")
    else:
        score = calculate_score(gpa, test_score, iit_jee_rank, cat_score, hackathon_wins, sports_achievements, joint_account_with_parent, parent_credit_score, relative_guarantor, relative_credit_score, utility_payments, rental_history, personal_statement)
        st.write(f"Your Total Score: {score}/100")
        
        if approve_loan(score):
            st.success("Congratulations! You have the potential to get a loan.")
            st.info("Please compile and organize all your documents in a single folder for physical verification. Ensure the following documents are included:")
            st.write("- ID Proof (e.g., Aadhar Card, Passport)")
            st.write("- Admission Letter from the Institution")
            st.write("- Academic Records (e.g., Mark Sheets, Certificates)")
            st.write("- Proof of Competitive Exam Scores (if applicable)")
            st.write("- Proof of Hackathon Wins or Sports Achievements (if applicable)")
            st.write("- Utility Bill Payment History (if applicable)")
            st.write("- Rental Payment History (if applicable)")
            st.write("- Personal Statement")
            st.write("- Recommendation Letter (if available)")
            st.write("- Any other relevant documents")
            st.write("Once compiled, visit our nearest branch for document authentication and verification.")
        else:
            st.error("Sorry, your loan application has been rejected at this time.")