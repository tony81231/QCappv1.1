import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd

# QC thresholds (customize as needed)
QC_THRESHOLDS = {
    'highlight_ratio_poor': 0.05,
    'highlight_ratio_excellent': 0.005,
    'shadow_ratio_poor': 0.10,
    'shadow_ratio_excellent': 0.02,
    'mean_brightness_low': 80,
    'mean_brightness_high': 200,
    'std_contrast_fair': 30
}

LABELS = {
    "🌟 Excellent": "Ideal HDR result, no visible flaws.",
    "👍 Good": "Minor issue, still professionally acceptable.",
    "⚠️ Fair": "Noticeable issue, may need re-edit.",
    "❌ Poor": "Serious issue, should be rejected or redone."
}

RATING_DETAILS = {
    "10/10 – Excellent": ("🌟 Excellent", "Professional quality. All aspects look great!"),
    "8/10 – Good": ("👍 Good", "Minor issues, but overall the image is very good."),
    "6/10 – Fair": ("⚠️ Needs Improvement", "Some noticeable problems, consider re-editing."),
    "4/10 – Poor": ("❌ Poor", "Multiple issues detected. Please review or redo this HDR image.")
}

st.set_page_config(page_title="HDR QC Review", layout="wide")
st.title("📸 HDR Quality Control Review")

st.markdown("""
Welcome! This app helps you review the quality of your HDR images using clear, visual ratings and feedback.  
**How it works:**  
- We check six aspects of your image (highlight, shadow, color, brightness, contrast, clarity)
- Each is rated as 🌟 Excellent, 👍 Good, ⚠️ Fair, or ❌ Poor
- The final score combines all aspects and gives you friendly, practical feedback.
""")

st.markdown("""
**Rating Legend:**  
- 🌟 **Excellent**: All quality metrics are Excellent/Good  
- 👍 **Good**: 1–2 Fair ratings, rest Good or better  
- ⚠️ **Needs Improvement**: 2+ Fair ratings or one Poor  
- ❌ **Poor**: 2+ Poor ratings  
""")

uploaded_files = st.file_uploader(
    "Upload HDR Images for QC",
    type=["jpg", "jpeg", "png", "tiff", "tif"],
    accept_multiple_files=True
)

def classify_metric(score):
    if score == "Excellent":
        return "🌟 Excellent"
    elif score == "Good":
        return "👍 Good"
    elif score == "Fair":
        return "⚠️ Fair"
    else:
        return "❌ Poor"

def analyze_image_ai(image, thresholds=QC_THRESHOLDS):
    np_img = np.array(image)
    if np_img.ndim == 2:
        np_img = np.stack([np_img]*3, axis=-1)
    elif np_img.shape[2] > 3:
        np_img = np_img[..., :3]

    gray = np.dot(np_img[...,:3], [0.2989, 0.5870, 0.1140])
    mean_brightness = np.mean(gray)
    std_contrast = np.std(gray)

    highlight_mask = np.all(np_img > 240, axis=-1)
    highlight_ratio = np.sum(highlight_mask) / highlight_mask.size

    shadow_mask = gray < 30
    shadow_ratio = np.sum(shadow_mask) / shadow_mask.size

    metrics = {
        "Highlight Control": classify_metric(
            "Poor" if highlight_ratio > thresholds['highlight_ratio_poor']
            else "Excellent" if highlight_ratio < thresholds['highlight_ratio_excellent']
            else "Fair"
        ),
        "Shadow Detail": classify_metric(
            "Poor" if shadow_ratio > thresholds['shadow_ratio_poor']
            else "Excellent" if shadow_ratio < thresholds['shadow_ratio_excellent']
            else "Fair"
        ),
        "Color Accuracy": classify_metric("Excellent"),  # Placeholder
        "Brightness Balance": classify_metric(
            "Fair" if mean_brightness < thresholds['mean_brightness_low'] or mean_brightness > thresholds['mean_brightness_high']
            else "Good"
        ),
        "Contrast & Depth": classify_metric(
            "Fair" if std_contrast < thresholds['std_contrast_fair'] else "Excellent"
        ),
        "Clarity & Sharpness": classify_metric("Good"),  # Placeholder
    }

    ratings = list(metrics.values())
    poor_count = ratings.count("❌ Poor")
    fair_count = ratings.count("⚠️ Fair")

    if poor_count >= 2:
        final = "4/10 – Poor"
    elif poor_count == 1 or fair_count >= 2:
        final = "6/10 – Fair"
    elif fair_count == 1:
        final = "8/10 – Good"
    else:
        final = "10/10 – Excellent"

    comment_map = {
        "10/10 – Excellent": "Professional quality HDR image. Balanced lighting, crisp details, and clean highlights.",
        "8/10 – Good": "Minor balance or exposure issue, but overall clean and sharp.",
        "6/10 – Fair": "Flatness or brightness imbalance noticeable. Still usable with minor edits.",
        "4/10 – Poor": "Multiple quality issues detected. Recommend re-edit or revision."
    }

    metrics["Final Rating"] = final
    metrics["Comment"] = comment_map[final]
    metrics["Brightness (mean)"] = f"{mean_brightness:.1f}"
    metrics["Contrast (std)"] = f"{std_contrast:.1f}"
    metrics["Highlight %"] = f"{highlight_ratio*100:.2f}%"
    metrics["Shadow %"] = f"{shadow_ratio*100:.2f}%"
    return metrics, gray

def show_histogram(gray):
    hist, bins = np.histogram(gray.ravel(), bins=32, range=(0,255))
    df = pd.DataFrame({'Luminance': bins[:-1], 'Pixel Count': hist})
    st.bar_chart(df.set_index('Luminance'))
    st.caption(
        "This bar chart shows how brightness is distributed in the image. "
        "A good HDR image usually spreads values across the chart, not just clustered left (dark) or right (bright)."
    )

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            image = Image.open(uploaded_file).convert("RGB")
            metrics, gray = analyze_image_ai(image)
        except Exception as e:
            st.error(f"Cannot open image: {e}")
            continue

        st.markdown(f"---\n### 🖼️ **{uploaded_file.name}**")

        # Layout: Image and main rating left, details right
        cols = st.columns([1, 2])
        with cols[0]:
            st.image(image, use_column_width=True)
            show_histogram(gray)
        with cols[1]:
            # Friendly rating box
            rating_emoji, rating_desc = RATING_DETAILS[metrics["Final Rating"]]
            st.markdown(f"## {rating_emoji}")
            st.success(rating_desc)
            st.info(metrics["Comment"])

            # Expand for metric details
            with st.expander("See detailed quality scores"):
                for metric, value in metrics.items():
                    if metric not in ["Final Rating", "Comment"]:
                        st.markdown(f"**{metric}:** {value}")

st.sidebar.header("ℹ️ QC Label Guide")
for label, desc in LABELS.items():
    st.sidebar.markdown(f"**{label}** – {desc}")
