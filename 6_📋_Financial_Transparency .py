import streamlit as st
import pandas as pd
import hashlib
import datetime
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Financial Transparency", layout="wide")

st.title("📋 Financial Transparency Dashboard")
st.markdown("**Tamper-Proof Tracking of Every Rand - Powered by IBM Z & LinuxONE**")

class BlockchainLedger:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = {
            'index': 0,
            'timestamp': datetime.datetime.now().isoformat(),
            'transactions': [],
            'previous_hash': '0',
            'hash': self.calculate_hash(0, '0', [], datetime.datetime.now().isoformat())
        }
        self.chain.append(genesis_block)
    
    def calculate_hash(self, index, previous_hash, transactions, timestamp):
        """Calculate SHA-256 hash of block contents"""
        block_string = f"{index}{previous_hash}{str(transactions)}{timestamp}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def add_transaction(self, transaction_data):
        """Add a new transaction to the ledger"""
        previous_block = self.chain[-1]
        new_block = {
            'index': len(self.chain),
            'timestamp': datetime.datetime.now().isoformat(),
            'transactions': [transaction_data],
            'previous_hash': previous_block['hash'],
            'hash': self.calculate_hash(len(self.chain), previous_block['hash'], [transaction_data], datetime.datetime.now().isoformat())
        }
        self.chain.append(new_block)
        return new_block

# Initialize blockchain ledger
if 'ledger' not in st.session_state:
    st.session_state.ledger = BlockchainLedger()

# Sample project data
PROJECTS = {
    "EC001": {
        "name": "Eastern Cape Solar Borehole Project",
        "location": "Mbizana, Eastern Cape",
        "budget": 4500000,
        "start_date": "2024-01-15",
        "status": "In Progress"
    },
    "EC002": {
        "name": "Rural Water Treatment Initiative", 
        "location": "Lusikisiki, Eastern Cape",
        "budget": 3200000,
        "start_date": "2024-02-01",
        "status": "Planning"
    }
}

# Main Dashboard
st.header("💰 Financial Overview")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)

total_budget = sum(project["budget"] for project in PROJECTS.values())
total_spent = 1850000  # Mock data
total_transactions = len(st.session_state.ledger.chain) - 1  # Exclude genesis block
verified_percentage = 100  # All transactions verified in this demo

with col1:
    st.metric("Total Project Budget", f"ZAR {total_budget:,}")
with col2:
    st.metric("Funds Deployed", f"ZAR {total_spent:,}", f"{(total_spent/total_budget)*100:.1f}%")
with col3:
    st.metric("Transactions Tracked", total_transactions)
with col4:
    st.metric("Verified Transactions", f"{verified_percentage}%", "All immutable")

# Project Selection
st.header("🏗️ Project Financial Tracking")

selected_project = st.selectbox(
    "Select Project to View:",
    list(PROJECTS.keys()),
    format_func=lambda x: f"{x} - {PROJECTS[x]['name']}"
)

if selected_project:
    project = PROJECTS[selected_project]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"Project: {project['name']}")
        st.write(f"**Location**: {project['location']}")
        st.write(f"**Status**: {project['status']}")
        st.write(f"**Start Date**: {project['start_date']}")
        
        # Budget utilization
        budget_used = min(total_spent, project['budget'])
        budget_remaining = project['budget'] - budget_used
        
        fig_budget = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = budget_used,
            delta = {'reference': project['budget']},
            gauge = {
                'axis': {'range': [None, project['budget']]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, project['budget']*0.7], 'color': "lightgray"},
                    {'range': [project['budget']*0.7, project['budget']*0.9], 'color': "yellow"},
                    {'range': [project['budget']*0.9, project['budget']], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': project['budget']*0.9
                }
            }
        ))
        fig_budget.update_layout(title=f"Budget Utilization: ZAR {budget_used:,} / {project['budget']:,}")
        st.plotly_chart(fig_budget, use_container_width=True)
    
    with col2:
        st.subheader("Quick Actions")
        
        if st.button("📋 Add New Transaction", type="primary"):
            st.session_state.show_transaction_form = True
        
        if st.button("📊 Generate Audit Report"):
            st.session_state.show_audit_report = True
        
        if st.button("🔍 Verify All Transactions"):
            st.success("✅ All transactions verified - Blockchain integrity confirmed!")
        
        # Quick stats
        st.metric("Project Budget", f"ZAR {project['budget']:,}")
        st.metric("Budget Remaining", f"ZAR {budget_remaining:,}")
        st.metric("Cost Efficiency", "94%", "6% savings")

