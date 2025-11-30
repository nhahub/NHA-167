"""
generate_sample_csvs.py

Generates CSV files for:
- users.csv
- cards.csv
- merchants.csv
- transactions.csv



"""

import os
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()

class TransactionDataGenerator:
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        random.seed(seed)
        Faker.seed(seed)

        self.merchant_categories = {
            'grocery': {'fraud_rate': 0.01, 'avg_amount': 85.50},
            'gas_station': {'fraud_rate': 0.02, 'avg_amount': 45.20},
            'restaurant': {'fraud_rate': 0.015, 'avg_amount': 32.80},
            'retail': {'fraud_rate': 0.025, 'avg_amount': 125.40},
            'electronics': {'fraud_rate': 0.035, 'avg_amount': 450.75},
            'online_shopping': {'fraud_rate': 0.04, 'avg_amount': 89.30},
            'travel': {'fraud_rate': 0.03, 'avg_amount': 850.20},
            'entertainment': {'fraud_rate': 0.02, 'avg_amount': 65.80},
            'healthcare': {'fraud_rate': 0.01, 'avg_amount': 180.50},
            'utilities': {'fraud_rate': 0.005, 'avg_amount': 120.30},
            'luxury_goods': {'fraud_rate': 0.08, 'avg_amount': 2500.00},
            'cryptocurrency': {'fraud_rate': 0.12, 'avg_amount': 500.00},
            'money_transfer': {'fraud_rate': 0.15, 'avg_amount': 300.00},
            'adult_entertainment': {'fraud_rate': 0.06, 'avg_amount': 75.00},
            'gambling': {'fraud_rate': 0.10, 'avg_amount': 200.00}
        }

        self.high_risk_locations = [
            'Miami, FL', 'Las Vegas, NV', 'Atlantic City, NJ',
            'Los Angeles, CA', 'New York, NY', 'Chicago, IL'
        ]
        self.normal_locations = [
            'Austin, TX', 'Denver, CO', 'Seattle, WA', 'Portland, OR',
            'Boston, MA', 'Philadelphia, PA', 'Phoenix, AZ', 'San Diego, CA',
            'Dallas, TX', 'Houston, TX', 'Atlanta, GA', 'Nashville, TN'
        ]
        self.device_types = ['mobile', 'desktop', 'tablet', 'pos_terminal']
        self.card_types = ['Visa', 'MasterCard', 'American Express', 'Discover']

    def generate_users(self, n_users: int = 1000) -> List[Dict[str, Any]]:
        users = []
        for i in range(n_users):
            users.append({
                'user_id': f'user_{i+1:05d}',
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': fake.safe_email(),
                'phone': fake.phone_number(),
                'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
                'address': fake.street_address(),
                'city': fake.city(),
                'state': fake.state(),
                'country': 'USA',
                'postal_code': fake.zipcode(),
                'registration_date': fake.date_time_between(start_date='-2y', end_date='now').isoformat(),
                'is_active': random.choice([True, True, True, False]),
                'risk_score': float(np.random.beta(2, 5))
            })
        return users

    def generate_cards(self, users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cards = []
        for user in users:
            n_cards = random.choices([1,2,3], weights=[0.6,0.3,0.1])[0]
            for c in range(n_cards):
                credit_limit = random.choice([5000,10000,15000,20000,25000,50000])
                cards.append({
                    'card_id': f'card_{user["user_id"]}_{c+1:02d}',
                    'user_id': user['user_id'],
                    'card_number': f'****{random.randint(1000,9999)}',
                    'card_type': random.choice(self.card_types),
                    'issuer': random.choice(['Chase Bank','Bank of America','Wells Fargo','Citi Bank','Capital One']),
                    'expiry_date': fake.future_date(end_date='+5y').isoformat(),
                    'is_active': random.choice([True,True,True,False]),
                    'credit_limit': credit_limit,
                    'current_balance': round(random.uniform(0,0.8) * credit_limit,2)
                })
        return cards

    def generate_merchants(self, n_merchants: int = 500) -> List[Dict[str, Any]]:
        merchants = []
        for i in range(n_merchants):
            category = random.choice(list(self.merchant_categories.keys()))
            merchants.append({
                'merchant_id': f'merchant_{i+1:05d}',
                'merchant_name': fake.company(),
                'merchant_category': category,
                'merchant_category_code': f'MCC_{random.randint(1000,9999)}',
                'address': fake.street_address(),
                'city': fake.city(),
                'state': fake.state(),
                'country': 'USA',
                'postal_code': fake.zipcode(),
                'is_active': random.choice([True, True, True, False]),
                'risk_score': float(np.random.beta(2,5))
            })
        return merchants

    def _calculate_fraud_probability(self, amount: float, transaction_time: datetime,
                                     location: str, merchant_category: str,
                                     user_risk_score: float, is_fraud: bool) -> float:
        probability = 0.0
        if amount > 10000:
            probability += 0.3
        elif amount > 5000:
            probability += 0.2
        elif amount > 1000:
            probability += 0.1
        if transaction_time.hour >= 22 or transaction_time.hour < 6:
            probability += 0.15
        if transaction_time.weekday() >= 5:
            probability += 0.1
        if location in self.high_risk_locations:
            probability += 0.2
        category_info = self.merchant_categories[merchant_category]
        probability += category_info['fraud_rate'] * 2
        probability += user_risk_score * 0.3
        probability += random.uniform(-0.1, 0.1)
        probability = max(0.0, min(1.0, probability))
        if is_fraud:
            probability = max(probability, 0.5)
        return probability

    def generate_transactions(self, users, cards, merchants,
                              n_transactions: int = 50000,
                              start_date: datetime = None,
                              end_date: datetime = None) -> List[Dict[str, Any]]:
        if start_date is None:
            start_date = datetime.now() - timedelta(days=90)
        if end_date is None:
            end_date = datetime.now()

        transactions = []
        last_tx_time_by_card = {}

        i = 0
        attempts = 0
        while i < n_transactions and attempts < n_transactions * 3:
            attempts += 1
            user = random.choice(users)
            user_cards = [c for c in cards if c['user_id'] == user['user_id'] and c['is_active']]
            if not user_cards:
                continue
            card = random.choice(user_cards)
            merchant = random.choice(merchants)

            transaction_time = fake.date_time_between(start_date=start_date, end_date=end_date)

            category_info = self.merchant_categories[merchant['merchant_category']]
            base_fraud_rate = category_info['fraud_rate']
            user_fraud_rate = base_fraud_rate * (1 + user['risk_score'])
            if transaction_time.hour >= 22 or transaction_time.hour < 6:
                user_fraud_rate *= 1.5
            if transaction_time.weekday() >= 5:
                user_fraud_rate *= 1.2
            if merchant['city'] in ['Miami', 'Las Vegas', 'Atlantic City']:
                user_fraud_rate *= 1.3

            is_fraud = random.random() < user_fraud_rate

            if is_fraud:
                amount = np.random.lognormal(mean=np.log(category_info['avg_amount']*2), sigma=0.8)
                amount = min(amount, 50000)
            else:
                amount = np.random.lognormal(mean=np.log(category_info['avg_amount']), sigma=0.6)
                amount = min(amount, 5000)

            if is_fraud and random.random() < 0.3:
                location = random.choice(self.high_risk_locations)
            else:
                location = random.choice(self.normal_locations)

            device_type = random.choice(self.device_types)
            device_id = f'device_{random.randint(1000,9999)}'

            prev_time = last_tx_time_by_card.get(card['card_id'])
            if prev_time:
                seconds_since = (transaction_time - prev_time).total_seconds()
            else:
                seconds_since = None
            last_tx_time_by_card[card['card_id']] = transaction_time

            fraud_probability = round(self._calculate_fraud_probability(
                amount, transaction_time, location, merchant['merchant_category'],
                user['risk_score'], is_fraud), 4)

            txn = {
                'transaction_id': f'txn_{i+1:07d}',
                'card_id': card['card_id'],
                'card_number': card['card_number'],
                'user_id': user['user_id'],
                'merchant_id': merchant['merchant_id'],
                'merchant_name': merchant['merchant_name'],
                'merchant_category': merchant['merchant_category'],
                'amount': round(float(amount),2),
                'currency': 'USD',
                'transaction_time': transaction_time.isoformat(),
                'location': location,
                'latitude': round(float(fake.latitude()),6),
                'longitude': round(float(fake.longitude()),6),
                'device_id': device_id,
                'device_type': device_type,
                'source_system': random.choice(['mobile_app','web_portal','pos_terminal','api']),
                'seconds_since_prev_tx': seconds_since,
                'is_fraud': is_fraud,
                'fraud_probability': fraud_probability,
                'created_at': transaction_time.isoformat()
            }

            transactions.append(txn)
            i += 1

        return transactions

    def generate_fraud_alerts(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        alerts = []
        for tx in transactions:
            if tx['fraud_probability'] > 0.5:
                alerts.append({
                    'alert_id': f'alert_{tx["transaction_id"]}',
                    'transaction_id': tx['transaction_id'],
                    'user_id': tx['user_id'],
                    'fraud_probability': tx['fraud_probability'],
                    'risk_level': 'high' if tx['fraud_probability'] > 0.8 else 'medium',
                    'alert_type': 'automatic_fraud_detection',
                    'description': f'Transaction flagged as { "high" if tx["fraud_probability"] > 0.8 else "medium" } risk fraud',
                    'status': random.choice(['pending','reviewed','resolved']),
                    'created_at': tx['transaction_time']
                })
        return alerts

def save_csvs(output_dir: str = 'sample-data',
              n_users: int = 1000,
              n_merchants: int = 500,
              n_transactions: int = 50000):
    os.makedirs(output_dir, exist_ok=True)
    gen = TransactionDataGenerator(seed=42)

    print("Generating users...")
    users = gen.generate_users(n_users)
    print("Generating cards...")
    cards = gen.generate_cards(users)
    print("Generating merchants...")
    merchants = gen.generate_merchants(n_merchants)
    print("Generating transactions...")
    transactions = gen.generate_transactions(users, cards, merchants, n_transactions)
    print("Generating fraud alerts...")
    alerts = gen.generate_fraud_alerts(transactions)

    tx_df = pd.DataFrame(transactions)
    points_agg = tx_df.groupby('user_id')['amount'].sum().reset_index().rename(columns={'amount':'total_spent'})
    points_agg['points'] = (points_agg['total_spent'] / 10).astype(int)
    users_df = pd.DataFrame(users)
    points_df = points_agg.merge(users_df[['user_id','risk_score']], on='user_id', how='left')
    points_df['points'] = (points_df['points'] + (points_df['risk_score'] * 10).fillna(0)).astype(int)
    points_df = points_df[['user_id','total_spent','points']]

    pd.DataFrame(users).to_csv(os.path.join(output_dir,'users.csv'), index=False)
    pd.DataFrame(cards).to_csv(os.path.join(output_dir,'cards.csv'), index=False)
    pd.DataFrame(merchants).to_csv(os.path.join(output_dir,'merchants.csv'), index=False)
    tx_df.to_csv(os.path.join(output_dir,'transactions.csv'), index=False)
    pd.DataFrame(alerts).to_csv(os.path.join(output_dir,'fraud_alerts.csv'), index=False)
    points_df.to_csv(os.path.join(output_dir,'points.csv'), index=False)

    print("Saved CSV files to", output_dir)
    print(f"Users: {len(users)} | Cards: {len(cards)} | Merchants: {len(merchants)} | Transactions: {len(transactions)} | Alerts: {len(alerts)}")

if __name__ == "__main__":
    save_csvs(output_dir='sample-data', n_users=10000, n_merchants=5000, n_transactions=500000)
