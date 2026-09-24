import streamlit as st
from backend import predict_loan

st.set_page_config(
    page_title="LoanGuard - Loan Default Prediction",
    page_icon="🏦",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f8fafc, #eef6ff);
}

.block-container {
    max-width: 1200px;
    padding: 30px 30px 50px;
}

.title-box {
    text-align: center;
    padding: 30px 10px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #e2e8f0;
    min-height: 150px;
    box-shadow: 0 5px 20px rgba(15, 23, 42, 0.06);
}

.card h3 {
    color: #0f172a;
    margin-bottom: 8px;
}

.card p {
    color: #64748b;
    line-height: 1.6;
}

.result {
    background: white;
    padding: 30px;
    border-radius: 18px;
    text-align: center;
    margin-top: 25px;
    border: 1px solid #e2e8f0;
}

.footer {
    text-align: center;
    color: #64748b;
    padding: 30px 0 10px;
}

@media (max-width: 768px) {
    .block-container {
        padding: 15px;
    }
}
</style>
""", unsafe_allow_html=True)


st.title("🏦 LoanGuard")

st.caption("Machine Learning Loan Default Prediction System")

st.divider()


st.markdown(
    "<div class='title-box'>",
    unsafe_allow_html=True
)

st.title("Loan Default Prediction")

st.write(
    "Analyze applicant financial information and predict "
    "the possibility of loan default using a trained "
    "machine learning model."
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:
    st.markdown(
        "<div class='card'>",
        unsafe_allow_html=True
    )
    st.subheader("👤 Applicant Analysis")
    st.write(
        "Analyze applicant personal, employment "
        "and financial information."
    )
    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        "<div class='card'>",
        unsafe_allow_html=True
    )
    st.subheader("📊 Financial Evaluation")
    st.write(
        "Evaluate credit score, income, loan amount "
        "and financial ratios."
    )
    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        "<div class='card'>",
        unsafe_allow_html=True
    )
    st.subheader("🎯 ML Prediction")
    st.write(
        "Generate loan default prediction and "
        "probability using the trained model."
    )
    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


st.divider()

st.header("Loan Applicant Details")

st.write(
    "Enter the applicant information below and click "
    "**Predict Loan Default**."
)


with st.form("loan_form"):

    left, right = st.columns(2)

    with left:

        st.subheader("👤 Personal & Financial Information")

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30
        )

        income = st.number_input(
            "Annual Income",
            min_value=0.0,
            value=50000.0,
            step=1000.0
        )

        loan_amount = st.number_input(
            "Loan Amount",
            min_value=0.0,
            value=10000.0,
            step=1000.0
        )

        credit_score = st.number_input(
            "Credit Score",
            min_value=300,
            max_value=900,
            value=650
        )

        months_employed = st.number_input(
            "Months Employed",
            min_value=0,
            value=24
        )

        num_credit_lines = st.number_input(
            "Number of Credit Lines",
            min_value=0,
            value=3
        )

        interest_rate = st.number_input(
            "Interest Rate (%)",
            min_value=0.0,
            value=10.0,
            step=0.1
        )

        loan_term = st.number_input(
            "Loan Term (Months)",
            min_value=1,
            value=36
        )


    with right:

        st.subheader("📋 Loan & Applicant Profile")

        dti_ratio = st.number_input(
            "DTI Ratio",
            min_value=0.0,
            value=0.30,
            step=0.01
        )

        education = st.selectbox(
            "Education",
            [
                "Bachelor's",
                "High School",
                "Master's",
                "PhD"
            ]
        )

        employment_type = st.selectbox(
            "Employment Type",
            [
                "Full-time",
                "Part-time",
                "Self-employed",
                "Unemployed"
            ]
        )

        marital_status = st.selectbox(
            "Marital Status",
            [
                "Single",
                "Married",
                "Divorced"
            ]
        )

        has_mortgage = st.selectbox(
            "Has Mortgage",
            [
                "No",
                "Yes"
            ]
        )

        has_dependents = st.selectbox(
            "Has Dependents",
            [
                "No",
                "Yes"
            ]
        )

        loan_purpose = st.selectbox(
            "Loan Purpose",
            [
                "Auto",
                "Business",
                "Education",
                "Home",
                "Other"
            ]
        )

        has_cosigner = st.selectbox(
            "Has Co-Signer",
            [
                "No",
                "Yes"
            ]
        )


    st.write("")

    submit = st.form_submit_button(
        "🔍 Predict Loan Default",
        use_container_width=True
    )


if submit:

    input_data = {
        "Age": age,
        "Income": income,
        "LoanAmount": loan_amount,
        "CreditScore": credit_score,
        "MonthsEmployed": months_employed,
        "NumCreditLines": num_credit_lines,
        "InterestRate": interest_rate,
        "LoanTerm": loan_term,
        "DTIRatio": dti_ratio,
        "Education": education,
        "EmploymentType": employment_type,
        "MaritalStatus": marital_status,
        "HasMortgage": has_mortgage,
        "HasDependents": has_dependents,
        "LoanPurpose": loan_purpose,
        "HasCoSigner": has_cosigner
    }

    try:

        result, probability = predict_loan(input_data)

        st.divider()

        if result == "DEFAULT":

            st.error(
                "⚠️ Loan Default: YES"
            )

            st.write(
                "The model predicts a higher possibility "
                "of loan default for this application."
            )

        else:

            st.success(
                "✅ Loan Default: NO"
            )

            st.write(
                "The model predicts that the applicant "
                "may not default on the loan."
            )


        if probability is not None:

            percentage = probability * 100

            st.subheader("📊 Prediction Analysis")

            result_col1, result_col2 = st.columns(2)

            with result_col1:
                st.metric(
                    "Default Probability",
                    f"{percentage:.2f}%"
                )

            with result_col2:
                st.metric(
                    "Model Prediction",
                    result
                )

            st.progress(
                min(max(probability, 0.0), 1.0)
            )


    except Exception as error:

        st.error("❌ Prediction Error")

        st.write(
            "Please check your model and feature files."
        )

        st.exception(error)


st.divider()

st.markdown(
    "<div class='footer'>"
    "🏦 LoanGuard<br>"
    "Loan Default Prediction System<br><br>"
    "Machine Learning Project · Streamlit Frontend · Python Backend"
    "</div>",
    unsafe_allow_html=True
)