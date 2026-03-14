# Power BI Bank Customer Dashboard - Complete Implementation Guide

## Overview
This guide will help you create a comprehensive Bank Customer Dashboard analyzing customer activity, exits, and retention patterns using your Bank Project.xlsx file.

---

## STEP 1: Data Import and Preparation

### 1.1 Import Data from Excel
1. Open Power BI Desktop
2. Click **Get Data** → **Excel**
3. Navigate to `Bank Project.xlsx`
4. Select **ALL** the following tables:
   - ✅ **Bank Departure** (Main fact table)
   - ✅ **CreditCard** (Lookup table)
   - ✅ **ActiveCustomer** (Lookup table)
   - ✅ **CustomerInfo** (Lookup table)
   - ✅ **ExitCustomer** (Lookup table)
   - ✅ **Gender** (Lookup table)
   - ✅ **Geography** (Lookup table)
5. Click **Load** (or **Transform Data** if you need cleaning)

### 1.2 Expected Table Structures

**Bank Departure (Main Table):**
- RowNumber
- CustomerId
- CreditScore
- GeographyID
- GenderID
- Age
- Tenure
- Balance
- NumOfProducts
- HasCrCard (1 = has card, 0 = no card)
- IsActiveMember (1 = active, 0 = inactive)
- EstimatedSalary
- Exited (1 = exited, 0 = retained)
- Bank DOJ (Date of Joining)

**Lookup Tables:**
- **CreditCard**: HasCrCard, Category
- **ActiveCustomer**: IsActiveMember, ActiveCategory
- **CustomerInfo**: CustomerId, Surname
- **ExitCustomer**: ExitID, ExitCategory
- **Gender**: GenderID, GenderCategory
- **Geography**: GeographyID, GeographyLocation

### 1.3 Data Cleaning (Power Query - Optional)
If you need to transform data:
1. Click **Transform Data** to open Power Query Editor
2. Check data types are correct (dates as Date, numbers as Whole Number)
3. Ensure no null values in key columns
4. Click **Close & Apply**

---

## STEP 2: Create Table Relationships (Data Model)

### 2.1 Set Up Relationships
Go to **Model View** and create the following relationships:

1. **Bank Departure[GeographyID]** → **Geography[GeographyID]** (Many to One)
2. **Bank Departure[GenderID]** → **Gender[GenderID]** (Many to One)
3. **Bank Departure[HasCrCard]** → **CreditCard[HasCrCard]** (Many to One)
4. **Bank Departure[IsActiveMember]** → **ActiveCustomer[IsActiveMember]** (Many to One)
5. **Bank Departure[Exited]** → **ExitCustomer[ExitID]** (Many to One)
6. **Bank Departure[CustomerId]** → **CustomerInfo[CustomerId]** (Many to One)

**All relationships should be:**
- Cardinality: Many to One (*)
- Cross filter direction: Single (or Both if needed)
- Active relationship

### 2.2 Create a Date Table for Time Intelligence

**Create a new table** using DAX:
1. Go to **Modeling** tab → **New Table**
2. Enter the following DAX:

```DAX
DateTable = 
ADDCOLUMNS(
    CALENDAR(DATE(2016,1,1), DATE(2022,12,31)),
    "Year", YEAR([Date]),
    "Month", FORMAT([Date], "MMMM"),
    "MonthNum", MONTH([Date]),
    "MonthShort", FORMAT([Date], "MMM"),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "MonthYear", FORMAT([Date], "MMM YYYY")
)
```

3. **Mark as Date Table:**
   - Right-click on DateTable → Mark as Date Table
   - Select [Date] column

4. **Create Relationship:**
   - Connect **DateTable[Date]** to **Bank Departure[Bank DOJ]** (Many to One)

---

## STEP 3: Create DAX Measures

Go to **Modeling** tab → **New Measure** and create each of the following measures:

### 3.1 Basic Count Measures (for Top KPI Cards)

#### 1. Total Customers
```DAX
Total Customers = DISTINCTCOUNT('Bank Departure'[CustomerId])
```

