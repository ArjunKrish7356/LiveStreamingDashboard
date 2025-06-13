### 🎯 **Frontend AI Prompt: Live Streaming Analytics Dashboard (Streamlit-Compatible)**

> ✅ **Objective:** Build a modern, clean, responsive **Streamlit dashboard UI** (in Python) for a live-streaming platform. The layout must be a **2x2 grid**, covering the full screen without scroll, and use a **light theme** with **equal space for each quadrant**.

---

### 🧩 **Layout: 2x2 Grid (Full-Screen, No Scroll)**

Split the screen into four equally-sized quadrants using `st.columns` or a CSS grid-compatible layout in Streamlit:

#### 🔺 **Top Left - Donut Chart**

* Show a **red donut chart**.
* The chart should show a **single percentage value** in the center (e.g., `76%`).
* The background should be light, with good contrast and no shadow.
* Label the section as “User Retention Rate”.

> Use `plotly` or `matplotlib` with a donut style chart (remove central circle if needed).

---

#### 🔺 **Top Right - 4 Linear Horizontal Bars**

* Show four **horizontal progress bars** with:

  * Labels: `low_engagement`, `poor_ux`, `genre_fatigue`, `bad_recommendation`
  * Red colored bars with percentage values displayed next to them (e.g., `32%`)
* All bars should be vertically stacked, equally spaced, and visually clean.

> Use `st.progress` with custom HTML/CSS or `plotly` horizontal bar chart.

---

#### 🔻 **Bottom Left - Line Chart (Watch Time Over Days)**

* A **green line chart** titled “Average Watch Time”.
* X-axis: Dates (`June 1` to `June 10`)
* Y-axis: Watch time in minutes (e.g., 0 to 120)
* No interactivity needed (no tooltips or selectors)
* Should be clean, minimal, and clearly labeled.

> Use `plotly.express.line` or `altair` for a green-colored line chart with custom axis labels.

---

#### 🔻 **Bottom Right - Top Watched Movies Table**

* A simple static table titled “Top Watched Movies Today”.
* Two columns:

  * `#` (1 to 10)
  * `Movie Name` (e.g., “Movie A”, “Movie B”, ...)
* The table should be static (non-scrollable, no interactivity).
* Should fit cleanly in the quadrant with white/light background and black text.

> Use `st.table()` or `pandas.DataFrame` with `st.dataframe()` (but disable interactivity if needed).

---

### 🎨 **Styling Guidelines**

* Use a **light theme** consistent with Streamlit’s default.
* Ensure **good color contrast** (especially red and green on white).
* All components should be responsive and adapt to different screen sizes without scrollbars.
* Maintain consistent padding and spacing between components (use `st.markdown()` or spacing techniques).

---

### 🛠️ **Optional Libraries to Use**

* `plotly` or `altair` for charts
* `pandas` for table display
* `st.columns()` for quadrant layout
* Optional: `st.markdown()` + inline CSS for fine-tuned styles

