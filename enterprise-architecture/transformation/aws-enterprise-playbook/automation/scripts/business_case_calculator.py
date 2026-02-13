#!/usr/bin/env python3
"""
AWS Transformation Business Case Calculator
Calculates ROI, NPV, Payback Period, and generates executive reports
"""

import argparse
import json
from datetime import datetime
from typing import Dict, List
import sys


class BusinessCaseCalculator:
    """Calculate financial metrics for AWS transformation"""

    def __init__(self, current_cost: float, aws_cost: float,
                 implementation_cost: float, years: int = 5,
                 discount_rate: float = 0.10):
        """
        Initialize calculator with financial inputs

        Args:
            current_cost: Annual on-premise cost
            aws_cost: Annual AWS cost (steady state)
            implementation_cost: One-time implementation cost
            years: Analysis period in years
            discount_rate: Discount rate for NPV calculation
        """
        self.current_cost = current_cost
        self.aws_cost = aws_cost
        self.implementation_cost = implementation_cost
        self.years = years
        self.discount_rate = discount_rate

        self.results = {}

    def calculate_annual_savings(self) -> float:
        """Calculate annual run-rate savings"""
        return self.current_cost - self.aws_cost

    def calculate_total_benefits(self) -> float:
        """Calculate total benefits over analysis period"""
        annual_savings = self.calculate_annual_savings()
        return annual_savings * self.years

    def calculate_total_costs(self) -> float:
        """Calculate total costs including implementation"""
        return self.implementation_cost + (self.aws_cost * self.years)

    def calculate_roi(self) -> float:
        """
        Calculate Return on Investment (ROI)
        ROI = (Total Benefits - Total Costs) / Total Costs * 100
        """
        total_benefits = self.calculate_total_benefits()
        total_current_costs = self.current_cost * self.years
        total_aws_costs = self.implementation_cost + (self.aws_cost * self.years)

        net_benefit = total_current_costs - total_aws_costs
        roi = (net_benefit / total_aws_costs) * 100

        return roi

    def calculate_npv(self) -> float:
        """
        Calculate Net Present Value (NPV)
        NPV = Sum of (Cash Flow / (1 + r)^t) - Initial Investment
        """
        npv = -self.implementation_cost  # Initial investment (negative)

        for year in range(1, self.years + 1):
            annual_savings = self.calculate_annual_savings()
            discount_factor = (1 + self.discount_rate) ** year
            present_value = annual_savings / discount_factor
            npv += present_value

        return npv

    def calculate_payback_period(self) -> float:
        """
        Calculate Payback Period (months)
        Time to recover initial investment
        """
        annual_savings = self.calculate_annual_savings()

        if annual_savings <= 0:
            return float('inf')  # Never pays back

        payback_years = self.implementation_cost / annual_savings
        payback_months = payback_years * 12

        return payback_months

    def calculate_irr(self) -> float:
        """
        Calculate Internal Rate of Return (IRR)
        Simplified calculation
        """
        # Simplified IRR estimation
        avg_annual_return = self.calculate_annual_savings()
        avg_investment = self.implementation_cost / 2  # Simplified average

        if avg_investment == 0:
            return 0.0

        irr = (avg_annual_return / avg_investment) * 100
        return irr

    def generate_cash_flow_analysis(self) -> List[Dict]:
        """Generate year-by-year cash flow analysis"""
        annual_savings = self.calculate_annual_savings()
        cash_flows = []
        cumulative = -self.implementation_cost

        # Year 0 (implementation)
        cash_flows.append({
            'year': 0,
            'investment': -self.implementation_cost,
            'benefits': 0,
            'net_cash_flow': -self.implementation_cost,
            'cumulative_cash_flow': cumulative
        })

        # Years 1-N
        for year in range(1, self.years + 1):
            # Ramp-up: Year 1 = 50%, Year 2 = 100%
            benefits_multiplier = min(year * 0.5, 1.0)
            year_benefits = annual_savings * benefits_multiplier

            net_cf = year_benefits
            cumulative += net_cf

            cash_flows.append({
                'year': year,
                'investment': 0,
                'benefits': year_benefits,
                'net_cash_flow': net_cf,
                'cumulative_cash_flow': cumulative
            })

        return cash_flows

    def calculate_all_metrics(self) -> Dict:
        """Calculate all financial metrics"""
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'inputs': {
                'current_annual_cost': self.current_cost,
                'aws_annual_cost': self.aws_cost,
                'implementation_cost': self.implementation_cost,
                'analysis_years': self.years,
                'discount_rate': self.discount_rate
            },
            'metrics': {
                'annual_savings': self.calculate_annual_savings(),
                'total_benefits': self.calculate_total_benefits(),
                'roi_percentage': round(self.calculate_roi(), 2),
                'npv': round(self.calculate_npv(), 2),
                'payback_months': round(self.calculate_payback_period(), 1),
                'irr_percentage': round(self.calculate_irr(), 2)
            },
            'cash_flow_analysis': self.generate_cash_flow_analysis()
        }

        return self.results

    def generate_executive_summary(self) -> str:
        """Generate executive summary text"""
        if not self.results:
            self.calculate_all_metrics()

        metrics = self.results['metrics']
        inputs = self.results['inputs']

        summary = f"""
================================================================
     AWS TRANSFORMATION BUSINESS CASE - EXECUTIVE SUMMARY
================================================================

FINANCIAL OVERVIEW
----------------------------------------------------------------
Current Annual Cost (On-Premise):  ${inputs['current_annual_cost']:,.0f}
Projected AWS Annual Cost:         ${inputs['aws_annual_cost']:,.0f}
Implementation Investment:         ${inputs['implementation_cost']:,.0f}
Analysis Period:                   {inputs['analysis_years']} years

KEY FINANCIAL METRICS
----------------------------------------------------------------
Annual Run-Rate Savings:           ${metrics['annual_savings']:,.0f}
Net Present Value (NPV):           ${metrics['npv']:,.0f}
Return on Investment (ROI):        {metrics['roi_percentage']:.1f}%
Payback Period:                    {metrics['payback_months']:.1f} months
Internal Rate of Return (IRR):     {metrics['irr_percentage']:.1f}%

RECOMMENDATION
----------------------------------------------------------------
"""

        # Add recommendation based on metrics
        if metrics['roi_percentage'] > 25 and metrics['payback_months'] < 24:
            summary += "STRONGLY RECOMMENDED: Excellent financial returns\n"
            summary += f"  - ROI of {metrics['roi_percentage']:.1f}% exceeds 25% target\n"
            summary += f"  - Payback period of {metrics['payback_months']:.1f} months is under 24 months\n"
            summary += f"  - Positive NPV of ${metrics['npv']:,.0f} creates shareholder value\n"
        elif metrics['roi_percentage'] > 15 and metrics['payback_months'] < 36:
            summary += "RECOMMENDED: Good financial returns\n"
            summary += f"  - ROI of {metrics['roi_percentage']:.1f}% provides solid returns\n"
            summary += f"  - Payback within {metrics['payback_months']:.1f} months\n"
        else:
            summary += "REQUIRES FURTHER ANALYSIS\n"
            summary += "  - Financial returns below typical thresholds\n"
            summary += "  - Consider non-financial benefits and strategic value\n"

        summary += f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        summary += "================================================================\n"

        return summary

    def print_cash_flow_table(self):
        """Print cash flow analysis table"""
        if not self.results:
            self.calculate_all_metrics()

        cash_flows = self.results['cash_flow_analysis']

        print("\n" + "="*100)
        print("CASH FLOW ANALYSIS")
        print("="*100)
        print(f"{'Year':<8} {'Investment':<20} {'Benefits':<20} {'Net Cash Flow':<20} {'Cumulative':<20}")
        print("-"*100)

        for cf in cash_flows:
            year = f"Year {cf['year']}"
            investment = f"${cf['investment']:,.0f}"
            benefits = f"${cf['benefits']:,.0f}"
            net_cf = f"${cf['net_cash_flow']:,.0f}"
            cumulative = f"${cf['cumulative_cash_flow']:,.0f}"

            print(f"{year:<8} {investment:<20} {benefits:<20} {net_cf:<20} {cumulative:<20}")

        print("="*100 + "\n")

    def save_to_json(self, filepath: str):
        """Save results to JSON file"""
        if not self.results:
            self.calculate_all_metrics()

        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"[OK] Results saved to: {filepath}")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description='AWS Transformation Business Case Calculator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic calculation
  python business_case_calculator.py --current-cost 500000 --aws-cost 350000 --implementation-cost 200000

  # 3-year analysis with custom discount rate
  python business_case_calculator.py --current-cost 1000000 --aws-cost 600000 --implementation-cost 500000 --years 3 --discount-rate 0.12

  # Save results to JSON
  python business_case_calculator.py --current-cost 500000 --aws-cost 350000 --implementation-cost 200000 --output results.json
        """
    )

    parser.add_argument('--current-cost', type=float, required=True,
                       help='Annual on-premise cost ($)')
    parser.add_argument('--aws-cost', type=float, required=True,
                       help='Annual AWS cost ($)')
    parser.add_argument('--implementation-cost', type=float, required=True,
                       help='One-time implementation cost ($)')
    parser.add_argument('--years', type=int, default=5,
                       help='Analysis period (years, default: 5)')
    parser.add_argument('--discount-rate', type=float, default=0.10,
                       help='Discount rate for NPV (default: 0.10)')
    parser.add_argument('--output', type=str, default=None,
                       help='Output JSON file path (optional)')

    args = parser.parse_args()

    # Create calculator
    calc = BusinessCaseCalculator(
        current_cost=args.current_cost,
        aws_cost=args.aws_cost,
        implementation_cost=args.implementation_cost,
        years=args.years,
        discount_rate=args.discount_rate
    )

    # Calculate metrics
    calc.calculate_all_metrics()

    # Print executive summary
    print(calc.generate_executive_summary())

    # Print cash flow table
    calc.print_cash_flow_table()

    # Save to JSON if requested
    if args.output:
        calc.save_to_json(args.output)

    # Print success message
    print("\n" + "[SUCCESS] Business case calculation complete!".center(100))
    print("\nNext Steps:")
    print("  1. Review the executive summary above")
    print("  2. Customize the business case template with these numbers")
    print("  3. Present to stakeholders for approval")
    print("  4. Proceed with Phase 1: Initiation if approved\n")


if __name__ == '__main__':
    main()
