import streamlit as st
from PIL import Image
import random

# Human-friendly rating labels and explanations
RATING_DETAILS = {
    "Excellent": ("🌟 Excellent", "Professional quality. All aspects look great!"),
    "Good": ("👍 Good", "Minor issues, but overall the image is very good."),
    "Fair": ("⚠️ Needs Improvement", "Some noticeable problems, consider re-editing."),
    "Poor": ("❌ Poor", "Multiple issues detected. Please review or redo this HDR image.")
}

LABELS = {
    "🌟 Excellent": "Ideal HDR result, no visible flaws.",
    "👍 Good": "Minor issue, still professionally acceptable.",
    "⚠️ Fair": "Noticeable issue, may need re-edit.",
    "❌ Poor": "Serious issue, should be rejected or redone."
}

st.set_page_config(page_title="HDR QC Review", layout="wide")
st.title("📸 HDR Quality Control Review")

st.markdown("""
Welcome! This app helps you review the quality of your HDR images using clear, visual ratings and feedback.

**How it works:**  
- We check six aspects of your image (e.g., highlight, shadow, color, brightness, contrast, clarity)
- Each is rated as 🌟 Excellent, 👍 Good, ⚠️ Fair, or ❌ Poor
- The final score combines all aspects and gives you friendly, practical feedback.
""")

st.markdown("""
**Rating Legend:**
- 🌟 **Excellent**: All quality aspects are excellent
- 👍 **Good**: Mostly good, a few minor issues
- ⚠️ **Needs Improvement**: Noticeable problems
- ❌ **Poor**: Serious issues, needs rework
""")

uploaded_files = st.file_uploader(
    "Upload HDR Images for QC",
    type=["jpg", "jpeg", "png", "tiff", "tif"],
    accept_multiple_files=True
)

def get_image_rating(image):
    # Replace this with your own image analysis logic
    # For now, randomly assign a rating for demonstration
    return random.choice(list(RATING_DETAILS.keys()))

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            image = Image.open(uploaded_file).convert("RGB")
        except Exception as e:
            st.error(f"Cannot open image: {e}")
            continue

        st.markdown(f"---\n### 🖼️ **{uploaded_file.name}**")
        cols = st.columns([1, 2])
        with cols[0]:
            st.image(image, use_container_width=True)
        with cols[1]:
            rating = get_image_rating(image)
            emoji, rating_desc = RATING_DETAILS[rating]
            st.markdown(f"## {emoji}")
            st.success(rating_desc)

            with st.expander("What does this mean?"):
                st.markdown(LABELS[emoji])

st.sidebar.header("ℹ️ QC Label Guide")
for label, desc in LABELS.items():
    st.sidebar.markdown(f"**{label}** – {desc}")
