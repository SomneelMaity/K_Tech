# Bank Dashboard Build Checklist ✓

## Phase 1: Data Connection & Preparation
- [ ] Open Tableau Desktop
- [ ] Connect to "Bank Real time Project.xlsx"
- [ ] Verify all columns are imported correctly
- [ ] Check data types (dates, numbers, strings)
- [ ] **IMPORTANT:** Verify "Bank Departure" is recognized as a Date field (📅 icon)
- [ ] Review unique values in key fields

---

## Phase 2: Create Calculated Fields

### Basic Customer Segmentation
- [ ] Active Customers
- [ ] Inactive Customers
- [ ] Exit Customers
- [ ] Retained Customers
- [ ] Credit Card Holders
- [ ] Non Credit Card Holders

### Count Metrics
- [ ] Total Customers
- [ ] Active Customers Count
- [ ] Inactive Customers Count
- [ ] Exit Customers Count
- [ ] Retained Customers Count
- [ ] Credit Card Holders Count
- [ ] Non Credit Card Holders Count

### Time Fields (Using [Bank Departure])
- [ ] **FIRST:** Check if Bank Departure shows Abc or 📅 in Data Source tab
- [ ] **If Abc (text):** Click icon → Change to Date, OR use DATE() wrapper
- [ ] Year: YEAR(DATE([Bank Departure])) or YEAR([Bank Departure])
- [ ] Month Name: DATENAME('month', DATE([Bank Departure])) or DATENAME('month', [Bank Departure])
- [ ] Month Number: MONTH(DATE([Bank Departure])) or MONTH([Bank Departure])

### Credit Type Grouping
- [ ] Credit Type: IF [Credit Score] >= 800 THEN "Excellent" ELSEIF [Credit Score] >= 740 THEN "Very Good" ELSEIF [Credit Score] >= 670 THEN "Good" ELSEIF [Credit Score] >= 580 THEN "Fair" ELSE "Poor" END

---

## Phase 3: Create Parameters

- [ ] Select Year Parameter (with values: All, 2016, 2017, 2018, 2019)
- [ ] Year Filter Calculated Field
- [ ] Select Month Parameter (with all 12 months + All)
- [ ] Month Filter Calculated Field

---

## Phase 4: Build KPI Cards (7 Worksheets)

- [ ] Sheet 1: Total Customers
- [ ] Sheet 2: Active Customers
- [ ] Sheet 3: Inactive Customers
- [ ] Sheet 4: Credit Card Holder
- [ ] Sheet 5: Non Credit Holders
- [ ] Sheet 6: Exit Customer
- [ ] Sheet 7: Retain Customers

**Formatting for each:**
- [ ] Large font size (24-28pt)
- [ ] Center aligned
- [ ] Appropriate number formatting
- [ ] Remove gridlines
- [ ] Add border

---

## Phase 5: Build Chart Visualizations

### Chart 1: Total Customer By Year Active Category
- [ ] Create worksheet "Customer by Year"
- [ ] Add Year to Columns
- [ ] Add Total Customers to Rows
- [ ] Add Active Category to Color
- [ ] Change to Stacked Bar
- [ ] Add data labels
- [ ] Apply color scheme (Green: Inactive, Blue: Active)
- [ ] Add title

### Chart 2: Exit Customers Trend (Line Chart by Year/Month)
- [ ] Create worksheet "Exit Trend"
- [ ] Add Year to Columns
- [ ] Add Month Name to Columns (right of Year)
- [ ] Add Exit Customers Count to Rows
- [ ] Add Year to Color (for different colored lines per year)
- [ ] Change to Line chart with markers
- [ ] Right-click Month Name → Sort by Month Number
- [ ] Add legend
- [ ] Adjust date axis formatting

### Chart 3: Exit Customer By Credit Type
- [ ] Create worksheet "Exit by Credit Type"
- [ ] Add Exit Customers Count to Columns
- [ ] Add Credit Type to Rows
- [ ] Sort descending by count
- [ ] Add data labels
- [ ] Apply blue color scheme
- [ ] Remove gridlines

### Chart 4: Exit Customers By Gender Category
- [ ] Create worksheet "Exit by Gender"
- [ ] Add Exit Customers Count to Angle
- [ ] Add Gender Category to Color
- [ ] Change to Pie chart
- [ ] Add percentage labels
- [ ] Create donut effect (optional: overlay white circle)
- [ ] Apply color scheme (Green: Female, Blue: Male)

### Chart 5: Exit Customers By Category
- [ ] Create worksheet "Exit by Category"
- [ ] Add Exit Customers Count to Angle
- [ ] Add Category to Color
- [ ] Change to Pie chart
- [ ] Add percentage labels
- [ ] Apply color scheme

---

## Phase 6: Create Filters

## Phase 6: Create Filters

- [ ] Parameters already created in Phase 3 (Year, Month)
- [ ] Create Geography Location filter
- [ ] Create Active Category filter
- [ ] Create Exit Category filter
- [ ] Create Gender Category filter
- [ ] Create Category filter
- [ ] Test each filter independently

---

## Phase 7: Build Dashboard

