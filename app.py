import re
import streamlit as st

from services.serpapi_service import search_google_scholar
from services.ai_service import analyze_research


# --------------------------------
# Page configuration
# --------------------------------

st.set_page_config(
    page_title="ResearchRadar",
    page_icon="🔎",
    layout="wide"
)


# --------------------------------
# Session state
# --------------------------------

if "papers" not in st.session_state:
    st.session_state.papers = []

if "topic" not in st.session_state:
    st.session_state.topic = ""

if "analysis" not in st.session_state:
    st.session_state.analysis = None


# --------------------------------
# Helper functions
# --------------------------------

def get_year(paper):

    summary = paper.get(
        "publication_info",
        {}
    ).get(
        "summary",
        ""
    )

    match = re.search(
        r"\b(?:19|20)\d{2}\b",
        summary
    )

    if match:
        return int(match.group())

    return None


def get_citation_count(paper):

    value = paper.get(
        "inline_links",
        {}
    ).get(
        "cited_by",
        {}
    ).get(
        "total",
        0
    )

    try:
        return int(value)

    except (TypeError, ValueError):
        return 0


# --------------------------------
# Sidebar
# --------------------------------

with st.sidebar:

    st.title("🔎 ResearchRadar")

    st.write(
        "Your AI-powered research discovery assistant."
    )

    st.divider()

    st.subheader("📌 How it works")

    st.write(
        """
        1. Enter a research topic
        2. Search Google Scholar
        3. Explore relevant papers
        4. Understand major themes
        5. Discover possible research gaps
        """
    )

    st.divider()

    st.subheader("🛠️ Powered by")

    st.write(
        "🐍 Python\n\n"
        "🎈 Streamlit\n\n"
        "🔎 SerpApi\n\n"
        "🧠 OpenAI"
    )

    st.divider()

    st.caption(
        "ResearchRadar • Hackathon 2026"
    )


# --------------------------------
# Header
# --------------------------------

st.title("🔎 ResearchRadar")

st.write(
    "Discover, understand, and explore research "
    "using live Google Scholar data."
)

st.divider()


# --------------------------------
# Search
# --------------------------------

topic = st.text_input(
    "🔍 What would you like to research?",
    placeholder="Example: Impact of AI on education",
    value=st.session_state.topic
)

search_button = st.button(
    "Search Research",
    type="primary"
)


# --------------------------------
# Search process
# --------------------------------

if search_button:

    if not topic.strip():

        st.warning(
            "Please enter a research topic."
        )

    else:

        # ----------------------------
        # Search Google Scholar
        # ----------------------------

        try:

            with st.spinner(
                "🔎 Searching Google Scholar..."
            ):

                results = search_google_scholar(
                    topic
                )

        except Exception:

            st.error(
                "❌ We couldn't retrieve research papers right now."
            )

            st.caption(
                "Please check your internet connection or try again."
            )

            st.stop()


        papers = results.get(
            "organic_results",
            []
        )


        # Save papers and topic
        st.session_state.papers = papers
        st.session_state.topic = topic


        # ----------------------------
        # AI analysis
        # ----------------------------

        if papers:

            try:

                with st.spinner(
                    "🧠 Analyzing the research..."
                ):

                    analysis = analyze_research(
                        papers,
                        topic
                    )

                st.session_state.analysis = analysis

            except Exception:

                st.session_state.analysis = None

                st.error(
                    "❌ We couldn't generate the AI research analysis."
                )

                st.caption(
                    "The research papers were retrieved successfully, "
                    "but the AI analysis could not be completed."
                )

        else:

            st.session_state.analysis = None


# --------------------------------
# Load saved results
# --------------------------------

papers = st.session_state.papers
analysis = st.session_state.analysis


# --------------------------------
# Display results
# --------------------------------

