# HDR QC App (Streamlit, PIL version)

This app lets you upload images, performs automated HDR QC, shows a luminance histogram, and gives a rating and comment for each image.

## 🚀 Usage (Local or Streamlit Cloud)

1. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```
2. **Run the app:**
    ```
    streamlit run app.py
    ```
3. **Or deploy directly to [Streamlit Community Cloud](https://share.streamlit.io/)**

## 📝 Notes

- No OpenCV or system dependencies! Works on Streamlit Cloud and most Python hosts.
- Supported formats: JPEG, PNG, TIFF.
- Ratings are not saved.
- All QC logic is customizable at the top of `app.py`.