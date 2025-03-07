import streamlit as st


class View:
    def __init__(self, repo, model):
        self.repo = repo
        self.model = model
        self.config = repo.config
        # streamlit parameters
        self.streamlit_settings = self.repo.config["streamlit"]["settings"]
        self.streamlit_widgets_config = self.repo.config["streamlit"]["widgets"]
        self.streamlit_captions = self.repo.config["streamlit"]["captions"]

        self.streamlit_widgets = dict()

        st.set_page_config(
            page_title=self.streamlit_settings["page_title"],
            layout=self.streamlit_settings["layout"],
            initial_sidebar_state=self.streamlit_settings["initial_sidebar_state"],
        )

    def show_title(self):
        st.title(self.streamlit_settings["title"])

    def show_run_button(self):
        return st.sidebar.button(self.streamlit_widgets_config["start_button"]["name"])

    def show_reset_button(self):
        return st.sidebar.button(self.streamlit_widgets_config["reset_button"]["name"])

    def show_select_names(self):
        return st.sidebar.multiselect(
            label=self.streamlit_widgets_config["select_names"]["name"],
            options=self.repo.names,
            default=self.repo.names,
        )

    def show_success_message(self):
        st.success(self.streamlit_settings["success_message"])

    def show_toggle_data(self):
        return st.sidebar.toggle(
            self.streamlit_widgets_config["toggle_data"]["name"], value=False
        )

    def show_toggle_other_data(self):
        return st.sidebar.toggle(
            self.streamlit_widgets_config["toggle_other_data"]["name"], value=False
        )

    def show_data(self):
        """Displays the filtered data table."""
        st.write(self.streamlit_captions["data"])
        st.dataframe(self.repo.get_data_as_dataframe())

    def show_other_data(self):
        """Displays the filtered data table."""
        st.write(self.streamlit_captions["other_data"])
        st.dataframe(self.repo.get_other_data_as_dataframe())

    def show_results(self):
        """Displays the filtered data table."""
        st.write(self.streamlit_captions["results"])
        st.dataframe(self.model.get_data_as_dataframe())

    def persist_value(self, key, value=True):
        st.session_state[key] = value

    def get_persisted_value(self, key):
        return st.session_state.get(key)
