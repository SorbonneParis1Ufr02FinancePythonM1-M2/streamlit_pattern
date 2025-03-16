import os.path

from constants import CONFIG_FOLDER, CONFIG_FILE_NAME, LOGGER_NAME, LOGGING_CONFIG_FILE
from helpers.helpers_logging import init_logger_from_file
from helpers.helpers_serialize import get_serialized_data
from model import Model
from repository import Repository
from view import View

logging_config_full_path = os.path.join(
    os.path.dirname(__file__), CONFIG_FOLDER, LOGGING_CONFIG_FILE
)
os.makedirs(os.path.dirname(logging_config_full_path), exist_ok=True)
logger = init_logger_from_file(
    logger_name=LOGGER_NAME, config_full_path=logging_config_full_path
)


class App:
    def __init__(self):
        logger.info("Initialize App")
        config_file_path = os.path.join(
            os.path.normpath(os.getcwd()), CONFIG_FOLDER, CONFIG_FILE_NAME
        )
        self.config = get_serialized_data(config_file_path)
        self.repo = Repository(self.config)
        self.model = Model(self.repo)
        self.view = View(self.repo, self.model)

    def run(self):
        logger.info("Run App")
        start_event_value = self.view.streamlit_widgets_config["start_button"]["event"]
        logger.info(f"start event={self.view.get_persisted_value(start_event_value)}")
        self.view.show_title()
        start_button = self.view.show_run_button()
        reset_button = self.view.show_reset_button()
        names = self.view.show_select_names()
        logger.debug(f"names={names}")
        toggle_data = self.view.show_toggle_data()
        toggle_other_data = self.view.show_toggle_other_data()
        export = self.view.show_export_button()

        if start_button:
            logger.debug("Start button")
            self.view.persist_value(start_event_value)

        if reset_button:
            logger.debug("Reset button")
            self.view.persist_value(start_event_value, False)

        if self.view.get_persisted_value(start_event_value):
            self.repo.load_data(names)
            self.repo.load_other_data(names)
            self.model.process()
            columns_results = self.view.show_multiselect_columns()
            items_filtered = self.view.show_selected_items()
            filter = self.view.show_slider_results()
            if toggle_data:
                self.view.show_data()
            if toggle_other_data:
                self.view.show_other_data()
            self.view.show_results(columns_results, items_filtered, filter)
            self.view.show_success_message()

            if export:
                logger.info("Run export")
                self.view.export_to_excel()


if __name__ == "__main__":
    app = App()
    app.run()
    logger.info("Finished")
