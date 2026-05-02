import streamlit as st
from datetime import datetime
from config.settings import settings
from src.agent import Agent
from src.storage import save_results

# --- Page config ---
st.set_page_config(page_title="PriceScout", page_icon="🔍", layout="wide")
st.title("🔍 PriceScout AI")
st.caption("Autonomous competitor price monitoring")

# --- Sidebar: Inputs ---
with st.sidebar:
    st.header("⚙️ Settings")
    product = st.text_input("Product name", placeholder="e.g. Sony WH-1000XM5")

    mode = st.radio("Mode", ["Autonomous", "Targeted URLs"])

    urls_input = ""
    max_results = 3

    if mode == "Autonomous":
        max_results = st.slider("Max results", 1, 5, 3)
    else:
        urls_input = st.text_area(
            "Competitors & URLs",
            placeholder="Amazon:https://amazon.com/...\nFnac:https://fnac.com/...",
            help="One per line, format: CompetitorName:https://url"
        )

    run = st.button("🚀 Run PriceScout", use_container_width=True, type="primary")

# --- Main: Run agent ---
if run:
    if not product.strip():
        st.warning("Please enter a product name.")
    else:
        agent = Agent()

        if mode == "Targeted URLs":
            # Parse exactly like main.py does
            urls_to_process = []
            for line in urls_input.strip().splitlines():
                parts = line.split(":", 1)
                if len(parts) == 2:
                    urls_to_process.append({
                        "competitor": parts[0].strip(),
                        "url": parts[1].strip()
                    })
                else:
                    st.warning(f"Skipping invalid line: `{line}` — use format `Name:https://...`")

            if not urls_to_process:
                st.error("No valid URLs found. Please check your input format.")
                st.stop()

            with st.spinner(f"Extracting prices from {len(urls_to_process)} URL(s)..."):
                results = agent.run_multi_url_search(product, urls_to_process)
        else:
            with st.spinner(f"Searching the web autonomously for '{product}'..."):
                results = agent.run_autonomous_search(product, max_results=max_results)

        # --- Display results ---
        if results:
            # Save exactly like main.py does
            timestamp = datetime.now().strftime("%Y%md_%H%M%S")
            filename = f"price_results_{timestamp}.json"
            save_results(results, filename)

            st.success(f"✅ {len(results)} result(s) found — saved to `{filename}`")

            # Summary metric cards
            cols = st.columns(len(results))
            for i, r in enumerate(results):
                with cols[i]:
                    st.metric(
                        label=r.competitor,
                        value=f"{r.price} {r.currency}" if r.price else "N/A",
                        delta=r.status
                    )

            # Full table
            st.subheader("📋 Full Results")
            st.dataframe(
                [r.model_dump() for r in results],
                use_container_width=True
            )

            # Raw JSON
            with st.expander("🗂 Raw JSON"):
                st.json([r.model_dump() for r in results])
        else:
            st.error("No results could be extracted. Try a different product or check your API keys.")