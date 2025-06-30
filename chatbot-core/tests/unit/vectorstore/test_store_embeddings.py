import numpy as np
import pytest
import faiss
from rag.vectorstore import embedding_storage as es

def test_build_faiss_ivf_index_trains_and_adds_vectors(mocker):
    """Test that build_faiss_ivf_index trains and adds vectors correctly."""
    vectors = np.random.rand(10, 5).astype("float32")
    mock_logger = mocker.Mock()

    # Patch IndexFlatL2 and IndexIVFFlat to be Mocks
    mock_quantizer = mocker.Mock()
    mock_index = mocker.Mock()
    mock_index.nprobe = 0

    mock_index_cls = mocker.patch("faiss.IndexIVFFlat", return_value=mock_index)
    mock_quantizer_cls = mocker.patch("faiss.IndexFlatL2", return_value=mock_quantizer)

    result_index = es.build_faiss_ivf_index(vectors, nlist=4, nprobe=2, logger=mock_logger)

    mock_quantizer_cls.assert_called_once_with(5)
    mock_index_cls.assert_called_once_with(mock_quantizer, 5, 4, faiss.METRIC_L2)
    mock_index.train.assert_called_once_with(vectors)
    mock_index.add.assert_called_once_with(vectors)

    assert result_index.nprobe == 2
    mock_logger.info.assert_any_call("FAISS index training started...")
    mock_logger.info.assert_any_call("FAISS index training completed.")


def test_run_indexing_pipeline_success(mocker):
    """Test run_indexing calls embedding, building index, and saving."""
    mock_logger = mocker.Mock()
    mock_vectors = [[0.1, 0.2], [0.3, 0.4]]
    mock_metadata = [{"id": 1}, {"id": 2}]
    # Patch embed_chunks
    mock_embed_chunks = mocker.patch("rag.vectorstore.embedding_storage.embed_chunks", return_value=(mock_vectors, mock_metadata))
    # Patch build_faiss_ivf_index
    mock_index = mocker.Mock()
    mock_build_index = mocker.patch("rag.vectorstore.embedding_storage.build_faiss_ivf_index", return_value=mock_index)
    # Patch save_faiss_index / save_metadata
    mock_save_index = mocker.patch("rag.vectorstore.embedding_storage.save_faiss_index")
    mock_save_metadata = mocker.patch("rag.vectorstore.embedding_storage.save_metadata")

    es.run_indexing(nlist=8, nprobe=3, logger=mock_logger)

    mock_embed_chunks.assert_called_once_with(mock_logger)

    # Check that vectors are converted to float32 numpy array
    vectors_arg = mock_build_index.call_args[0][0]
    assert isinstance(vectors_arg, np.ndarray)
    assert vectors_arg.dtype == np.float32

    mock_build_index.assert_called_once_with(vectors_arg, nlist=8, nprobe=3, logger=mock_logger)
    mock_save_index.assert_called_once_with(mock_index, es.INDEX_PATH, mock_logger)
    mock_save_metadata.assert_called_once_with(mock_metadata, es.METADATA_PATH, mock_logger)

    mock_logger.info.assert_any_call("Starting document embedding...")
    mock_logger.info.assert_any_call(f"Stored {len(mock_vectors)} vectors to FAISS (IVFFlat) at {es.INDEX_PATH}")