#### 2. Active Customers
```DAX
Active Customers = 
CALCULATE(
    [Total Customers],
    'Bank Departure'[IsActiveMember] = 1
)
```

#### 3. Inactive Customers
```DAX
Inactive Customers = 
CALCULATE(
    [Total Customers],
    'Bank Departure'[IsActiveMember] = 0
)
```

#### 4. Credit Card Holder
```DAX
Credit Card Holder = 
CALCULATE(
    [Total Customers],
    'Bank Departure'[HasCrCard] = 1
)
```

#### 5. Non Credit Holders
```DAX
Non Credit Holders = 
CALCULATE(
    [Total Customers],
    'Bank Departure'[HasCrCard] = 0
)
```

#### 6. Exit Customer
```DAX
Exit Customer = 
CALCULATE(
    [Total Customers],
    'Bank Departure'[Exited] = 1
)
```

#### 7. Retain Customers
```DAX
Retain Customers = 
CALCULATE(
    [Total Customers],
    'Bank Departure'[Exited] = 0
)
```

---

### 3.2 Time Intelligence Measures (for Line Chart)

#### Previous Month Exit Customers
```DAX
Previous Month Exit = 
CALCULATE(
    [Exit Customer],
    DATEADD(DateTable[Date], -1, MONTH)
)
```

---

### 3.3 Credit Score Category (Calculated Column)

You need to create a credit score category column for the bar chart.

**Go to Data view** → Select **Bank Departure** table → **New Column**:

```DAX
CreditCategory = 
SWITCH(
    TRUE(),
    'Bank Departure'[CreditScore] >= 800, "Excellent",
    'Bank Departure'[CreditScore] >= 740, "Very Good",
    'Bank Departure'[CreditScore] >= 670, "Good",
    'Bank Departure'[CreditScore] >= 580, "Fair",
    'Bank Departure'[CreditScore] < 580, "Poor",
    "Unknown"
)
```

---

## STEP 4: Create Visualizations

### 4.1 Top KPI Cards (Row 1)

Create **7 Card Visuals** across the top of your dashboard:

1. **Total Customers Card**
   - Visual: Card
   - Field: Drag `Total Customers` measure
   - Title: "Total Customers"

2. **Active Customers Card**
   - Visual: Card
   - Field: `Active Customers` measure
   - Title: "Active Customers"

3. **Inactive Customers Card**
   - Visual: Card
   - Field: `Inactive Customers` measure
   - Title: "Inactive Customers"
   - Tooltip: Shows 4,849

4. **Credit Card Holder Card**
   - Visual: Card
   - Field: `Credit Card Holder` measure
   - Title: "Credit Card Holder"

5. **Non Credit Holders Card**
   - Visual: Card
   - Field: `Non Credit Holders` measure
   - Title: "Non Credit Holders"

6. **Exit Customer Card**
   - Visual: Card
   - Field: `Exit Customer` measure
   - Title: "Exit Customer"

7. **Retain Customers Card**
   - Visual: Card
   - Field: `Retain Customers` measure
   - Title: "Retain Customers"

**Formatting Tips:**
- Align all cards horizontally at the top
- Use consistent spacing
- Set background color to white
- Add subtle borders

---

### 4.2 Create Slicers (Left Panel)

Create a vertical column of slicers on the left side:

1. **Select Year Slicer**
   - Visual: Slicer
   - Field: `DateTable[Year]`
   - Style: Dropdown
   - Title: "Select Year"

2. **Select Month Slicer**
   - Visual: Slicer
   - Field: `DateTable[Month]` or `DateTable[MonthNum]`
   - Style: Dropdown
   - Title: "Select Month"

3. **Geography Location Slicer**
   - Visual: Slicer
   - Field: `Geography[GeographyLocation]`
   - Style: Dropdown
   - Title: "Geography Location"
   - Options: France, Spain, Germany

4. **Active Category Slicer**
   - Visual: Slicer
   - Field: `ActiveCustomer[ActiveCategory]`
   - Style: Dropdown
   - Title: "Active Category"
   - Options: Active Member, Inactive Member

