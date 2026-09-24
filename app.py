import streamlit as st
from backend import predict_loan


# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="LoanGuard | Smart Loan Default Prediction",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==================================================
# HELPERS
# ==================================================

def html(markup: str) -> None:
    st.markdown(markup, unsafe_allow_html=True)


def feature_card(icon: str, title: str, text: str) -> str:
    return (
        '<div class="lg-card">'
        f'<div class="lg-icon">{icon}</div>'
        f'<h3>{title}</h3>'
        f'<p>{text}</p>'
        "</div>"
    )


def step_card(num: str, title: str, text: str) -> str:
    return (
        '<div class="lg-card lg-step">'
        f'<div class="lg-step-num">{num}</div>'
        f'<h3>{title}</h3>'
        f'<p>{text}</p>'
        "</div>"
    )


# ==================================================
# CSS
# ==================================================

html("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: Inter, system-ui, -apple-system, Segoe UI, sans-serif;
    }

    .stApp {
        background: #f5f8fc;
        color: #0f172a;
        overflow-x: hidden;
    }

    .block-container {
        max-width: 1160px;
        padding-top: 0.6rem;
        padding-bottom: 1.2rem;
        padding-left: 1.1rem;
        padding-right: 1.1rem;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    #MainMenu,
    footer,
    .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }

    .stApp > header {
        display: none;
    }

    /* Navbar */
    .lg-nav {
        background: #0b1f3a;
        border-radius: 16px;
        padding: 14px 22px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        box-shadow: 0 10px 28px rgba(11, 31, 58, 0.18);
        margin-bottom: 18px;
        flex-wrap: wrap;
    }

    .lg-brand {
        color: #ffffff;
        font-weight: 800;
        font-size: 1.25rem;
        letter-spacing: 0.02em;
        display: flex;
        align-items: center;
        gap: 8px;
        white-space: nowrap;
    }

    .lg-brand .accent {
        color: #7dd3fc;
    }

    .lg-links {
        display: flex;
        flex-wrap: wrap;
        gap: 8px 16px;
    }

    .lg-links a {
        color: #dbeafe !important;
        text-decoration: none !important;
        font-size: 0.92rem;
        font-weight: 600;
        padding: 6px 4px;
    }

    .lg-links a:hover {
        color: #ffffff !important;
    }

    /* Hero */
    .lg-hero {
        background: linear-gradient(135deg, #0b1f3a 0%, #163a6b 58%, #1d4ed8 100%);
        border-radius: 20px;
        padding: 28px 30px;
        color: #ffffff;
        min-height: 280px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.18);
    }

    .lg-kicker {
        color: #93c5fd;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .lg-hero h1 {
        font-size: clamp(1.6rem, 3.4vw, 2.5rem);
        line-height: 1.15;
        margin: 0 0 12px 0;
        font-weight: 800;
        color: #ffffff;
    }

    .lg-hero p {
        font-size: clamp(0.95rem, 1.6vw, 1.08rem);
        color: #dbeafe;
        margin: 0 0 20px 0;
        max-width: 520px;
        line-height: 1.55;
    }

    .lg-cta {
        display: inline-block;
        background: #ffffff;
        color: #0b1f3a !important;
        text-decoration: none !important;
        font-weight: 800;
        border-radius: 12px;
        padding: 12px 20px;
        font-size: 0.98rem;
        min-height: 44px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.16);
    }

    .lg-cta:hover {
        background: #e0f2fe;
    }

    .lg-hero-img {
        width: 100%;
        border-radius: 20px;
        object-fit: cover;
        min-height: 280px;
        max-height: 340px;
        box-shadow: 0 16px 40px rgba(15, 23, 42, 0.16);
    }

    /* Section titles */
    .lg-section-title {
        text-align: center;
        margin: 8px 0 6px 0;
    }

    .lg-section-title h2 {
        color: #0b1f3a !important;
        font-size: clamp(1.35rem, 2.4vw, 1.85rem) !important;
        font-weight: 800 !important;
        margin-bottom: 6px;
    }

    .lg-section-title p {
        color: #64748b;
        font-size: 0.98rem;
        margin: 0 auto 8px auto;
        max-width: 640px;
    }

    /* Cards */
    .lg-card {
        background: #ffffff;
        border: 1px solid #e6eef8;
        border-radius: 16px;
        padding: 20px 18px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .lg-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 28px rgba(15, 23, 42, 0.08);
    }

    .lg-icon {
        font-size: 1.5rem;
        margin-bottom: 8px;
    }

    .lg-card h3 {
        color: #0f172a !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        margin: 0 0 8px 0 !important;
    }

    .lg-card p {
        color: #64748b;
        font-size: 0.92rem;
        line-height: 1.5;
        margin: 0;
    }

    .lg-step-num {
        color: #1d4ed8;
        font-weight: 800;
        font-size: 0.85rem;
        letter-spacing: 0.08em;
        margin-bottom: 8px;
    }

    .lg-form-head {
        background: #ffffff;
        border: 1px solid #e6eef8;
        border-radius: 16px;
        padding: 18px 20px 8px 20px;
        margin-bottom: 8px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
    }

    .lg-form-head h2 {
        color: #0b1f3a !important;
        font-size: 1.4rem !important;
        margin: 0 0 6px 0 !important;
    }

    .lg-form-head p {
        color: #64748b;
        margin: 0 0 8px 0;
        font-size: 0.95rem;
    }

    .lg-group-title {
        background: #0b1f3a;
        color: #ffffff;
        border-radius: 12px;
        padding: 10px 14px;
        font-weight: 700;
        font-size: 0.95rem;
        margin: 6px 0 10px 0;
    }

    label {
        font-weight: 600 !important;
        color: #334155 !important;
    }

    div[data-baseweb="input"],
    div[data-baseweb="select"],
    input {
        border-radius: 10px !important;
    }

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] button {
        width: 100%;
        min-height: 54px;
        border-radius: 14px;
        border: none;
        background: linear-gradient(135deg, #1d4ed8, #0b1f3a);
        color: #ffffff;
        font-size: 1.05rem;
        font-weight: 800;
        letter-spacing: 0.01em;
        transition: 0.2s ease;
        margin-top: 8px;
    }

    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(29, 78, 216, 0.28);
    }

    /* Result cards */
    .lg-result {
        border-radius: 16px;
        padding: 22px 22px 16px 22px;
        margin: 6px 0 12px 0;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    }

    .lg-result.ok {
        background: linear-gradient(180deg, #ecfdf5 0%, #ffffff 70%);
        border: 1px solid #a7f3d0;
    }

    .lg-result.warn {
        background: linear-gradient(180deg, #fff7ed 0%, #ffffff 70%);
        border: 1px solid #fed7aa;
    }

    .lg-badge {
        display: inline-block;
        font-size: 0.75rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        border-radius: 999px;
        padding: 5px 10px;
        margin-bottom: 10px;
    }

    .ok .lg-badge {
        background: #d1fae5;
        color: #065f46;
    }

    .warn .lg-badge {
        background: #ffedd5;
        color: #9a3412;
    }

    .lg-result h2 {
        margin: 0 0 8px 0 !important;
        font-size: 1.55rem !important;
        font-weight: 800 !important;
    }

    .ok h2 { color: #065f46 !important; }
    .warn h2 { color: #9a3412 !important; }

    .lg-result p {
        color: #475569;
        margin: 0 0 12px 0;
    }

    .lg-metrics {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }

    .lg-metric {
        background: #ffffff;
        border-radius: 12px;
        padding: 12px;
        border: 1px solid #e2e8f0;
    }

    .lg-metric span {
        display: block;
        color: #64748b;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 4px;
    }

    .lg-metric strong {
        font-size: 1.05rem;
        color: #0f172a;
    }

    .lg-about {
        background: #ffffff;
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid #e6eef8;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
    }

    .lg-about-copy {
        padding: 22px 22px 8px 22px;
    }

    .lg-about-copy h2 {
        color: #0b1f3a !important;
        margin-top: 0 !important;
    }

    .lg-about-copy p {
        color: #475569;
        line-height: 1.65;
        font-size: 0.98rem;
    }

    .lg-about img {
        width: 100%;
        height: 100%;
        min-height: 220px;
        object-fit: cover;
        display: block;
    }

    .lg-footer {
        background: #0b1f3a;
        color: #dbeafe;
        border-radius: 16px;
        padding: 22px 20px;
        text-align: center;
        margin-top: 8px;
    }

    .lg-footer strong {
        color: #ffffff;
        font-size: 1.1rem;
        display: block;
        margin-bottom: 6px;
    }

    .lg-footer p {
        margin: 4px 0;
        font-size: 0.9rem;
        color: #bfdbfe;
    }

    [data-testid="stVerticalBlock"] > [style*="flex-direction: column"] {
        gap: 0.55rem;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.7rem;
            padding-right: 0.7rem;
        }

        .lg-nav {
            padding: 12px 14px;
        }

        .lg-links a {
            font-size: 0.82rem;
        }

        .lg-hero {
            padding: 22px 18px;
            min-height: auto;
        }

        .lg-hero-img,
        .lg-about img {
            min-height: 180px;
            max-height: 220px;
        }

        .lg-metrics {
            grid-template-columns: 1fr;
        }

        div.stButton > button,
        div[data-testid="stFormSubmitButton"] button {
            min-height: 52px;
            font-size: 1rem;
        }
    }
</style>
""")


# ==================================================
# NAVBAR
# ==================================================

html("""
<div class="lg-nav" id="home">
    <div class="lg-brand"><span>🏦</span><span>Loan<span class="accent">Guard</span></span></div>
    <div class="lg-links">
        <a href="#home">Home</a>
        <a href="#loan-analysis">Loan Analysis</a>
        <a href="#how-it-works">How It Works</a>
        <a href="#about">About</a>
    </div>
</div>
""")


# ==================================================
# HERO
# ==================================================

hero_left, hero_right = st.columns([1.15, 0.85], gap="medium")

with hero_left:
    html("""
    <div class="lg-hero">
        <div class="lg-kicker">Fintech Risk Intelligence</div>
        <h1>Smart Loan Default Prediction</h1>
        <p>Evaluate loan risk with machine learning and make data-driven lending decisions.</p>
        <a class="lg-cta" href="#loan-analysis">Start Loan Analysis</a>
    </div>
    """)

with hero_right:
    html("""
    <img class="lg-hero-img"
         src="https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=900&q=70"
         alt="Financial analysis and loan documents">
    """)


st.write("")


# ==================================================
# FEATURES
# ==================================================

html("""
<div class="lg-section-title">
    <h2>Built for clearer lending decisions</h2>
    <p>LoanGuard presents applicant, credit, and loan signals in a structured way so risk can be reviewed quickly.</p>
</div>
""")

f1, f2, f3, f4 = st.columns(4, gap="small")

with f1:
    html(feature_card(
        "📈",
        "Credit Score Analysis",
        "Review credit standing alongside repayment capacity before a lending decision is made."
    ))

with f2:
    html(feature_card(
        "💼",
        "Financial Evaluation",
        "Income, DTI, credit lines, and loan terms are organized into a single applicant profile."
    ))

with f3:
    html(feature_card(
        "🛡️",
        "Risk Prediction",
        "Receive a default / no-default outcome with an estimated default probability."
    ))

with f4:
    html(feature_card(
        "🤖",
        "Machine Learning",
        "A trained scikit-learn model scores the same 16 features used during project development."
    ))


st.write("")


# ==================================================
# LOAN PREDICTION FORM
# ==================================================

html('<div id="loan-analysis"></div>')

html("""
<div class="lg-form-head">
    <h2>Loan Analysis</h2>
    <p>Complete the applicant profile below. All fields map to the existing trained model features.</p>
</div>
""")

with st.form("loan_prediction_form"):

    personal_col, financial_col = st.columns(2, gap="large")

    with personal_col:
        html('<div class="lg-group-title">👤 Personal Information</div>')

        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=30
        )

        education = st.selectbox(
            "Education",
            [
                "High School",
                "Bachelor's",
                "Master's",
                "PhD"
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

        has_dependents = st.selectbox(
            "Has Dependents",
            [
                "Yes",
                "No"
            ]
        )

    with financial_col:
        html('<div class="lg-group-title">💳 Financial Information</div>')

        income = st.number_input(
            "Annual Income",
            min_value=0.0,
            value=50000.0
        )

        credit_score = st.number_input(
            "Credit Score",
            min_value=300,
            max_value=900,
            value=650
        )

        dti_ratio = st.number_input(
            "DTI Ratio",
            min_value=0.0,
            value=0.30,
            step=0.01
        )

        num_credit_lines = st.number_input(
            "Number of Credit Lines",
            min_value=0,
            value=3
        )

    loan_col, employment_col = st.columns(2, gap="large")

    with loan_col:
        html('<div class="lg-group-title">🏦 Loan Information</div>')

        loan_amount = st.number_input(
            "Loan Amount",
            min_value=0.0,
            value=10000.0
        )

        interest_rate = st.number_input(
            "Interest Rate",
            min_value=0.0,
            value=10.0,
            step=0.1
        )

        loan_term = st.number_input(
            "Loan Term",
            min_value=1,
            value=36
        )

        loan_purpose = st.selectbox(
            "Loan Purpose",
            [
                "Home",
                "Auto",
                "Education",
                "Business",
                "Other"
            ]
        )

    with employment_col:
        html('<div class="lg-group-title">📎 Employment Information</div>')

        months_employed = st.number_input(
            "Months Employed",
            min_value=0,
            value=24
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

        has_mortgage = st.selectbox(
            "Has Mortgage",
            [
                "Yes",
                "No"
            ]
        )

        has_cosigner = st.selectbox(
            "Has Co-Signer",
            [
                "Yes",
                "No"
            ]
        )

    st.write("")

    submitted = st.form_submit_button(
        "🔍 Analyze Loan Risk"
    )


# ==================================================
# BACKEND + PREDICTION
# ==================================================

if submitted:

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

        percentage = None
        if probability is not None:
            percentage = probability * 100
            probability_label = f"{percentage:.2f}%"
        else:
            probability_label = "Not available"

        if result == "DEFAULT":

            html(f"""
            <div class="lg-result warn">
                <div class="lg-badge">High Risk</div>
                <h2>Loan Default: YES</h2>
                <p>The applicant is predicted to default on the loan.</p>
                <div class="lg-metrics">
                    <div class="lg-metric">
                        <span>Default Probability</span>
                        <strong>{probability_label}</strong>
                    </div>
                    <div class="lg-metric">
                        <span>Model Prediction</span>
                        <strong>{result}</strong>
                    </div>
                </div>
            </div>
            """)

        else:

            html(f"""
            <div class="lg-result ok">
                <div class="lg-badge">Low Risk</div>
                <h2>Loan Default: NO</h2>
                <p>The applicant is predicted to repay the loan.</p>
                <div class="lg-metrics">
                    <div class="lg-metric">
                        <span>Default Probability</span>
                        <strong>{probability_label}</strong>
                    </div>
                    <div class="lg-metric">
                        <span>Model Prediction</span>
                        <strong>{result}</strong>
                    </div>
                </div>
            </div>
            """)

        if probability is not None:

            st.subheader("📊 Prediction Probability")

            st.metric(
                "Estimated Default Probability",
                f"{percentage:.2f}%"
            )

            st.progress(
                min(
                    max(probability, 0.0),
                    1.0
                )
            )

    except Exception as error:

        st.error(
            "❌ Prediction Error"
        )

        st.write(
            "Please check the model and feature names."
        )

        st.exception(error)


st.write("")


# ==================================================
# HOW IT WORKS
# ==================================================

html('<div id="how-it-works"></div>')

html("""
<div class="lg-section-title">
    <h2>How It Works</h2>
    <p>Four simple steps from applicant details to a readable risk result.</p>
</div>
""")

s1, s2, s3, s4 = st.columns(4, gap="small")

with s1:
    html(step_card(
        "01",
        "Enter Applicant Details",
        "Provide personal, financial, loan, and employment information using the structured form."
    ))

with s2:
    html(step_card(
        "02",
        "Machine Learning Analysis",
        "The existing trained model scores the applicant using the original project features."
    ))

with s3:
    html(step_card(
        "03",
        "Risk Prediction",
        "The model returns a default or no-default outcome together with a probability score."
    ))

with s4:
    html(step_card(
        "04",
        "View Result",
        "Review the highlighted result card, default probability, and progress indicator."
    ))


st.write("")


# ==================================================
# ABOUT
# ==================================================

html('<div id="about"></div>')

about_copy, about_image = st.columns([1.15, 0.85], gap="medium")

with about_copy:
    html("""
    <div class="lg-about">
        <div class="lg-about-copy">
            <h2>About LoanGuard</h2>
            <p>LoanGuard is a machine-learning based loan default prediction system that analyzes applicant and loan-related information and predicts the possibility of loan default.</p>
            <p>It is designed as an academic demonstration of applied machine learning. Results are intended for learning and presentation, not as guaranteed outcomes or as advice for real-world financial decisions.</p>
        </div>
    </div>
    """)

with about_image:
    html("""
    <div class="lg-about">
        <img src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=900&q=70"
             alt="Credit and financial planning workspace">
    </div>
    """)


st.write("")


# Image row: banking / credit / analysis
img1, img2, img3 = st.columns(3, gap="small")

with img1:
    html("""
    <img class="lg-hero-img"
         src="https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=700&q=70"
         alt="Secure credit card and banking">
    """)

with img2:
    html("""
    <img class="lg-hero-img"
         src="https://images.unsplash.com/photo-1553729459-efe14ef6055d?auto=format&fit=crop&w=700&q=70"
         alt="Loan and savings planning">
    """)

with img3:
    html("""
    <img class="lg-hero-img"
         src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=700&q=70"
         alt="Machine learning financial analytics dashboard">
    """)


st.write("")


# ==================================================
# FOOTER
# ==================================================

html("""
<div class="lg-footer">
    <strong>LoanGuard</strong>
    <p>Loan Default Prediction System</p>
    <p>Machine Learning Project</p>
    <p>Python • Scikit-learn • Streamlit</p>
</div>
""")
