from typing import List, Dict, Any
from src.models.schemas import Transaction, Insight, Prediction, InsightType
from src.services.groq_client import groq_client
from collections import defaultdict
from datetime import date

class AnalysisService:
    """
    Service responsible for orchestrating the AI-powered analysis of financial transactions.
    """
    async def analyze_transactions(self, transactions: List[Transaction]) -> Dict[str, Any]:
        """
        Orchestrates the analysis of transactions: categorization, pattern detection, and predictions.
        
        Args:
            transactions: A list of Transaction objects to analyze.
            
        Returns:
            A dictionary containing categorized transactions, generated insights, and predictions.
        """
        if not transactions:
            return {
                "categorized_transactions": [],
                "insights": [],
                "predictions": []
            }

        # 1. Categorization
        descriptions = [t.description for t in transactions]
        categories = await groq_client.categorize_transactions(descriptions)

        categorized_transactions: List[Transaction] = []
        for i, transaction in enumerate(transactions):
            transaction.category = categories[i] if i < len(categories) else "Uncategorized"
            categorized_transactions.append(transaction)

        # 2. Spending Patterns (Simple example: total spent per category)
        category_spending = defaultdict(float)
        for t in categorized_transactions:
            category_spending[t.category] += t.amount

        insights: List[Insight] = []
        for category, total_spent in category_spending.items():
            if total_spent > 0: # Only consider expenses
                insights.append(
                    Insight(
                        type=InsightType.SPENDING_PATTERN,
                        title=f"Spending Pattern: {category}",
                        description=f"You spent a total of {total_spent:.2f} in '{category}'.",
                        data={"category": category, "total_spent": total_spent}
                    )
                )
        
        # 3. Anomalous Transactions (Simple example: unusually high single transaction)
        # This is a very basic anomaly detection. A real system would use statistical methods.
        average_transaction_amount = sum(t.amount for t in transactions) / len(transactions) if transactions else 0 # Added check for empty transactions
        for t in categorized_transactions:
            if t.amount > (average_transaction_amount * 3) and t.amount > 100: # Example threshold
                insights.append(
                    Insight(
                        type=InsightType.ANOMALY_DETECTED,
                        title=f"Anomaly Detected: Large Transaction in {t.category}",
                        description=f"An unusually large transaction of {t.amount:.2f} was detected in '{t.category}' on {t.date}.",
                        data={"transaction_id": str(t.id), "amount": t.amount, "category": t.category}
                    )
                )

        # 4. Monthly Spending Predictions (Very basic example: average of current month's spending)
        # This is a placeholder. Real predictions require historical data and time-series models.
        predictions: List[Prediction] = []
        current_month_transactions = [t for t in transactions if t.date.month == date.today().month and t.date.year == date.today().year]
        if current_month_transactions:
            current_month_total = sum(t.amount for t in current_month_transactions)
            predictions.append(
                Prediction(
                    period=date.today().strftime("%Y-%m"),
                    predicted_amount=current_month_total, # Simple projection
                    confidence_score=0.5 # Low confidence for simple projection
                )
            )


        return {
            "categorized_transactions": categorized_transactions,
            "insights": insights,
            "predictions": predictions
        }

analysis_service = AnalysisService()
