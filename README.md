# 📚 Python 3.12 Tutorial for Summer Interns

This repository serves as a **minimal working guide** to help you get started running Python and performing common tasks in our seismology workflows.  
It does **not focus on writing the most elegant or perfect code**, but rather emphasizes getting Python to work in a simple, direct way.

We use **Ipykernel (`#%%` cells in VS Code)** and **Jupyter Notebook** to demonstrate these examples.

---

## 📂 Contents

### `00_Python_features.ipynb`
- Introduces two core characteristics of Python:
  - **Dynamic typing** (variables can change types)
  - **Strong typing** (type safety is still enforced)

---

### `01_Coding_style.ipynb`
- A short introduction to recommended coding style guides:
  - **PEP8** for code formatting
  - **PEP484** for type hints

---

### `02_CRUD_with.ipynb`
- Demonstrates how to use Python’s `with` statement to read and process **unstructured text data** (where the column format may vary).

---

### `03_CRUD_pandas.ipynb`
- Shows how to use **Pandas** to handle **structured data** (like CSV), and covers some of the most powerful `DataFrame` operations.

---

### `04_moveout.py`
- An example of using **ObsPy** to process `.sac` files and plot a **moveout diagram** for a given seismic event.

---

### `05_fig_and_ax.py`
- Demonstrates the basics of creating figures and axes with **Matplotlib**, and how different plotting objects relate to each other.

---

### `06_error_handling.py`
- Shows common Python errors:
  - `ValueError`, `KeyError`, `TypeError`, `IndexError`, `RuntimeError`
  - Also demonstrates **chained exceptions** with `raise ... from ...` to help you learn how to read tracebacks.

---