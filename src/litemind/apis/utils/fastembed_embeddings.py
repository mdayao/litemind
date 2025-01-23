from typing import List, Optional, Sequence

from arbol import aprint

from litemind.apis.utils.random_projector import DeterministicRandomProjector


def is_fastembed_available() -> bool:
    # Check that the fastembed library is installed:
    try:
        import fastembed
        return True
    except:
        return False


def fastembed_text(texts: List[str],
                   model_name: Optional[str] = 'BAAI/bge-large-en-v1.5',
                   dimensions: int = 512,
                   **kwargs) -> Sequence[Sequence[float]]:
    from fastembed import TextEmbedding

    # Check that the fastembed library is installed:
    supported_models = TextEmbedding.list_supported_models()

    # Check if the fastembed library is installed:
    supported_models = [model['model'] for model in supported_models]

    # Check if model is supported:
    if model_name not in supported_models:
        for model in supported_models:
            aprint(model)
        raise ValueError(
            f"Model {model_name} is not supported. Supported models are: {supported_models}")

    # Create a TextEmbedding object:
    model = TextEmbedding(model_name=model_name)

    # Embed the texts:
    embeddings = list(model.embed(texts))

    # Create a DeterministicRandomProjector object:
    drp = DeterministicRandomProjector(original_dim=len(embeddings[0]),
                                       reduced_dim=dimensions,
                                       **kwargs)

    # Project the embeddings:
    embeddings = drp.transform(embeddings)

    return embeddings