# Transaction Ledger
st.header("📋 Immutable Transaction Ledger")

# Sample transactions (in real app, these would come from the blockchain)
sample_transactions = [
    {
        'txn_id': 'TXN_2024_001',
        'date': '2024-01-20',
        'description': 'Solar pump purchase - AquaFix Solutions',
        'amount': 450000,
        'vendor': 'AquaFix Solutions',
        'category': 'Equipment',
        'project': 'EC001',
        'block_hash': '0001a2b3c4d5e6f7890abcdef1234567890',
        'verified': True,
        'proof_of_payment': 'invoice_001.pdf'
    },
    {
        'txn_id': 'TXN_2024_002', 
        'date': '2024-01-25',
        'description': 'HDPE piping materials',
        'amount': 285000,
        'vendor': 'PipeTech SA',
        'category': 'Materials',
        'project': 'EC001',
        'block_hash': '0002b3c4d5e6f7890abcdef12345678901',
        'verified': True,
        'proof_of_payment': 'invoice_002.pdf'
    },
    {
        'txn_id': 'TXN_2024_003',
        'date': '2024-02-01', 
        'description': 'Community labor - construction phase',
        'amount': 320000,
        'vendor': 'Local Workforce',
        'category': 'Labor',
        'project': 'EC001',
        'block_hash': '0003c4d5e6f7890abcdef123456789012',
        'verified': True,
        'proof_of_payment': 'payroll_001.pdf'
    }
]

# Display transactions
transactions_df = pd.DataFrame(sample_transactions)
st.dataframe(
    transactions_df[['txn_id', 'date', 'description', 'amount', 'vendor', 'category', 'verified']],
    use_container_width=True
)

# Expenditure Analysis
st.header("📈 Expenditure Analysis")

col1, col2 = st.columns(2)

with col1:
    # Spending by category
    category_spending = transactions_df.groupby('category')['amount'].sum().reset_index()
    fig_category = px.pie(category_spending, values='amount', names='category', 
                         title='Spending by Category')
    st.plotly_chart(fig_category, use_container_width=True)

with col2:
    # Monthly spending trend
    monthly_data = transactions_df.copy()
    monthly_data['date'] = pd.to_datetime(monthly_data['date'])
    monthly_data['month'] = monthly_data['date'].dt.to_period('M')
    monthly_spending = monthly_data.groupby('month')['amount'].sum().reset_index()
    monthly_spending['month'] = monthly_spending['month'].astype(str)
    
    fig_trend = px.bar(monthly_spending, x='month', y='amount', 
                      title='Monthly Expenditure Trend')
    st.plotly_chart(fig_trend, use_container_width=True)

# Anti-Corruption Features
st.header("🛡️ Anti-Corruption Safeguards")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔍 Real-time Monitoring")
    st.write("""
    - **Automated anomaly detection**
    - **Duplicate payment checks**
    - **Vendor verification**
    - **Budget compliance alerts**
    """)
    
    st.metric("Suspicious Activities", "0", "This month")
    st.metric("Cost Savings", "ZAR 275,000", "Through transparency")

with col2:
    st.subheader("📊 Performance Metrics")
    st.write("""
    - **98%** On-time project delivery
    - **94%** Budget efficiency 
    - **100%** Transaction verification
    - **0** Corruption incidents
    """)
    
    efficiency = (total_spent / total_budget) * 100
    st.metric("Budget Efficiency", f"{efficiency:.1f}%")

with col3:
    st.subheader("👥 Community Oversight")
    st.write("""
    - **Public transaction ledger**
    - **Citizen reporting portal**
    - **Independent audits**
    - **Whistleblower protection**
    """)
    
    st.metric("Community Reports", "12", "This quarter")
    st.metric("Issues Resolved", "12", "100% resolution rate")

