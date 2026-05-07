# Bank Customer Analytics Dashboard - Complete Build Guide

## Overview
This guide will help you build a comprehensive bank customer analytics dashboard in Tableau that tracks customer behavior, churn analysis, and demographic insights.

**Data Source:** Bank Real time Project.xlsx  
**Date Field Used:** Bank Departure (for exit/churn analysis trends from 2016-2019)

---

## STEP 1: Connect to Data Source

1. Open Tableau Desktop
2. Click on **"Excel"** under Connect
3. Navigate to `2_Tableau` folder
4. Select **"Bank Real time Project.xlsx"**
5. Drag the data sheet to the canvas
6. Review the data structure and field types

---

## STEP 2: Create Calculated Fields

### 2.1 Customer Category Calculations

#### Active Customers
```tableau
IF [Active Category] = "Active Customer" 
THEN [CustomerID] 
END
```

#### Inactive Customers
```tableau
IF [Active Category] = "Inactive Customer" 
THEN [CustomerID] 
END
```

#### Exit Customers
```tableau
IF [Exit Category] = "Exit Customer" 
THEN [CustomerID] 
END
```

#### Retained Customers
```tableau
IF [Exit Category] = "Retain Customer" 
THEN [CustomerID] 
END
```

#### Credit Card Holders
```tableau
IF [Category] = "credit card holder" 
THEN [CustomerID] 
END
```

#### Non Credit Card Holders
```tableau
IF [Category] = "non credit card holder" 
THEN [CustomerID] 
END
```

### 2.2 Count Metrics

#### Total Customers
```tableau
COUNTD([CustomerID])
```

#### Active Customers Count
```tableau
COUNTD([Active Customers])
```

#### Inactive Customers Count
```tableau
COUNTD([Inactive Customers])
```

#### Exit Customers Count
```tableau
COUNTD([Exit Customers])
```

#### Retained Customers Count
```tableau
COUNTD([Retained Customers])
```

#### Credit Card Holders Count
```tableau
COUNTD([Credit Card Holders])
```

#### Non Credit Card Holders Count
```tableau
COUNTD([Non Credit Card Holders])
```

### 2.3 Year and Month Extractions

**Using the [Bank Departure] date field for time-based analysis.**

**⚠️ IMPORTANT:** If "Bank DOJ" or "Bank Departure" shows as **Abc** (text) instead of 📅 (date):
1. Go to Data Source tab → Click Abc icon → Change to **Date**
2. OR use `DATE()` function to convert text to date (see formulas below)

#### Year
```tableau
YEAR(DATE([Bank Departure]))
```
*If Tableau recognizes it as a date, you can use: `YEAR([Bank Departure])`*

#### Month Name
```tableau
DATENAME('month', DATE([Bank Departure]))
```
*If recognized as date: `DATENAME('month', [Bank Departure])`*

#### Month Number (for proper sorting)
```tableau
MONTH(DATE([Bank Departure]))
```
*If recognized as date: `MONTH([Bank Departure])`*

**Note:** The `DATE()` function converts text-formatted dates to proper date type. Use this if you see "Abc" icon instead of calendar icon 📅.

### 2.4 Credit Type (Credit Score Grouping)

Create a calculated field to group credit scores into categories:

#### Credit Type
```tableau
IF [Credit Score] >= 800 THEN "Excellent"
ELSEIF [Credit Score] >= 740 THEN "Very Good"
ELSEIF [Credit Score] >= 670 THEN "Good"
ELSEIF [Credit Score] >= 580 THEN "Fair"
ELSE "Poor"
END
```

**Note:** This groups credit scores into standard credit rating categories (Excellent, Very Good, Good, Fair, Poor).

---

## STEP 3: Create Parameters

### Parameter 1: Select Year
- **Name:** Select Year Parameter
- **Data Type:** Integer
- **Allowable Values:** List
- **Values:** Add: 0 (for "All"), 2016, 2017, 2018, 2019
- **Current Value:** 0

**Year Parameter Calculated Field:**
```tableau
IF [Select Year Parameter] = 0 
THEN TRUE 
ELSEIF [Year] = [Select Year Parameter] 
THEN TRUE 
ELSE FALSE 
END
```

### Parameter 2: Select Month
- **Name:** Select Month Parameter
- **Data Type:** String
- **Allowable Values:** List
- **Values:** All, January, February, March, April, May, June, July, August, September, October, November, December
- **Current Value:** All

**Month Parameter Calculated Field:**
```tableau
IF [Select Month Parameter] = "All" 
THEN TRUE 
ELSEIF [Month Name] = [Select Month Parameter] 
THEN TRUE 
ELSE FALSE 
END
```

---

## STEP 4: Build Individual Visualizations

### 4.1 KPI Cards (Top Row)

