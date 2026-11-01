
import streamlit as st
import matplotlib.pyplot as plt

1
# SVG KPI Icons
KPI_ICONS = {
    "revenue": """
    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28"
         viewBox="0 0 24 24" fill="none" stroke="#14B8A6"
         stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="6" width="18" height="14" rx="2"/>
        <path d="M3 10h18M7 6V4h10v2"/>
        <circle cx="12" cy="15" r="2.5"/>
    </svg>
    """,

    "orders": """
    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28"
         viewBox="0 0 24 24" fill="none" stroke="#14B8A6"
         stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="9" cy="21" r="1"/>
        <circle cx="19" cy="21" r="1"/>
        <path d="M1 1h4l2.7 13.4a2 2 0 002 1.6h9.7a2 2 0 002-1.6L23 6H6"/>
    </svg>
    """,

    "customers": """
    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28"
         viewBox="0 0 24 24" fill="none" stroke="#14B8A6"
         stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="9" cy="8" r="3.5"/>
        <path d="M2 20v-2a7 7 0 0114 0v2z"/>
        <path d="M16 4.8a3.5 3.5 0 010 6.5M18 14a5.5 5.5 0 014 5.3V20"/>
    </svg>
    """,

    "sellers": """
    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28"
         viewBox="0 0 24 24" fill="none" stroke="#14B8A6"
         stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 10v11h18V10"/>
        <path d="M2 10l2-7h16l2 7"/>
        <path d="M2 10a3 3 0 006 0 3 3 0 006 0 3 3 0 006 0 3 3 0 002-3"/>
        <path d="M9 21v-6h6v6"/>
    </svg>
    """,

    "aov": """
    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28"
         viewBox="0 0 24 24" fill="none" stroke="#14B8A6"
         stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 3v18h18"/>
        <rect x="6" y="12" width="3.5" height="6" rx="0.5"/>
        <rect x="11" y="8" width="3.5" height="10" rx="0.5"/>
        <rect x="16" y="4" width="3.5" height="14" rx="0.5"/>
    </svg>
    """,

    "reviews": """
    <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28"
         viewBox="0 0 24 24" fill="none" stroke="#14B8A6"
         stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-3-5.6 3 1.1-6.2L3 9.6l6.2-.9L12 3z"/>
    </svg>
    """
}
def kpi_card(icon, label, value):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">
            <span class="kpi-icon">{icon}</span>
            <span>{label}</span>
        </div>
        <div class="kpi-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def money_short(value):
    if value >= 1_000_000:
        return f"R${value / 1_000_000:.2f}M"
    if value >= 100_000:
        return f"R${value / 100_000:.2f}L"
    return f"R${value:,.0f}"

def show_chart(chartType,Xaxis,Yaxis,Xlabel,Ylabel,Title,figsize=(10,5),color="#153653",df=""):
    if chartType=="Line":
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(
            Xaxis,
            Yaxis,
            marker="o",
            linestyle="-",
            color=color
        )
        ax.set_xlabel(Xlabel)
        ax.set_ylabel(Ylabel)
        ax.set_title(Title)
        ax.tick_params(colors='#486581')
        ax.xaxis.label.set_color('#486581')
        ax.yaxis.label.set_color('#486581')
        ax.grid(axis="y", color='#E8EEF5',linestyle="--", alpha=0.4)
        st.pyplot(fig)
    elif chartType=="Bar":
        fig, ax = plt.subplots(figsize=figsize)
        ax.bar(
            Xaxis,
            Yaxis,
            width=0.6,
            color=color
        )
        ax.set_xlabel(Xlabel)
        ax.set_ylabel(Ylabel)
        ax.set_title(Title)
        ax.tick_params(colors='#486581')
        ax.tick_params(axis="x", rotation=45)
        ax.xaxis.label.set_color('#486581')
        ax.yaxis.label.set_color('#486581')
        ax.grid(axis="y",color='#E8EEF5', linestyle="--", alpha=0.4)
        st.pyplot(fig)
    elif chartType=="Scatter":
        fig, ax = plt.subplots(figsize=figsize)
        ax.scatter(
            Xaxis,
            Yaxis,
            color=color,
            alpha=0.7,
            s=50
        )
        ax.set_xlabel(Xlabel)
        ax.set_ylabel(Ylabel)
        ax.tick_params(colors="#486581")
        ax.xaxis.label.set_color('#486581')
        ax.yaxis.label.set_color('#486581')
        ax.grid(
            axis="y",
            color="#E8EEF5",
            linestyle="--",
            alpha=0.4
        )
        st.pyplot(fig)
    elif chartType=="Donut":
        fig, ax = plt.subplots(figsize=figsize)

        wedges, texts, autotexts = ax.pie(
            Yaxis,
            colors=color,
            startangle=90,
            counterclock=False,
            autopct="%1.1f%%",
            pctdistance=0.78,
            textprops={"color": "#FFFFFF", "fontsize": 10},
            wedgeprops={
                "width": 0.42,
                "edgecolor": "white",
                "linewidth": 2
            }
        )

        ax.legend(
            wedges,
            Xaxis,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.08),
            ncol=2,
            frameon=False,
            fontsize=9
        )

        ax.set_title(
            Title,
            color="#243B53",
            fontsize=7,
            fontweight="bold",
            pad=12
        )

        ax.axis("equal")
        fig.tight_layout()

        st.pyplot(fig, use_container_width=True)

    elif chartType=="Barh":
        fig, ax = plt.subplots(figsize=figsize)
        ax.barh(
            y=Xaxis,
            width=Yaxis,
            color=color
        )
        ax.set_xlabel(Xlabel)
        ax.set_ylabel(Ylabel)
        ax.set_title(Title)
        ax.tick_params(colors='#486581')
        ax.xaxis.label.set_color('#486581')
        ax.yaxis.label.set_color('#486581')
        st.pyplot(fig)
    elif chartType=="PivotBar":

        fig, ax = plt.subplots(figsize=figsize)
        df.plot(
            kind="bar",
            stacked=True,
            ax=ax,
            color=color,
            colormap="Set2"
        )

        ax.set_title(Title)
        ax.set_xlabel(Xlabel)
        ax.set_ylabel(Ylabel)

        ax.tick_params(axis="x", rotation=0)
        ax.legend(title="Review Score")

        ax.grid(axis="y", alpha=0.2)
        ax.spines[["top", "right"]].set_visible(False)

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    elif chartType=="Histogram":
        fig, ax = plt.subplots(figsize=figsize)

        ax.hist(
            Yaxis,
            bins=10,
            color="#5B9BD5",
            edgecolor="white",

        )

        ax.set_xlabel(Xlabel, color="#486581", fontsize=11)
        ax.set_ylabel(Ylabel, color="#486581", fontsize=11)

        ax.set_title(Title)

        ax.tick_params(colors="#486581")
        ax.grid(
            axis="y",
            color="#E8EEF5",
            linestyle="--",
            alpha=0.8
        )
        ax.set_axisbelow(True)
        fig.tight_layout()
        st.pyplot(fig)