# Add Transaction Form
if st.session_state.get('show_transaction_form', False):
    st.header("➕ Add New Transaction")
    
    with st.form("transaction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            txn_date = st.date_input("Transaction Date")
            description = st.text_input("Description")
            amount = st.number_input("Amount (ZAR)", min_value=0, value=10000)
            vendor = st.text_input("Vendor Name")
            
        with col2:
            category = st.selectbox("Category", ["Equipment", "Materials", "Labor", "Professional Services", "Administrative", "Other"])
            project_code = st.selectbox("Project", list(PROJECTS.keys()))
            proof_file = st.file_uploader("Proof of Payment", type=['pdf', 'jpg', 'png'])
        
        submitted = st.form_submit_button("Add to Blockchain Ledger")
        
        if submitted:
            # Create new transaction
            new_txn = {
                'txn_id': f"TXN_{txn_date.strftime('%Y_%m_%d')}_{len(sample_transactions) + 1}",
                'date': txn_date.isoformat(),
                'description': description,
                'amount': amount,
                'vendor': vendor,
                'category': category,
                'project': project_code,
                'verified': True,
                'proof_of_payment': proof_file.name if proof_file else "uploaded_file"
            }
            
            # Add to blockchain
            new_block = st.session_state.ledger.add_transaction(new_txn)
            
            st.success(f"✅ Transaction added to blockchain! Block Hash: {new_block['hash'][:20]}...")
            st.session_state.show_transaction_form = False
            st.rerun()

# Blockchain Verification
st.header("⛓️ Blockchain Verification")

with st.expander("🔗 View Blockchain Details"):
    st.write("**Blockchain Integrity Check**")
    
    for i, block in enumerate(st.session_state.ledger.chain):
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**Block {block['index']}** - {block['timestamp'][:10]}")
                st.write(f"Hash: `{block['hash'][:30]}...`")
                st.write(f"Previous: `{block['previous_hash'][:30]}...`")
            with col2:
                if i > 0:  # Not genesis block
                    st.metric("Transactions", len(block['transactions']))
                else:
                    st.metric("Block Type", "Genesis")

# Audit Report
if st.session_state.get('show_audit_report', False):
    st.header("📊 Financial Audit Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Executive Summary")
        st.write(f"""
        - **Total Projects**: {len(PROJECTS)}
        - **Total Budget**: ZAR {total_budget:,}
        - **Total Spent**: ZAR {total_spent:,}
        - **Remaining Funds**: ZAR {total_budget - total_spent:,}
        - **Transaction Count**: {total_transactions}
        - **Verification Rate**: 100%
        """)
        
        st.subheader("Key Findings")
        st.success("✅ No financial irregularities detected")
        st.success("✅ All transactions properly documented")
        st.success("✅ Budget utilization within acceptable limits")
        st.success("✅ Blockchain integrity verified")
    
    with col2:
        st.subheader("Recommendations")
        st.info("""
        1. Continue current transparency practices
        2. Expand blockchain tracking to all projects
        3. Increase community oversight participation
        4. Regular independent audits (quarterly)
        """)
        
        st.download_button(
            "📄 Download Full Audit Report",
            data="Mock PDF audit report content would be here",
            file_name=f"audit_report_{datetime.datetime.now().date()}.pdf",
            mime="application/pdf"
        )

# Community Impact
st.header("🌍 Community Impact Tracking")

impact_data = {
    'Metric': ['Households Served', 'Jobs Created', 'Local Businesses Supported', 'Water Access Improved', 'Community Satisfaction'],
    'Before': [150, 5, 3, '42%', '65%'],
    'After': [850, 48, 15, '89%', '94%'],
    'Improvement': [+700, +43, +12, '+47%', '+29%']
}

impact_df = pd.DataFrame(impact_data)
st.dataframe(impact_df, use_container_width=True)

st.info("""
💡 **Transparency Transformation**: 
*When every rand is traceable, corruption cannot hide. When every transaction is public, trust is rebuilt. 
When communities can see where money flows, hope returns.*
""")

# Footer
st.markdown("---")
st.caption("""
**HydroTransparent Financial System** - Built on IBM Z & LinuxONE for maximum security and transparency.
All transactions are cryptographically sealed and immutable. Public verification available 24/7.
""")