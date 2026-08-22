import streamlit as st
import networkx as nx

from src.navigation import find_route
from src.rag import search_hospital_information
from src.llm import generate_answer


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="CareCompass",
    page_icon="🏥",
    layout="wide"
)


# ==================================================
# SESSION STATE
# ==================================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# ==================================================
# HEADER
# ==================================================

st.title("🏥 CareCompass")

st.subheader(
    "Intelligent Hospital Navigation and Query Assistant"
)

st.write(
    "Navigate through the hospital and ask questions "
    "about doctors, treatments, departments, facilities, "
    "timings, emergency services and hospital policies."
)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🏥 CareCompass")

st.sidebar.write(
    "Your intelligent hospital assistant"
)

st.sidebar.divider()


# ==================================================
# CLEAR CHAT
# ==================================================

if st.sidebar.button(
    "🗑️ Clear Chat",
    use_container_width=True
):

    st.session_state.chat_history = []

    st.rerun()


# ==================================================
# EMERGENCY ASSISTANCE
# ==================================================

st.divider()

st.header("🚨 Emergency Assistance")

st.warning(
    "If this is a medical emergency, please seek "
    "immediate assistance from hospital staff or "
    "emergency medical services."
)


emergency_col1, emergency_col2 = st.columns(2)


# ==================================================
# EMERGENCY INFORMATION
# ==================================================

with emergency_col1:

    st.subheader(
        "🚑 Emergency Department"
    )

    st.write(
        "**Location:** Ground Floor, East Wing"
    )

    st.write(
        "**Availability:** 24 hours / 7 days"
    )

    st.write(
        "**Emergency Contact:** 0866-2222111"
    )


# ==================================================
# EMERGENCY CONTACT
# ==================================================

with emergency_col2:

    st.subheader(
        "📞 Emergency Contact"
    )

    st.write(
        "For this demonstration, CareCompass uses "
        "the published Vijayawada hospital contact "
        "number mentioned in the emergency dataset."
    )

    st.link_button(
        "📞 Call Emergency Department",
        "tel:+918662222111",
        use_container_width=True
    )


# ==================================================
# FIND EMERGENCY ROUTE
# ==================================================

if st.button(
    "🚨 FIND EMERGENCY DEPARTMENT",
    use_container_width=True
):

    try:

        route = find_route(
            "Main Entrance",
            "Emergency"
        )

        st.success(
            "Emergency route found!"
        )

        st.subheader(
            "🧭 Route to Emergency Department"
        )

        for i, location in enumerate(route):

            if i == 0:

                st.write(
                    f"🟢 **Start:** {location}"
                )

            elif i == len(route) - 1:

                st.write(
                    f"🔴 **Emergency:** {location}"
                )

            else:

                st.write(
                    f"⬇️ **Step {i}:** {location}"
                )

        st.info(
            " → ".join(route)
        )

    except nx.NetworkXNoPath:

        st.error(
            "No emergency route was found."
        )

    except nx.NodeNotFound:

        st.error(
            "Emergency location is not present "
            "in the hospital map."
        )


# ==================================================
# HOSPITAL NAVIGATION
# ==================================================

st.divider()

st.header(
    "🧭 Hospital Navigation"
)

st.write(
    "Select your current location and destination "
    "to find the shortest route."
)


locations = [

    "Main Entrance",

    "Emergency Entrance",

    "Reception",

    "Pharmacy",

    "Emergency",

    "Lift",

    "First Floor",

    "Orthopedics",

    "Laboratory",

    "Second Floor",

    "Cardiology",

    "Neurology"
]


col1, col2 = st.columns(2)


with col1:

    source = st.selectbox(
        "📍 Current Location",
        locations
    )


with col2:

    destination = st.selectbox(
        "🎯 Destination",
        locations,
        index=9
    )


if st.button(
    "🧭 Find Route",
    use_container_width=True
):

    if source == destination:

        st.warning(
            "Current location and destination "
            "are the same."
        )

    else:

        try:

            route = find_route(
                source,
                destination
            )

            st.success(
                "✅ Route found!"
            )

            st.subheader(
                "📍 Recommended Route"
            )

            for i, location in enumerate(route):

                if i == 0:

                    st.write(
                        f"🟢 **Start:** {location}"
                    )

                elif i == len(route) - 1:

                    st.write(
                        f"🔴 **Destination:** {location}"
                    )

                else:

                    st.write(
                        f"⬇️ **Step {i}:** {location}"
                    )

            st.info(
                " → ".join(route)
            )

        except nx.NetworkXNoPath:

            st.error(
                "❌ No route exists between "
                "these locations."
            )

        except nx.NodeNotFound:

            st.error(
                "❌ Location not found in hospital map."
            )


# ==================================================
# HOSPITAL INFORMATION
# ==================================================

st.divider()

st.header(
    "💬 Hospital Information"
)

st.write(
    "Ask questions about doctors, treatments, "
    "departments, facilities, timings, emergency "
    "services and hospital policies."
)


question = st.text_input(
    "Ask your question",

    placeholder=(
        "Example: Who is the cardiologist?"
    )
)


# ==================================================
# ASK CARECOMPASS
# ==================================================

if st.button(
    "🤖 Ask CareCompass",
    use_container_width=True
):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            with st.spinner(
                "🔍 Searching hospital information..."
            ):

                context = search_hospital_information(
                    question
                )

            with st.spinner(
                "🤖 Generating answer..."
            ):

                answer = generate_answer(
                    question,
                    context
                )

            st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": answer
                }
            )

        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )


# ==================================================
# CHAT HISTORY
# ==================================================

if st.session_state.chat_history:

    st.divider()

    st.subheader(
        "💬 Conversation"
    )

    for chat in reversed(
        st.session_state.chat_history
    ):

        st.markdown(
            f"**👤 You:** {chat['question']}"
        )

        st.markdown(
            f"**🤖 CareCompass:** {chat['answer']}"
        )

        st.divider()


# ==================================================
# FOOTER
# ==================================================

st.caption(
    "CareCompass | RAG + FAISS + Llama 3.1 + "
    "NVIDIA NIM + NetworkX"
)