Create 7 separate worksheets, one for each KPI:

#### Sheet 1: Total Customers
1. Drag **Total Customers** to Text
2. Format as large number
3. Add title "Total Customers"
4. Center align
5. Font size: 24-28pt for number

#### Sheet 2: Active Customers
1. Drag **Active Customers Count** to Text
2. Format similarly

#### Sheet 3: Inactive Customers
1. Drag **Inactive Customers Count** to Text
2. Format similarly

#### Sheet 4: Credit Card Holder
1. Drag **Credit Card Holders Count** to Text
2. Format similarly

#### Sheet 5: Non Credit Holders
1. Drag **Non Credit Card Holders Count** to Text
2. Format similarly

#### Sheet 6: Exit Customer
1. Drag **Exit Customers Count** to Text
2. Format similarly

#### Sheet 7: Retain Customers
1. Drag **Retained Customers Count** to Text
2. Format similarly

### 4.2 Total Customer By Year Active Category (Stacked Bar Chart)

**Worksheet: Customer by Year**
1. Drag **Year** to Columns
2. Drag **Total Customers** (or COUNTD([CustomerID])) to Rows
3. Drag **Active Category** to Color
4. Change mark type to **Bar**
5. Show labels on bars
6. Color scheme:
   - Inactive Customers: Green
   - Active Customers: Blue/Teal
7. Sort by Year ascending
8. Add data labels showing values

### 4.3 Exit Customers By Year and Month (Line Chart)

**Worksheet: Exit Trend**
1. Drag **Year** to Columns
2. Drag **Month Name** to Columns (right of Year)
3. Drag **Exit Customers Count** to Rows
4. Change mark type to **Line**
5. Drag **Year** to Color
6. Add markers to lines
7. Right-click **Month Name** → Sort → Sort By Field → Month Number
8. Format:
   - Different color for each year
   - Add legend
9. Optional: Add labels at peaks

**Alternative - Just by Month (aggregated across years):**
1. Drag **Month Name** to Columns only
2. Drag **Exit Customers Count** to Rows
3. Line chart with single line showing monthly pattern

### 4.4 Exit Customer By Credit Type (Horizontal Bar Chart)

**Worksheet: Exit by Credit Type**
1. Drag **Exit Customers Count** to Columns
2. Drag **Credit Type** (the calculated field you created in Step 2.4) to Rows
3. Sort by Exit Customers Count descending
4. Add data labels at end of bars
5. Color: Teal/Blue
6. Format axis to start at 0
7. The chart should show: Excellent, Very Good, Good, Fair, Poor with their respective counts

### 4.5 Exit Customers By Gender Category (Donut Chart)

**Worksheet: Exit by Gender**
1. Drag **Exit Customers Count** to Angle
2. Drag **Gender Category** to Color
3. Change mark type to **Pie**
4. Drag a duplicate of **Exit Customers Count** to Label
5. Quick Table Calculation → Percent of Total
6. To create donut:
   - Duplicate the sheet
   - On second sheet, remove Gender from Color
   - Make it a small white circle
   - Place this on top in dashboard
7. Colors:
   - Female: Green
   - Male: Blue/Teal
8. Show percentages on chart

### 4.6 Exit Customers By Category (Pie Chart)

**Worksheet: Exit by Category**
1. Drag **Exit Customers Count** to Angle
2. Drag **Category** to Color
3. Change mark type to **Pie**
4. Add labels with percentages
5. Format:
   - Credit Card Holder: Blue/Teal
   - Non Credit Card Holder: Green
6. Show percentages

---

## STEP 5: Create Filters

Create separate filter worksheets or use dashboard filters:

### Filter 1: Select Year
- Use the **Select Year Parameter** 
- Show parameter control on dashboard
- Display: 0=All, 2016, 2017, 2018, 2019

### Filter 2: Select Month
- Use the **Select Month Parameter**
- Show parameter control on dashboard

### Filter 3: Geography Location
- Field: **Geography Location**
- Type: Single Value (dropdown)
- Include "All" option

### Filter 4: Active Category
- Field: **Active Category**
- Type: Multiple Values (dropdown)
- Show all values

### Filter 5: Exit Category
- Field: **Exit Category**
- Type: Multiple Values (dropdown)

### Filter 6: Gender Category
- Field: **Gender Category**
- Type: Multiple Values (dropdown)

### Filter 7: Category
- Field: **Category**
- Type: Multiple Values (dropdown)

---

## STEP 6: Build the Dashboard