if papers:

    st.success(
        f"Found {len(papers)} research papers."
    )


    # --------------------------------
    # Paper filtering and sorting
    # --------------------------------

    available_years = sorted(
        {
            get_year(paper)
            for paper in papers
            if get_year(paper)
        },
        reverse=True
    )


    col1, col2 = st.columns(2)


    with col1:

        selected_year = st.selectbox(
            "📅 Filter by publication year",
            ["All years"] + available_years
        )


    with col2:

        sort_option = st.selectbox(
            "🔃 Sort papers by",
            [
                "Relevance",
                "Most cited",
                "Newest",
                "Oldest"
            ]
        )


    # --------------------------------
    # Create display copy
    # --------------------------------

    display_papers = papers.copy()


    # --------------------------------
    # Filter by year
    # --------------------------------

    if selected_year != "All years":

        display_papers = [
            paper
            for paper in display_papers
            if get_year(paper) == selected_year
        ]


    # --------------------------------
    # Sort papers
    # --------------------------------

    if sort_option == "Most cited":

        display_papers.sort(
            key=get_citation_count,
            reverse=True
        )

    elif sort_option == "Newest":

        display_papers.sort(
            key=lambda paper: get_year(paper) or 0,
            reverse=True
        )

    elif sort_option == "Oldest":

        display_papers.sort(
            key=lambda paper: get_year(paper) or 9999
        )


    # --------------------------------
    # Research statistics
    # --------------------------------

    years = []


    for paper in papers:

        publication_info = paper.get(
            "publication_info",
            {}
        )

        summary = publication_info.get(
            "summary",
            ""
        )

        matches = re.findall(
            r"\b(?:19|20)\d{2}\b",
            summary
        )

        for year in matches:

            years.append(
                int(year)
            )


    if years:

        oldest_year = min(years)
        newest_year = max(years)

    else:

        oldest_year = "N/A"
        newest_year = "N/A"


    # --------------------------------
    # Statistics
    # --------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "📚 Papers Found",
            len(papers)
        )


    with col2:

        st.metric(
            "📅 Research Period",
            f"{oldest_year} – {newest_year}"
        )


    with col3:

        st.metric(
            "🔗 Sources",
            len(
                [
                    paper
                    for paper in papers
                    if paper.get("link")
                ]
            )
        )


    # --------------------------------
    # Publication trend
    # --------------------------------

    if years:

        year_counts = {}


        for year in years:

            if year in year_counts:

                year_counts[year] += 1

            else:

                year_counts[year] = 1


        sorted_years = sorted(
            year_counts.keys()
        )


        chart_data = {
            "Year": sorted_years,
            "Papers": [
                year_counts[year]
                for year in sorted_years
            ]
        }


        st.subheader(
            "📈 Publication Trend"
        )

        st.caption(
            "Publication-year distribution of the papers "
            "retrieved for the current research query."
        )


        st.line_chart(
            chart_data,
            x="Year",
            y="Papers"
        )


    # --------------------------------
    # Tabs
    # --------------------------------

    tab1, tab2, tab3 = st.tabs(
        [
            "🧠 Research Insights",
            "📚 Research Papers",
            "💡 Research Gaps"
        ]
    )


    # --------------------------------
    # TAB 1 — AI Insights
    # --------------------------------

    with tab1:

        st.subheader(
            "🧠 Research Insights"
        )

        st.caption(
            "AI-generated synthesis based on the "
            "retrieved Google Scholar results."
        )


        if analysis:

            st.markdown(
                analysis
            )

        else:

            st.info(
                "AI analysis is currently unavailable. "
                "You can still explore the retrieved research papers."
            )


    # --------------------------------
    # TAB 2 — Research Papers
    # --------------------------------

    with tab2:

        st.subheader(
            "📚 Retrieved Research Papers"
        )

        st.caption(
            f"Showing {len(display_papers)} "
            f"of {len(papers)} retrieved papers."
        )


        if display_papers:

            for i, paper in enumerate(
                display_papers,
                start=1
            ):

                title = paper.get(
                    "title",
                    "Untitled paper"
                )


                publication_info = paper.get(
                    "publication_info",
                    {}
                )


                summary = publication_info.get(
                    "summary",
                    "Publication information unavailable."
                )


                snippet = paper.get(
                    "snippet",
                    "No description available."
                )


                link = paper.get(
                    "link"
                )


                citation_count = get_citation_count(
                    paper
                )


                year = get_year(
                    paper
                )


                with st.container(
                    border=True
                ):

                    st.markdown(
                        f"### {i}. {title}"
                    )


                    col1, col2 = st.columns(2)


                    with col1:

                        st.write(
                            f"👥 **{summary}**"
                        )


                    with col2:

                        st.write(
                            f"📅 **Year:** "
                            f"{year or 'N/A'}"
                        )

                        st.write(
                            f"📚 **Citations:** "
                            f"{citation_count}"
                        )


                    st.write(
                        f"📝 {snippet}"
                    )


                    if link:

                        st.link_button(
                            "🔗 Read Paper",
                            link
                        )

        else:

            st.info(
                "No papers match the selected publication year."
            )


    # --------------------------------
    # TAB 3 — Research Gaps
    # --------------------------------

    with tab3:

        st.subheader(
            "💡 Potential Research Directions"
        )

        st.write(
            "ResearchRadar identifies possible research "
            "directions from the retrieved literature. "
            "These are suggestions, not confirmed gaps."
        )


        if analysis and "## Research Gaps" in analysis:

            gaps = analysis.split(
                "## Research Gaps",
                1
            )[1]


            if "## Possible Research Questions" in gaps:

                gaps = gaps.split(
                    "## Possible Research Questions",
                    1
                )[0]


            st.markdown(
                gaps
            )

        else:

            st.info(
                "Research gap information was not returned "
                "for this search."
            )


# --------------------------------
# No search performed yet
# --------------------------------

elif not search_button:

    if not papers:

        st.info(
            "👆 Enter a research topic above and click "
            "**Search Research** to get started."
        )


# --------------------------------
# Search returned no papers
# --------------------------------

if search_button and not papers:

    st.warning(
        "No research papers were found for this topic."
    )