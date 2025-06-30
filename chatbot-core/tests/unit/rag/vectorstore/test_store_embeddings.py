"""Unit Tests for store_embeddings module."""

import numpy as np
import faiss
from rag.vectorstore import store_embeddings

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

    result_index = store_embeddings.build_faiss_ivf_index(vectors, nlist=4, nprobe=2, logger=mock_logger)

    mock_quantizer_cls.assert_called_once_with(5)
    mock_index_cls.assert_called_once_with(mock_quantizer, 5, 4, faiss.METRIC_L2)
    mock_index.train.assert_called_once_with(vectors)
    mock_index.add.assert_called_once_with(vectors)
    mock_logger.info.assert_any_call("FAISS index training started...")
    mock_logger.info.assert_any_call("FAISS index training completed.")
    assert result_index.nprobe == 2
