import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Stock Prediction App", layout="wide")

# Custom CSS for colorful design
st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        h1 {
            color: #ffffff;
            text-align: center;
            font-size: 3em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Stock Price Prediction Website")

# Input section with nice styling
col1, col2 = st.columns([3, 1])
with col1:
    stock = st.text_input("🔍 Enter Stock Symbol", placeholder="E.g., AAPL, TSLA, TCS.NS").upper()

if stock:
    try:
        data = yf.download(stock, start="2020-01-01", progress=False)
        
        if data.empty:
            st.error(f"❌ No data found for '{stock}'. Check the symbol and try again.")
        else:
            # Get stock info
            ticker = yf.Ticker(stock)
            info = ticker.info
            
            # Display key metrics
            st.markdown("---")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("💰 Current Price", f"${data['Close'].iloc[-1]:.2f}", 
                         delta=f"${data['Close'].iloc[-1] - data['Close'].iloc[-5]:.2f}")
            
            with col2:
                st.metric("📈 52 Week High", f"${data['Close'].max():.2f}")
            
            with col3:
                st.metric("📉 52 Week Low", f"${data['Close'].min():.2f}")
            
            with col4:
                change_percent = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
                st.metric("📊 Change %", f"{change_percent:.2f}%")
            
            st.markdown("---")
            
            # Colorful price chart with Plotly
            st.subheader("📊 Closing Price Chart")
            fig_price = go.Figure()
            fig_price.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.3)',
                line=dict(color='#667eea', width=3),
                name='Close Price'
            ))
            fig_price.update_layout(
                title=f"{stock} - Price Trend",
                xaxis_title="Date",
                yaxis_title="Price ($)",
                hovermode='x unified',
                template='plotly_dark',
                height=400,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig_price, use_container_width=True)
            
            # Volume chart
            st.subheader("📈 Trading Volume")
            fig_volume = go.Figure()
            colors = ['#667eea' if data['Close'].iloc[i] >= data['Close'].iloc[i-1] else '#ff6b6b' 
                     for i in range(1, len(data))]
            colors = ['#667eea'] + colors
            
            fig_volume.add_trace(go.Bar(
                x=data.index,
                y=data['Volume'],
                marker=dict(color=colors),
                name='Volume'
            ))
            fig_volume.update_layout(
                title=f"{stock} - Trading Volume",
                xaxis_title="Date",
                yaxis_title="Volume",
                hovermode='x unified',
                template='plotly_dark',
                height=300,
                showlegend=False,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig_volume, use_container_width=True)
            
            # Moving averages
            st.subheader("📉 Moving Averages")
            data['MA20'] = data['Close'].rolling(window=20).mean()
            data['MA50'] = data['Close'].rolling(window=50).mean()
            
            fig_ma = go.Figure()
            fig_ma.add_trace(go.Scatter(
                x=data.index, y=data['Close'],
                line=dict(color='#667eea', width=2),
                name='Close Price'
            ))
            fig_ma.add_trace(go.Scatter(
                x=data.index, y=data['MA20'],
                line=dict(color='#f59e0b', width=2, dash='dash'),
                name='20-Day MA'
            ))
            fig_ma.add_trace(go.Scatter(
                x=data.index, y=data['MA50'],
                line=dict(color='#ef4444', width=2, dash='dash'),
                name='50-Day MA'
            ))
            fig_ma.update_layout(
                title=f"{stock} - Price with Moving Averages",
                xaxis_title="Date",
                yaxis_title="Price ($)",
                hovermode='x unified',
                template='plotly_dark',
                height=400,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            st.plotly_chart(fig_ma, use_container_width=True)
            
            # Recent data table
            with st.expander("📋 View Recent Data"):
                st.dataframe(data.tail(20), use_container_width=True)
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")