### 6.1 Dashboard Setup
1. Create new Dashboard
2. Set size to **Automatic** or **1366 x 768**
3. Background: Light gray (#F5F5F5)

### 6.2 Layout Structure

```
+------------------------------------------------------------------+
|  Total  | Active | Inactive| Credit | Non-   | Exit   | Retain  |
|  Cust.  | Cust.  | Cust.   | Holder | Credit | Cust.  | Cust.   |
+------------------------------------------------------------------+
| FILTERS |  Customer by Year Active    | Exit Trend Line Chart   |
|         |  Category (Stacked Bar)     | (By Year & Month)       |
| Year    |--------------------------------+------------------------+
| Month   | Exit by  | Exit by  | Exit by Category         |
| Geo     | Credit   | Gender   | (Pie Chart)              |
| Active  | Type     | (Donut)  |                          |
| Exit    | (Bars)   |          |                          |
| Gender  |          |          |                          |
| Category|          |          |                          |
+------------------------------------------------------------------+
```

### 6.3 Assembly Steps

1. **Top Section - KPI Cards:**
   - Drag all 7 KPI worksheets in a horizontal container
   - Equal spacing
   - Add borders between each

2. **Left Side - Filters Panel:**
   - Create vertical container
   - Add Select Year parameter control
   - Add Select Month parameter control
   - Add Geography Location filter
   - Add Active Category filter
   - Add Exit Category filter
   - Add Gender Category filter
   - Add Category filter
   - Background: White
   - Width: 150-200 pixels

3. **Middle Section:**
   - Create horizontal container
   - Left: Customer by Year chart (stacked bars)
   - Right: Exit Trend chart (line chart by year/month)
   - Equal width distribution

4. **Bottom Section:**
   - Create horizontal container
   - Left: Exit by Credit Type (narrow)
   - Middle: Exit by Gender (square)
   - Right: Exit by Category (remaining space)

### 6.4 Formatting

1. **Add borders** to all worksheets
2. **Hide titles** that are redundant
3. **Align all elements** properly
4. **Color scheme consistency:**
   - Primary: Blue/Teal (#1F77B4)
   - Secondary: Green (#2CA02C)
   - Background: Light gray/White
5. **Font consistency:** Arial or Segoe UI, 10-12pt

---

## STEP 7: Apply Dashboard Actions

### Action 1: Filter Action
1. Dashboard → Actions → Add Action → Filter
2. Source: All sheets
3. Target: All sheets
4. Run on: Select
5. Clearing selection will: Show all values

### Action 2: Highlight Action
1. Dashboard → Actions → Add Action → Highlight
2. Source: All sheets
3. Target: All relevant sheets
4. Enable: Hover

### Action 3: Reset Filters
1. Create a blank worksheet with text "Reset Filters"
2. Add to filter panel
3. Create filter action that resets all filters on click

---

## STEP 8: Additional Enhancements

### 8.1 Tooltips
Customize tooltips for each visualization to show:
- Relevant metrics
- Trend information
- Contextual data

Example tooltip for Exit Customers:
```
Exit Customers: <Exit Customers Count>
Month: <Month Name>
Year: <Year>
Geography: <Geography Location>
```

### 8.2 Mobile Layout (Optional)
1. Dashboard → Device Preview
2. Create phone layout
3. Stack visualizations vertically
4. Adjust sizes for mobile viewing

### 8.3 Performance Optimization
1. Use extracts instead of live connection for large datasets
2. Aggregate data where possible
3. Limit quick filters to necessary fields
4. Use context filters for high-cardinality fields

---

## STEP 9: Testing and Validation

### Checklist:
- [ ] All KPIs display correct values
- [ ] Filters work across all visualizations
- [ ] Year and Month parameters function properly
- [ ] Chart interactions (hover, click) work
- [ ] Colors are consistent with the design
- [ ] Labels are visible and formatted
- [ ] Time-based charts display 2016-2019 data correctly
- [ ] Dashboard is responsive
- [ ] No performance issues

---

## STEP 10: Publishing (Optional)

1. Server → Tableau Server/Tableau Public
2. Sign in to your account
3. Set permissions
4. Schedule refresh (if using extract)
5. Share dashboard link

---

## Quick Reference: All Calculated Fields Summary

| Field Name | Formula |
|------------|---------|
| Active Customers | `IF [Active Category] = "Active Customer" THEN [CustomerID] END` |
| Inactive Customers | `IF [Active Category] = "Inactive Customer" THEN [CustomerID] END` |
| Exit Customers | `IF [Exit Category] = "Exit Customer" THEN [CustomerID] END` |
| Retained Customers | `IF [Exit Category] = "Retain Customer" THEN [CustomerID] END` |
| Credit Card Holders | `IF [Category] = "credit card holder" THEN [CustomerID] END` |
| Non Credit Card Holders | `IF [Category] = "non credit card holder" THEN [CustomerID] END` |
| Total Customers | `COUNTD([CustomerID])` |
| Active Customers Count | `COUNTD([Active Customers])` |
| Inactive Customers Count | `COUNTD([Inactive Customers])` |
| Exit Customers Count | `COUNTD([Exit Customers])` |
| Retained Customers Count | `COUNTD([Retained Customers])` |
| Credit Card Holders Count | `COUNTD([Credit Card Holders])` |
| Non Credit Card Holders Count | `COUNTD([Non Credit Card Holders])` |
| Year | `YEAR(DATE([Bank Departure]))` or `YEAR([Bank Departure])` if date type |
| Month Name | `DATENAME('month', DATE([Bank Departure]))` or `DATENAME('month', [Bank Departure])` |
| Month Number | `MONTH(DATE([Bank Departure]))` or `MONTH([Bank Departure])` |
| Credit Type | `IF [Credit Score] >= 800 THEN "Excellent" ELSEIF [Credit Score] >= 740 THEN "Very Good" ELSEIF [Credit Score] >= 670 THEN "Good" ELSEIF [Credit Score] >= 580 THEN "Fair" ELSE "Poor" END` |

**Note:** Use `DATE()` wrapper if field shows as Text (Abc) instead of Date (📅) in Tableau.


---

## Color Palette Reference

- **Primary Blue:** #1F77B4 (Active, Male, Credit Card Holder)
- **Green:** #2CA02C (Inactive, Female, Non-Credit Card Holder)
- **Light Gray Background:** #F5F5F5
- **Border Gray:** #CCCCCC
- **Text Black:** #333333

---

## Troubleshooting Common Issues

### Issue 1: Filters not working across all sheets
**Solution:** Ensure all worksheets use the same data source and fields are spelled exactly the same.

### Issue 2: Previous Month Exit showing NULL
**Solution:** Use `IFNULL([Previous Month Exit], 0)` to handle null values.

### Issue 3: Donut chart not displaying correctly
**Solution:** Layer two pie charts - bottom one with data, top one as white circle for center hole.

### Issue 4: KPI numbers not matching
**Solution:** Check filter context and ensure Level of Detail (LOD) expressions are used correctly if needed.

### Issue 5: "Previous Month Exit" shows error or doesn't work
**Solution:** Make sure you're using `LOOKUP(COUNTD([Exit Customers]), -1)` not `LOOKUP(SUM([Exit Customers Count]), -1)`. The LOOKUP function needs the base aggregation, not a wrapped calculated field. Also, this only works when you have a dimension like Month in your view.

### Issue 6: Calculated fields showing 0 values
**Solution:** 
1. Verify the exact spelling and case of field names (e.g., "Customer Id" vs "CustomerID")
2. Check the exact values in your data - right-click field → Show Filter to see actual values
3. Ensure string matches are exact, including spaces ("Active Customer" vs "Active")
4. Try using `CONTAINS()` or `LOWER()` for more flexible matching

### Issue 7: Date fields showing as Text (Abc) instead of Date (📅)
**Solution:**
1. **In Data Source tab:** Click the Abc icon above the column → Select "Date"
2. **If conversion fails:** Use `DATE()` function: `YEAR(DATE([Bank DOJ]))` instead of `YEAR([Bank DOJ])`
3. **In Excel (best fix):** 
   - Widen column to check if ##### shows dates
   - Format Cells → Date → Save file → Refresh Tableau
   - Look for green triangles (text stored as numbers) → Convert to Number
4. **Check for mixed data:** Some cells might be text, others dates - clean the Excel source

### Issue 8: YEAR/MONTH functions showing errors
**Solution:** The date field is likely stored as text. Use: `YEAR(DATE([Bank Departure]))` to convert text to date first, then extract year.

---

## Tips for Success

1. **Build incrementally** - Create one visualization at a time
2. **Test filters frequently** - Ensure interactivity works as expected
3. **Save versions** - Save different versions as you build
4. **Use naming conventions** - Keep worksheet names clear and organized
5. **Document your work** - Add comments in calculated fields
6. **Check data types** - Ensure fields are recognized correctly (dates, numbers, strings)
7. **Performance matters** - Use extracts for better performance
8. **Mobile-first** - Consider mobile viewing if dashboard will be used on phones/tablets

---

## Next Steps

After completing the dashboard:
1. Schedule regular data refreshes
2. Set up alerts for key metrics
3. Create drill-down dashboards for deeper analysis
4. Add advanced analytics (forecasting, clustering)
5. Integrate with other data sources
6. Train stakeholders on how to use the dashboard

---

**Estimated Time to Complete:** 3-4 hours for first-time build
**Difficulty Level:** Intermediate
**Prerequisites:** Basic Tableau knowledge, understanding of customer analytics

---

Good luck building your Bank Customer Analytics Dashboard! 🎯
