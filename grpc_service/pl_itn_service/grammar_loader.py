from pathlib import Path
import yaml

from pl_itn import GrammarType
from grpc import StatusCode


class GrammarLoaderError(Exception):
    def __init__(
        self,
        grpc_error=StatusCode.UNKNOWN,
        message="Loading grammar fst failed.",
    ):
        self.grpc_error = grpc_error
        self.message = message

        super().__init__(self.message)


class GrammarLoader:
    def __init__(self, resources_path: Path, fst_config_file: str = "config.yaml"):
        self.resources_path = resources_path
        self.fst_config_file = fst_config_file

    def _read_config(self):
        try:
            with open(self.resources_path / self.fst_config_file) as config:
                config_dict = yaml.safe_load(config)
                return config_dict
        except FileNotFoundError:
            raise GrammarLoaderError(
                grpc_error=StatusCode.NOT_FOUND,
                message=f"{self.resources_path / self.fst_config_file} does not exist.",
            )
        except yaml.YAMLError:
            raise GrammarLoaderError(
                grpc_error=StatusCode.INVALID_ARGUMENT,
                message=f"{self.resources_path / self.fst_config_file} is not a valid yaml file.",
            )

    def get_available_fst(self, fst_type: GrammarType):
        available_fst = self._read_config()
        if fst_type == GrammarType.TAGGER:
            available_fst = available_fst.get("taggers")
        else:
            available_fst = available_fst.get("verbalizers")
        return available_fst

    def get_specified_fst(self, fst_name: str, fst_type: GrammarType):
        specified_fst_description = self.get_available_fst(fst_type).get(fst_name)
        if not specified_fst_description:
            raise GrammarLoaderError(
                grpc_error=StatusCode.INVALID_ARGUMENT,
                message=f"'{fst_name}' grammar of type {fst_type} not found.",
            )
        return self.resources_path / fst_name, specified_fst_description


if __name__ == "__main__":
    try:
        rl = GrammarLoader(
            Path("/home/tkurkowski/Tasks/studia/inzynierka/fst_resources")
        )
        print(rl.get_available_fst(GrammarType.VERBALIZER))
    except GrammarLoaderError:
        print("asdas")