5. **Exit Category Slicer**
   - Visual: Slicer
   - Field: `ExitCustomer[ExitCategory]`
   - Style: Dropdown
   - Title: "Exit Category"
   - Options: Exit, Retain

6. **Gender Category Slicer**
   - Visual: Slicer
   - Field: `Gender[GenderCategory]`
   - Style: Dropdown
   - Title: "Gender Category"
   - Options: Male, Female

7. **Category Slicer** (Credit Card)
   - Visual: Slicer
   - Field: `CreditCard[Category]`
   - Style: Dropdown
   - Title: "Category"
   - Options: credit card holder, non credit card holder

**Add Reset Filters Button:**
1. Insert → Button → Blank
2. Change text to "Reset Filters"
3. Format:
   - Background: Teal (#5B9BD5)
   - Text: White, Bold
4. Action → Type: Bookmark or Page Refresh

---

### 4.3 Total Customer By Year Active Category (Clustered Column Chart)

**Visual Type:** Clustered Column Chart

**Configuration:**
- **X-axis:** `DateTable[Year]`
- **Y-axis:** `Total Customers` measure
- **Legend:** `ActiveCustomer[ActiveCategory]`
- **Data Labels:** On

**Expected Values:**
- 2016: Inactive ~960, Active ~991
- 2017: Inactive ~1,049, Active ~1,094
- 2018: Inactive ~1,249, Active ~1,344
- 2019: Inactive ~1,591, Active ~1,722

**Colors:**
- Inactive Customers: Green (#70AD47)
- Active Customers: Teal/Blue (#4472C4)

**Title:** "Total Customer By Year Active Category"

---

### 4.4 Exit Customers and Previous Month Exit Customers (Line Chart)

**Visual Type:** Line Chart

**Configuration:**
- **X-axis:** `DateTable[Month]` or use month names
- **Y-axis Lines:** 
  - `Exit Customer` measure
  - `Previous Month Exit` measure
- **Data Labels:** Optional

**Colors:**
- 2018: Green line
- 2019: Teal/Blue line

**Expected Pattern:**
- Shows monthly trend from January to December
- Two lines comparing 2018 vs 2019

**Title:** "Exit Customers and Previous Month Exit Customers"

---

### 4.5 Exit Customer By Credit Type (Horizontal Bar Chart)

**Visual Type:** Bar Chart (Horizontal)

**Configuration:**
- **Y-axis:** `Bank Departure[CreditCategory]` (calculated column you created)
- **X-axis:** `Exit Customer` measure
- **Data Labels:** On (show values)

**Sorting:** Sort by Exit Customer value descending

**Expected Values:**
- Fair: ~685
- Poor: ~520
- Good: ~452
- Very Good: ~252
- Excellent: ~128

**Color:** Single teal/blue color

**Title:** "Exit Customer By Credit Type"

---

### 4.6 Exit Customers By Gender Category (Donut Chart)

**Visual Type:** Donut Chart

**Configuration:**
- **Legend:** `Gender[GenderCategory]`
- **Values:** `Exit Customer` measure
- **Detail Labels:** Show percentage

**Expected Values:**
- Female: 56% (shown in green)
- Male: 44% (shown in teal/blue)

**Center Label:** Show "100%"

**Title:** "Exit Customers By Gender Category"

---

### 4.7 Exit Customers By Category (Donut Chart - Credit Card)

**Visual Type:** Donut Chart

**Configuration:**
- **Legend:** `CreditCard[Category]`
- **Values:** `Exit Customer` measure
- **Detail Labels:** Show percentage

**Expected Values:**
- credit card holder: 69.9% (teal/blue)
- non credit card holder: 30.1% (green)

**Center Label:** Show percentage

**Title:** "Exit Customers By Category"

---

## STEP 5: Formatting and Design

### 5.1 Overall Dashboard Layout
- **Canvas Background:** Light gray or white (#F3F2F1 or #FFFFFF)
- **Page Size:** 16:9 (Default)
- **View:** Fit to Width

### 5.2 KPI Cards Formatting
For each card at the top:
1. Click on card → Format visual
2. **Callout value:**
   - Font: Segoe UI Bold
   - Size: 32-40
   - Color: Black or Dark Gray
3. **Category label:**
   - Font: Segoe UI Regular
   - Size: 12-14
   - Color: Dark Gray
4. **Background:** White
5. **Border:** Light gray, 1-2px
6. **Alignment:** Center

### 5.3 Chart Titles
- Select each visual → Format → Title
- **Font:** Segoe UI, Bold or Italic
- **Size:** 12-14
- **Color:** Black
- **Alignment:** Left or Center

### 5.4 Color Scheme
Use consistent colors across all visuals:
- **Green:** #70AD47 (for Inactive, Female, Non-card holders)
- **Teal/Blue:** #4472C4 (for Active, Male, Card holders)
- **Additional colors:** Use Power BI default palette or custom

### 5.5 Slicer Formatting
- Background: White
- Border: Light gray
- Style: Dropdown (more compact)
- Header: Bold, Dark gray

### 5.6 Reset Filters Button
1. Insert → Button → Blank
2. Text: "Reset Filters"
3. Button style:
   - Fill: Teal (#5B9BD5)
   - Text: White, Bold, 12pt
   - Border: None or 1px darker teal
4. Action: Bookmark or use Power BI Service reset

---

## STEP 6: Additional DAX Measures (Optional Enhancements)

### Calculate Percentages
```DAX
Active % = 
DIVIDE([Active Customers], [Total Customers], 0)
```

```DAX
Exit Rate = 
DIVIDE([Exit Customer], [Total Customers], 0)
```

```DAX
Retention Rate = 
DIVIDE([Retain Customers], [Total Customers], 0)
```

### Year over Year Analysis
```DAX
YoY Customer Growth = 
VAR CurrentYearCustomers = [Total Customers]
VAR PreviousYearCustomers = 
    CALCULATE(
        [Total Customers],
        DATEADD(DateTable[Date], -1, YEAR)
    )
RETURN
    DIVIDE(CurrentYearCustomers - PreviousYearCustomers, PreviousYearCustomers, 0)
```

### Average Metrics
```DAX
Avg Balance = AVERAGE('Bank Departure'[Balance])
```

```DAX
Avg Credit Score = AVERAGE('Bank Departure'[CreditScore])
```

```DAX
Avg Age = AVERAGE('Bank Departure'[Age])
```

---

## STEP 7: Interactions and Final Touches

### 7.1 Edit Interactions
1. Select a visual (e.g., a chart)
2. Go to **Format** tab → **Edit Interactions**
3. For each other visual, choose:
   - **Filter** (funnel icon) - recommended for slicers
   - **Highlight** (bar chart icon) - for cross-highlighting
   - **None** (no icon) - to prevent interaction

**Best Practice:**
- Slicers should filter all visuals
- Charts can highlight each other
- KPI cards should be filtered by slicers

### 7.2 Add Tooltips
- Hover over visual → More options (...)
- Edit tooltip
- Add additional fields like:
  - Avg Credit Score
  - Avg Balance
  - Count of Products

### 7.3 Test Your Dashboard
✅ Click each slicer and verify:
- All visuals update correctly
- Numbers make sense
- No blank or error values

✅ Test Filter Combinations:
- Select Year 2019
- Select Geography: France
- Verify totals change appropriately

✅ Hover over charts:
- Tooltips show correct information
- Cross-filtering works as expected

---

## STEP 8: Publish and Share (Optional)

### 8.1 Save Your Work
- File → Save As
- Name: "Bank Customer Dashboard.pbix"

### 8.2 Publish to Power BI Service
1. Home tab → **Publish**
2. Select workspace
3. Click **Select**
4. Wait for upload to complete

### 8.3 Share Dashboard
- Go to app.powerbi.com
- Find your report
- Click **Share** or create an **App**

---

## Common Issues and Troubleshooting

### Issue 1: Wrong Totals or Numbers Don't Match
**Solution:** 
- Verify you're using DISTINCTCOUNT for customer counts
- Check that relationships are set correctly (Many to One)
- Ensure no duplicate rows in fact table

### Issue 2: Date Filters Not Working
**Solution:** 
- Mark DateTable as date table (right-click → Mark as Date Table)
- Verify relationship between DateTable[Date] and Bank Departure[Bank DOJ]
- Check relationship is active and cross-filter direction is correct

### Issue 3: Slicers Don't Filter All Visuals
**Solution:** 
- Use Edit Interactions to ensure slicers have filter icons (not none)
- Check relationships in Model View
- Verify tables are properly related

### Issue 4: Previous Month Shows Blank in Line Chart
**Solution:** 
- Ensure DateTable has continuous dates (no gaps)
- Check DATEADD function syntax
- Verify relationship to date column

### Issue 5: Credit Score Category Shows "Unknown"
**Solution:** 
- Check CreditScore column for null values
- Adjust SWITCH formula thresholds if needed
- Verify CreditScore is numeric type

### Issue 6: Percentages in Donut Charts Don't Add to 100%
**Solution:** 
- Check for null or missing category values
- Ensure all records have proper lookup values
- Verify relationships are working

---

## Quick Reference: All Table and Column Names

### Main Fact Table: **Bank Departure**
- CustomerId
- CreditScore
- GeographyID
- GenderID
- Age
- Tenure
- Balance
- NumOfProducts
- HasCrCard (1 = Yes, 0 = No)
- IsActiveMember (1 = Yes, 0 = No)
- Exited (1 = Yes, 0 = No)
- EstimatedSalary
- Bank DOJ (Date of Joining)

### Dimension Tables:
- **Geography**: GeographyID, GeographyLocation (France, Spain, Germany)
- **Gender**: GenderID, GenderCategory (Male, Female)
- **CreditCard**: HasCrCard, Category (credit card holder, non credit card holder)
- **ActiveCustomer**: IsActiveMember, ActiveCategory (Active Member, Inactive Member)
- **ExitCustomer**: ExitID, ExitCategory (Exit, Retain)
- **CustomerInfo**: CustomerId, Surname

### Calculated Table:
- **DateTable**: Date, Year, Month, MonthNum, MonthShort, Quarter, MonthYear

### Calculated Column:
- **Bank Departure[CreditCategory]**: Excellent, Very Good, Good, Fair, Poor

---

## Complete Measures List

Copy and paste all these measures into Power BI:

```DAX
Total Customers = DISTINCTCOUNT('Bank Departure'[CustomerId])

Active Customers = CALCULATE([Total Customers], 'Bank Departure'[IsActiveMember] = 1)

Inactive Customers = CALCULATE([Total Customers], 'Bank Departure'[IsActiveMember] = 0)

Credit Card Holder = CALCULATE([Total Customers], 'Bank Departure'[HasCrCard] = 1)

Non Credit Holders = CALCULATE([Total Customers], 'Bank Departure'[HasCrCard] = 0)

Exit Customer = CALCULATE([Total Customers], 'Bank Departure'[Exited] = 1)

Retain Customers = CALCULATE([Total Customers], 'Bank Departure'[Exited] = 0)

Previous Month Exit = CALCULATE([Exit Customer], DATEADD(DateTable[Date], -1, MONTH))
```

---

## Dashboard Checklist

Use this checklist to verify your dashboard is complete:

### Data Import
- [ ] Imported Bank Project.xlsx
- [ ] All 7 tables loaded (Bank Departure + 6 lookup tables)
- [ ] Data types are correct

### Data Model
- [ ] Created DateTable
- [ ] Marked DateTable as date table
- [ ] Created 7 relationships (GeographyID, GenderID, HasCrCard, IsActiveMember, Exited, CustomerId, Date)
- [ ] All relationships are Many to One

### Calculated Columns
- [ ] Created CreditCategory column in Bank Departure table

### DAX Measures
- [ ] Total Customers
- [ ] Active Customers
- [ ] Inactive Customers
- [ ] Credit Card Holder
- [ ] Non Credit Holders
- [ ] Exit Customer
- [ ] Retain Customers
- [ ] Previous Month Exit

### Visualizations
- [ ] 7 KPI cards at top (all measures)
- [ ] 7 slicers on left side (Year, Month, Geography, Active, Exit, Gender, Category)
- [ ] Reset Filters button
- [ ] Clustered column chart (Total Customer By Year Active Category)
- [ ] Line chart (Exit Customers and Previous Month)
- [ ] Horizontal bar chart (Exit Customer By Credit Type)
- [ ] Donut chart (Exit Customers By Gender)
- [ ] Donut chart (Exit Customers By Category - Credit)

### Formatting
- [ ] All cards formatted with consistent style
- [ ] Chart titles are clear and descriptive
- [ ] Color scheme is consistent (Green and Teal/Blue)
- [ ] Slicers are styled consistently
- [ ] Dashboard layout matches reference image

### Testing
- [ ] All slicers filter visuals correctly
- [ ] Numbers make sense and match expectations
- [ ] No errors or blank values
- [ ] Tooltips work properly
- [ ] Cross-filtering works as expected

### Final Steps
- [ ] Saved PBIX file
- [ ] Tested all functionality
- [ ] Ready to publish (optional)

---

## Expected Results Validation

Use these numbers to validate your dashboard (when no filters applied):

- **Total Customers:** 10,000
- **Active Customers:** 5,151
- **Inactive Customers:** 4,849
- **Credit Card Holder:** 7,055
- **Non Credit Holders:** 2,945
- **Exit Customer:** 2,037
- **Retain Customers:** 7,963

**Year Breakdown:**
- 2016: ~1,951 customers (960 inactive, 991 active)
- 2017: ~2,143 customers (1,049 inactive, 1,094 active)
- 2018: ~2,593 customers (1,249 inactive, 1,344 active)
- 2019: ~3,313 customers (1,591 inactive, 1,722 active)

**Geography:**
- France, Spain, Germany (verify distribution)

**Gender:**
- Male, Female (Exit: Male 44%, Female 56%)

---

## Next Steps After Completion

1. **Add More Analytics:**
   - Average balance by geography
   - Customer tenure analysis
   - Product count analysis
   
2. **Create Additional Pages:**
   - Detailed customer table
   - Credit score deep dive
   - Retention analysis page

3. **Set Up Alerts:**
   - Alert when exit rate exceeds threshold
   - Monthly report email

4. **Share with Stakeholders:**
   - Publish to workspace
   - Create app
   - Set up row-level security (if needed)

---

## Resources and Tips

**Power BI Best Practices:**
- Use measures instead of calculated columns when possible (better performance)
- Create a separate Measures table to organize all measures
- Use meaningful names for all objects
- Document complex DAX formulas with comments
- Test performance with larger datasets

**Learning Resources:**
- Microsoft Learn: Power BI documentation
- SQLBI.com: Advanced DAX tutorials
- Power BI Community: Forums for questions

**Performance Tips:**
- Avoid bidirectional filtering unless necessary
- Use CALCULATE instead of FILTER when possible
- Import mode is faster than DirectQuery for small datasets
- Remove unused columns from model

---

## Need Help?

If you encounter specific errors or need clarification:

1. Check the **Common Issues** section above
2. Verify **Data Model** relationships in Model View
3. Test **one visual at a time** to isolate problems
4. Use **Performance Analyzer** to identify slow visuals
5. Review **DAX formula** syntax carefully

**Success Tips:**
- Build dashboard incrementally (don't try to do everything at once)
- Test each measure as you create it
- Save frequently
- Keep a copy of working version before major changes

---

**Congratulations!** You now have a complete guide to build your Bank Customer Dashboard in Power BI. Follow each step carefully, and you'll have a professional dashboard matching your reference image.
