import crdatamgt
import yaml
import os
import simplelogging
from yaml.scanner import ScannerError

from crdatamgt.helpers import log_format


def main():
    log = simplelogging.get_logger(
        file_name="cr.log", console=False, file_format=log_format("simple")
    )

    def represent_none(self, _):
        return self.represent_scalar("tag:yaml.org,2002:null", "")

    yaml.add_representer(type(None), represent_none)

    try:
        with open("parameters.yaml", "r") as stream:
            try:
                data_loaded = yaml.safe_load(stream)
                crdatamgt.project.project_load(**data_loaded)
            except TypeError as e:
                log.exception(e)
                print("Please double-check your parameters.yaml document'")
                os.startfile(os.path.join(os.getcwd(), "parameters.yaml"))
                log.debug("Type Error\n     {}".format(e))
            except ScannerError as e:
                print(
                    "Your YAML file is not properly formated - Likley missing a space BEFORE your file-path\n Example -> RESULTS DIRECTORY: R:\Shared Drive <- Is proper"
                )
                log.debug("YAML parse error\n    {}".format(e))

    except FileNotFoundError as e:
        data_loaded = crdatamgt.helpers.write_yaml()
        with open("parameters.yaml", "w") as outfile:
            yaml.dump(data_loaded, outfile, default_flow_style=False)
        print("Please fill out the parameter.yaml document")
        log.debug("File not found\n     {}".format(e))
        os.startfile(os.path.join(os.getcwd(), "parameters.yaml"))



if __name__ == "__main__":
    main()