### Layout Setup
- [ ] Create new Dashboard
- [ ] Set size (Automatic or 1366x768)
- [ ] Set background color (#F5F5F5)

### Add Components - Top Row (KPI Cards)
- [ ] Add Total Customers KPI
- [ ] Add Active Customers KPI
- [ ] Add Inactive Customers KPI
- [ ] Add Credit Card Holder KPI
- [ ] Add Non Credit Holders KPI
- [ ] Add Exit Customer KPI
- [ ] Add Retain Customers KPI
- [ ] Arrange in horizontal container
- [ ] Add borders between cards
- [ ] Ensure equal spacing

### Add Components - Left Panel (Filters)
- [ ] Create vertical container for filters
- [ ] Add Select Year parameter control
- [ ] Add Select Month parameter control
- [ ] Add Geography Location filter
- [ ] Add Active Category filter
- [ ] Add Exit Category filter
- [ ] Add Gender Category filter
- [ ] Add Category filter
- [ ] Add "Reset Filters" button/action
- [ ] Set panel background to white
- [ ] Set width to 150-200px

### Add Components - Middle Section
- [ ] Add Customer by Year chart (left)
- [ ] Add Exit Trend chart (right)
- [ ] Arrange in horizontal container
- [ ] Adjust sizes appropriately

### Add Components - Bottom Section
- [ ] Add Exit by Credit Type chart (left, narrow)
- [ ] Add Exit by Gender chart (middle, square)
- [ ] Add Exit by Category chart (right)
- [ ] Arrange in horizontal container

---

## Phase 8: Apply Dashboard Actions

- [ ] Add Filter Action (Select → Filter all sheets)
- [ ] Add Highlight Action (Hover → Highlight)
- [ ] Test filter interactions
- [ ] Test highlight on hover
- [ ] Add Reset Filters action

---

## Phase 9: Final Formatting

### Colors & Styling
- [ ] Verify consistent color scheme across all charts
- [ ] Blue (#1F77B4) for Active/Male/Credit Card Holder
- [ ] Green (#2CA02C) for Inactive/Female/Non-Credit
- [ ] Light gray background (#F5F5F5)

### Text & Labels
- [ ] All titles are visible and clear
- [ ] Font consistency (Arial or Segoe UI)
- [ ] Font sizes appropriate (10-12pt for text)
- [ ] Data labels visible where needed

### Layout
- [ ] All elements properly aligned
- [ ] Borders added to separate sections
- [ ] Spacing is consistent
- [ ] No overlapping elements
- [ ] Responsive layout tested

### Tooltips
- [ ] Customize tooltips for each chart
- [ ] Include relevant metrics
- [ ] Remove unnecessary default information
- [ ] Test tooltip display

---

## Phase 10: Testing & Validation

### Functionality Testing
- [ ] Test all filter combinations
- [ ] Verify parameter controls work correctly
- [ ] Test Year selection
- [ ] Test Month selection
- [ ] Test Geography filter
- [ ] Test Active Category filter
- [ ] Test Exit Category filter
- [ ] Test Gender filter
- [ ] Test Category filter
- [ ] Verify Reset Filters works

### Data Validation
- [ ] Verify Total Customers = Active + Inactive
- [ ] Verify Total Customers = Exit + Retained
- [ ] Verify Total Customers = Credit Card + Non-Credit Card
- [ ] Cross-check numbers with source data
- [ ] Test edge cases (single selections, combinations)

### Visual Validation
- [ ] All charts display correctly
- [ ] No missing data
- [ ] Colors match design
- [ ] Labels are readable
- [ ] Layout matches reference image

### Performance
- [ ] Dashboard loads quickly
- [ ] Filters respond instantly
- [ ] No lag when switching views
- [ ] Consider using extract if slow

---

## Phase 11: Documentation & Sharing

- [ ] Add dashboard description
- [ ] Document data refresh schedule
- [ ] Create user guide (if needed)
- [ ] Test on different screen sizes
- [ ] Test on mobile (if applicable)
- [ ] Save final version with clear name
- [ ] Export as PDF/Image for reference
- [ ] Publish to Tableau Server/Public (if needed)
- [ ] Set up automatic data refresh
- [ ] Share with stakeholders

---

## Troubleshooting Checklist

If something doesn't work:
- [ ] Check data source connection
- [ ] Verify calculated fields syntax
- [ ] Check filter context
- [ ] Ensure field names match exactly
- [ ] Review parameter settings
- [ ] Check for null values
- [ ] Verify data types
- [ ] Clear Tableau cache
- [ ] Restart Tableau (last resort)

---

## Post-Launch

- [ ] Monitor dashboard performance
- [ ] Gather user feedback
- [ ] Schedule regular reviews
- [ ] Plan enhancements
- [ ] Update documentation as needed

---

**Total Estimated Time:** 3-4 hours
**Difficulty:** Intermediate
**Status:** ___________

**Build Started:** ___________
**Build Completed:** ___________
**Tested By:** ___________
**Approved By:** ___________

---

## Notes & Issues

Use this space to track any issues or special notes during the build:

1. _______________________________________________________________

2. _______________________________________________________________

3. _______________________________________________________________

4. _______________________________________________________________

5. _______________________________________________________________
