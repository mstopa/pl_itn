from pathlib import Path

from fastapi import FastAPI, HTTPException, status
from prometheus_fastapi_instrumentator import Instrumentator

from pl_itn import Normalizer, Grammar, GrammarType
from pl_itn_service.grammar_loader import GrammarLoader, GrammarLoaderError
from pl_itn_service.models import NormalizeRequest, FstDetails, FstType
from pl_itn_service.logger import Logger
from pl_itn_service.config import Config

config = Config()
grammar_loader = GrammarLoader(Path(config.fst_dir))

logger = Logger(
    name="fastAPI pl_itn_logger",
    console_log_level=config.console_log_level,
    file_log_level=config.file_log_level,
    file_log_dir=config.file_log_dir,
).logger

app = FastAPI()
Instrumentator().instrument(app).expose(app)

normalizer = Normalizer()


@app.post("/normalize")
async def normalize(request: NormalizeRequest):
    text = request.text
    tagger = request.tagger
    verbalizer = request.verbalizer

    try:
        logger.debug(f"Normalizing text: {text}")
        if tagger is None and verbalizer is None:
            normalized_text = normalizer(text)
        else:
            logger.debug(
                f"Alernative grammar requested, creating temporary Normalizer instance..."
            )
            normalizer_kwargs = {}
            if tagger:
                logger.debug(f"tagger: {tagger}")
                (
                    tagger_path,
                    tagger_description,
                ) = grammar_loader.get_specified_fst(tagger, GrammarType.TAGGER)
                normalizer_kwargs["tagger_fst_path"] = tagger_path
            if verbalizer:
                logger.debug(f"verbalizer: {verbalizer}")
                (
                    verbalizer_path,
                    verbalizer_description,
                ) = grammar_loader.get_specified_fst(verbalizer, GrammarType.VERBALIZER)
                normalizer_kwargs["verbalizer_fst_path"] = verbalizer_path

            temp_normalizer = Normalizer(**normalizer_kwargs)
            normalized_text = temp_normalizer(text)

        return {"normalized_text": normalized_text}

    except GrammarLoaderError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown Error."
        )


@app.get("/normalizer/settings")
def get_normalizer_settings():
    try:
        tagger = FstDetails(
            name=normalizer.tagger.fst_path.name,
            type=FstType.TAGGER,
            description=normalizer.tagger.description,
        )

        verbalizer = FstDetails(
            name=normalizer.verbalizer.fst_path.name,
            type=FstType.VERBALIZER,
            description=normalizer.verbalizer.description,
        )

        return {"tagger": tagger, "verbalizer": verbalizer}

    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown Error."
        )


@app.get("/fst/taggers")
def list_tagger_fst():
    try:
        available_taggers = grammar_loader.get_available_fst(GrammarType.TAGGER)
        taggers_list = [
            FstDetails(name=fst_name, type=FstType.TAGGER, description=fst_description)
            for (fst_name, fst_description) in available_taggers.items()
        ]

        return {"fst": taggers_list}

    except GrammarLoaderError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown Error."
        )


@app.get("/fst/verbalizers")
def list_verbalizer_fst():
    try:
        available_verbalizers = grammar_loader.get_available_fst(GrammarType.VERBALIZER)
        verbalizers_list = [
            FstDetails(
                name=fst_name, type=FstType.VERBALIZER, description=fst_description
            )
            for (fst_name, fst_description) in available_verbalizers.items()
        ]

        return {"fst": verbalizers_list}

    except GrammarLoaderError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown Error."
        )


@app.post("/normalizer/fst", status_code=status.HTTP_200_OK)
def set_fst(request: FstDetails):
    try:
        fst_name = request.name
        grammar_type = (
            GrammarType.VERBALIZER
            if request.type == FstType.VERBALIZER
            else GrammarType.TAGGER
        )

        fst_path, description = grammar_loader.get_specified_fst(fst_name, grammar_type)
        normalizer.set_grammar(fst_path, grammar_type, description)

        return {"message": "Success"}

    except GrammarLoaderError as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unknown Error."
        )
