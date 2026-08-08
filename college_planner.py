def calculate_college_debt():
    print("=" * 50)
    print("      SMART BUDGET & COLLEGE COST PLANNER")
    print("=" * 50)

    # --- USER INPUTS ---
    try:
        college_name = input("Enter the college name: ")
        base_tuition = float(input("Enter Year 1 Tuition & Fees ($): "))
        base_housing = float(input("Enter Year 1 Housing & Meal Plan ($): "))
        annual_scholarship = float(input("Enter annual Merit Scholarship/Grants ($): "))
        inflation_rate = float(input("Estimated annual tuition inflation rate (e.g., 4 for 4%): ")) / 100
    except ValueError:
        print("\n[Error] Please enter valid numbers for financial fields.")
        return

    # --- INITIAL VARIABLES ---
    total_gross_cost = 0
    total_scholarships_received = 0
    total_funding_gap = 0
    
    current_tuition = base_tuition
    current_housing = base_housing

    print(f"\n--- 4-YEAR FINANCIAL PROJECTION FOR {college_name.upper()} ---")
    print(f"{'Year':<6} | {'Gross Cost':<12} | {'Scholarship':<12} | {'Net Cost (Gap)':<15}")
    print("-" * 55)

    # --- 4-YEAR LOOP ---
    for year in range(1, 5):
        # Calculate costs for the current year
        year_gross = current_tuition + current_housing
        year_net = max(0.0, year_gross - annual_scholarship) # Net cost cannot be negative
        
        # Add to cumulative lifetime totals
        total_gross_cost += year_gross
        total_scholarships_received += annual_scholarship
        total_funding_gap += year_net

        # Print formatted row for the current year
        print(f"Year {year:<1} | ${year_gross:,.2f:<11} | ${annual_scholarship:,.2f:<11} | ${year_net:,.2f:<14}")

        # Compound the costs for the NEXT year using the inflation rate
        current_tuition *= (1 + inflation_rate)
        current_housing *= (1 + inflation_rate)

    # --- SUMMARY SUMMARY REPORT ---
    print("=" * 55)
    print(f"Total Cumulative Gross Cost:   ${total_gross_cost:,.2f}")
    print(f"Total Scholarships Received:   ${total_scholarships_received:,.2f}")
    print(f"TOTAL ESTIMATED DEBT/GAP:      ${total_funding_gap:,.2f}")
    print("=" * 55)

# Run the program
if __name__ == "__main__":
    calculate_college_debt()
