import streamlit as st
import sqlite3
import os
import json
import ingest_utils
from vector_search import search_questions, fetch_all_questions,delete_rows_from_db
import pandas as pd

def update_qlqrecord(question, lens_query):
    ingest_utils.save_question_query(question, lens_query)

def reset_session_state():
    # Clear all relevant session state variables
    st.session_state.selected_rows = []
    st.session_state.show_df = False
    st.session_state.selected_questions = []
    st.session_state.refresh = False
    if 'dataframe' in st.session_state:
        del st.session_state['dataframe']

def search_questions_vector_db():

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300&display=swap');
        .title0 {{
            text-align: center;
            font-size: 35px;
            font-weight: light;
            color: white;
            position: relative;
            top: -55px;
            margin-bottom: 10px;
            color: black;

        }}
        @media (prefers-color-scheme: dark) {{
            .title0 {{
                    color: white;
                }}
            }}
            @media (prefers-color-scheme: light) {{
                .title0 {{
                    color: black;
                }}
            }}
        </style>
        <div class="title0">
            Search Vector Store
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
                <style>
                    [data-testid="stForm"] {border: 0px}
                </style>
            """,
        unsafe_allow_html=True,
    )


    # Initialize session state variables for c2 delete feature

    if 'selected_rows_c2' not in st.session_state:
        st.session_state.selected_rows_c2 = []
    if 'show_df_c2' not in st.session_state:
        st.session_state.show_df_c2 = False
    if 'selected_questions_c2' not in st.session_state:
        st.session_state.selected_questions_c2 = []
    if 'refresh_c2' not in st.session_state:
        st.session_state.refresh_c2 = False
    delete_button_c2 = False
    refresh_button_c2 = False
    df_c2 = None  # Initialize the variable


    # Initialize session state variables for c3 delete feature
    if 'selected_rows' not in st.session_state:
        st.session_state.selected_rows = []
    if 'show_df' not in st.session_state:
        st.session_state.show_df = False
    if 'selected_questions' not in st.session_state:
        st.session_state.selected_questions = []
    if 'refresh' not in st.session_state:
        st.session_state.refresh = False
    delete_button = False
    refresh_button = False




    df = fetch_all_questions()
    with st.form("Questions Data Form"):

        c1, c2, c3 = st.columns([0.65, 0.15, 0.20], vertical_alignment="top")

        with c1:
            st.markdown(
                """
                <style>
                .stTextInput  {
                    margin-top: -70px;
                    }
                </style>
                """,
                unsafe_allow_html=True,
            )
            question = st.text_input(
                "Enter a natural language questions you want to search",
                placeholder="Please enter your question...",
                label_visibility="hidden",
            )

        with c2:
            st.markdown(
                """
                <style>
                    .stButton  {
                        margin-top: -42px;
                        }
                    </style>
                """,
                unsafe_allow_html=True,
            )
            submitted = st.form_submit_button("Search")
        if submitted:
            rec = search_questions(question)
            if rec:
                st.empty()
                # st.markdown(
                #      f"""
                #         <style>
                #         @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300&display=swap');
                #         .title2 {{
                #             text-align: center;
                #             font-size: 20px;
                #             font-weight: 100;
                #             color: white;
                #             position: relative;
                #             margin-bottom: 10px;
                #             color: black;
                #         }}
                #         @media (prefers-color-scheme: dark) {{
                #             .title2 {{
                #                     color: white;
                #                 }}
                #             }}
                #             @media (prefers-color-scheme: light) {{
                #                 .title2 {{
                #                     color: black;
                #                 }}
                #             }}
                #         </style>
                #         <div class="title2">
                #            Search Results
                #         </div>
                #         """,
                # unsafe_allow_html=True,
                # )
                # st.markdown(
                #     """
                # <style>
                # [data-testid="stElementToolbar"] {
                #     display: none;
                # }
                # </style>
                # """,
                #     unsafe_allow_html=True,
                # )

                data = pd.DataFrame(rec)
                df_c2 = data.rename(
                    columns={
                        "question": "Question",
                        "json_query": "Lens Query",
                        "_distance": "Distance",
                    }
                )
                st.session_state.df_c2 = df_c2
                st.session_state.show_df_c2 = True
                # st.dataframe(df_c2, use_container_width=True, hide_index=True)
            else:
                st.write("No Matching records Found")

    if st.session_state.show_df_c2:
        st.markdown(
                     f"""
                        <style>
                        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300&display=swap');
                        .title2 {{
                            text-align: center;
                            font-size: 20px;
                            font-weight: 100;
                            color: white;
                            position: relative;
                            margin-bottom: 10px;
                            color: black;
                        }}
                        @media (prefers-color-scheme: dark) {{
                            .title2 {{
                                    color: white;
                                }}
                            }}
                            @media (prefers-color-scheme: light) {{
                                .title2 {{
                                    color: black;
                                }}
                            }}
                        </style>
                        <div class="title2">
                           Search Results
                        </div>
                        """,
                unsafe_allow_html=True,
                )
        st.markdown(
            """
        <style>
        [data-testid="stElementToolbar"] {
            display: none;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        selected_rows_c2 = st.dataframe(
            st.session_state.df_c2,
            key="dataframe_c2",
            on_select="rerun",  # Trigger rerun on selection
            selection_mode="multi-row",  # Allow multiple row selection
            column_order=["Question", "Lens Query", "Distance"],
            hide_index=True
        )

        # Handle the selection
        if 'dataframe_c2' in st.session_state:
            selection_c2 = st.session_state["dataframe_c2"].get("selection", {})
            if selection_c2 and "rows" in selection_c2:
                st.session_state.selected_rows_c2 = selection_c2["rows"]

    # Show selected rows data if any rows are selected
    if st.session_state.selected_rows_c2:
        df_c2 = st.session_state.df_c2  # Retrieve df_c2 from session state
        selected_rows_data_c2 = df_c2.iloc[st.session_state.selected_rows_c2]
        st.session_state.selected_questions_c2 = selected_rows_data_c2['Question'].tolist()

        delete_button_c2 = st.button("Delete Selected Rows", key="delete_c2")
        if delete_button_c2:
            delete_rows_from_db(st.session_state.selected_questions_c2)
            # Reset state after deletion
            st.session_state.selected_rows_c2 = []
            st.session_state.selected_questions_c2 = []



        with c3:
            st.markdown(
                """
                <style>
                    .stButton  {
                        margin-top: -42px;
                        }
                    </style>
                """,
                unsafe_allow_html=True,
            )
            submitted = st.form_submit_button("All Records")
        if submitted:
            st.empty()
            df = fetch_all_questions()
            st.session_state.show_df = True

            # st.dataframe(
            #     df,
            #     selection_mode="multi-row",
            #     on_select="rerun",
            #     key="dataframe",
            #     hide_index=True
            # )

    if st.session_state.show_df:
        st.markdown(
                        f"""
                            <style>
                            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300&display=swap');
                            .title1 {{
                                text-align: center;
                                font-size: 20px;
                                font-weight: 100;
                                color: white;
                                position: relative;
                                margin-bottom: 10px;
                                color: black;

                            }}
                            @media (prefers-color-scheme: dark) {{
                                .title1 {{
                                        color: white;
                                    }}
                                }}
                                @media (prefers-color-scheme: light) {{
                                    .title1 {{
                                        color: black;
                                    }}
                                }}
                            </style>
                            <div class="title1">
                            All rows of Vector DB
                            </div>
                            """,
                    unsafe_allow_html=True,
                )
        selected_rows = st.dataframe(
            df,
            key="dataframe",
            on_select="rerun",  # Trigger rerun on selection
            selection_mode="multi-row",  # Allow multiple row selection
            column_order=["Question", "Lens Query"],
            hide_index=True
        )

        # Handle the selection
        if 'dataframe' in st.session_state:
            selection = st.session_state["dataframe"].get("selection", {})
            if selection and "rows" in selection:
                st.session_state.selected_rows = selection["rows"]

    # Show selected rows data if any rows are selected
    if st.session_state.selected_rows:
        # Extract selected rows
        selected_rows_data = df.iloc[st.session_state.selected_rows]
        # Ensure 'Question' is a Series and convert to a list
        st.session_state.selected_questions = selected_rows_data['Question'].tolist()

        delete_button= st.button("Delete Selected Rows")

    if delete_button:
        print(st.session_state.selected_questions)
        delete_rows_from_db(st.session_state.selected_questions)


        if st.session_state.refresh:
            refresh_button = st.button("Refresh")

    if refresh_button:
        st.empty()
        st.session_state.show_df = False


if __name__ == '__main__':
    search_questions_vector_db()