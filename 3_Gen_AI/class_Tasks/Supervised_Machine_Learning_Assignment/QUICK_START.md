# 🚀 Quick Start Guide - Customer Purchase Prediction Assignment

## ⚡ Fast Track Instructions

### Step 1: Verify Files
Check that you have these files in `3_Gen_AI/class_Tasks/`:
- ✅ `Assignment_Supervised_Machine_Learning.ipynb`
- ✅ `data.xlsx`
- ✅ `README.md`

### Step 2: Install Required Packages
Run this in terminal:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn openpyxl
```

### Step 3: Open and Run Notebook
1. Open `Assignment_Supervised_Machine_Learning.ipynb` in VS Code
2. Select Python kernel
3. Click **"Run All"** (Ctrl + Shift + P → "Run All")

### Step 4: Wait for Completion
⏱️ Expected time: 2-5 minutes
- Data loading: instant
- EDA visualizations: ~30 seconds
- Model training: ~1 minute
- Hyperparameter tuning: ~2-3 minutes (this is the longest part)

### Step 5: Review Results
After completion, you'll have:
- ✅ All visualizations displayed
- ✅ Model performance metrics printed
- ✅ Models saved in `models/` folder
- ✅ Final comparison table

---

## 📊 What to Expect

### Notebook Sections (43 cells total)
1. **Cells 1-2**: Title and imports → ~10 seconds
2. **Cells 3-8**: Data loading and understanding → ~30 seconds
3. **Cells 9-16**: EDA visualizations → ~1 minute
4. **Cells 17-21**: Data preprocessing → ~10 seconds
5. **Cells 22-28**: Model training (3 models) → ~30 seconds
6. **Cells 29-32**: Confusion matrices & ROC curves → ~20 seconds
7. **Cells 33-35**: Hyperparameter tuning → ~2-3 minutes ⚠️ (longest)
8. **Cells 36-37**: Feature importance → ~10 seconds
9. **Cells 38-40**: Final comparison → ~10 seconds
10. **Cells 41-42**: Model saving → ~5 seconds
11. **Cell 43**: Summary (markdown)

---

## 🎯 Key Results to Look For

### 1. Dataset Summary
- 100 samples, 10 features
- 51% purchased, 49% not purchased
- No missing values

### 2. EDA Insights
- Age group analysis
- Salary vs purchase correlation
- Device type conversion rates
- Feature correlations

### 3. Model Performance
You'll get a comparison table showing:
- Logistic Regression
- Decision Tree
- Random Forest
- Random Forest (Tuned) ← **Best Model**

### 4. Saved Models (in `models/` folder)
- `best_model_random_forest.pkl`
- `scaler.pkl`
- `logistic_regression.pkl`
- `decision_tree.pkl`
- `random_forest.pkl`

---

## ⚠️ Troubleshooting

### Issue: Import Error
**Solution:** Install missing packages
```bash
pip install package_name
```

### Issue: File Not Found (data.xlsx)
**Solution:** Ensure `data.xlsx` is in the same folder as the notebook

### Issue: GridSearchCV Taking Too Long
**Solution:** This is normal! GridSearchCV explores many parameter combinations.
- Expected time: 2-3 minutes on most machines
- To speed up: Reduce parameter grid size in the notebook (not recommended)

### Issue: Kernel Not Starting
**Solution:** 
1. Restart VS Code
2. Select Python kernel manually
3. Ensure Python 3.x is installed

---

## 📈 Expected Output Preview

After running, you'll see:

### Visualizations (12 plots)
1. Target variable distribution
2. Numerical features histograms (5 plots)
3. Categorical features count plots (3 plots)
4. Age group analysis (2 plots)
5. Salary analysis (2 plots)
6. Device type analysis (2 plots)
7. Correlation heatmap
8. Confusion matrices (3 models)
9. ROC curves (all models)
10. Feature importance (2 models)
11. Model comparison charts (4 metrics)

### Performance Metrics
For each model you'll see:
- Accuracy score
- Precision, Recall, F1-Score
- ROC-AUC score
- Classification report
- Confusion matrix

---

## ✅ Verification Checklist

After running the notebook, verify:

- [ ] All cells executed without errors
- [ ] 12+ visualizations displayed
- [ ] Model comparison table shows 4 models
- [ ] "Best Model" is identified with justification
- [ ] `models/` folder created with 5 .pkl files
- [ ] All metrics are between 0 and 1
- [ ] ROC-AUC scores > 0.5 (better than random)

---

## 📝 For Submission

### Required Files:
1. ✅ `Assignment_Supervised_Machine_Learning.ipynb` (with outputs)
2. ✅ `data.xlsx`
3. ✅ `README.md`
4. ✅ `models/*.pkl` (5 files)

### Optional Files:
- Convert notebook to PDF: File → Print → Save as PDF
- Extract .py file: File → Export → Python Script

---

## 💡 Pro Tips

1. **Run cells sequentially** - Don't skip cells or run out of order
2. **Check outputs after each section** - Verify results make sense
3. **GridSearchCV verbose output** - Shows progress during tuning
4. **Save your work** - Ctrl+S frequently
5. **Review visualizations** - Zoom in to see details

---

## 🎓 Assignment Grading Points

This notebook covers all required components:

✅ **Part 1: Data Loading** (10%)
- Load data ✓
- Display info ✓
- Check nulls ✓

✅ **Part 2: EDA** (20%)
- Visualizations ✓
- Answer 4 questions ✓

✅ **Part 3: Preprocessing** (15%)
- Encoding ✓
- Scaling ✓
- Train-test split ✓

✅ **Part 4: Model Building** (25%)
- 3 models ✓
- Proper training ✓

✅ **Part 5: Evaluation** (15%)
- All metrics ✓
- Confusion matrix ✓
- ROC curves ✓

✅ **Part 6: Hyperparameter Tuning** (10%)
- GridSearchCV ✓
- Improved performance ✓

✅ **Part 7: Feature Importance** (5%)
- Visualization ✓
- Top features ✓

---

## 🏁 Next Steps After Running

1. **Review all outputs** - Read through results
2. **Understand insights** - What do the visualizations tell you?
3. **Check best model** - Why was it selected?
4. **Export to PDF** - For report submission
5. **Write conclusions** - Based on your findings

---

## ⏱️ Time Estimate

- **First-time setup**: 5 minutes
- **Running notebook**: 3-5 minutes
- **Reviewing results**: 10-15 minutes
- **Total**: ~20-25 minutes

---

**Ready? Let's go! Open the notebook and click "Run All" 🚀**

For detailed information, see `README.md`
