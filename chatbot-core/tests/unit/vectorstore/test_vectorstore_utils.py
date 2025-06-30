"""Unit Tests for vectorstore_utils."""

from rag.vectorstore.vectorstore_utils import save_faiss_index

def test_save_faiss_index_success(mocker, tmp_path):
    """Test saving FAISS index successfully logs info."""
    mock_index = mocker.Mock()
    mock_write_index = mocker.patch("faiss.write_index")
    mock_logger = mocker.Mock()
    path = tmp_path / "index.faiss"

    save_faiss_index(mock_index, str(path), mock_logger)

    mock_write_index.assert_called_once_with(mock_index, str(path))
    mock_logger.info.assert_called_once_with("FAISS index saved to %s", str(path))


def test_save_faiss_index_logs_error_on_oserror(mocker, tmp_path):
    """Test that OSError during save is logged as error."""
    mock_index = mocker.Mock()
    mock_logger = mocker.Mock()
    mock_write_index = mocker.patch("faiss.write_index", side_effect=OSError("disk full"))
    path = tmp_path / "index.faiss"

    vsu.save_faiss_index(mock_index, str(path), mock_logger)

    mock_logger.error.assert_called_once()
    assert "Failed to save FAISS index" in mock_logger.error.call_args[0][0]


def test_load_faiss_index_success(mocker, tmp_path):
    """Test loading FAISS index successfully logs info and returns index."""
    mock_index = mocker.Mock()
    mock_read_index = mocker.patch("faiss.read_index", return_value=mock_index)
    mock_logger = mocker.Mock()
    path = tmp_path / "index.faiss"

    result = vsu.load_faiss_index(str(path), mock_logger)

    mock_logger.info.assert_any_call("Loading FAISS index from %s...", str(path))
    mock_logger.info.assert_any_call("FAISS index loaded successfully.")
    mock_read_index.assert_called_once_with(str(path))
    assert result == mock_index


def test_load_faiss_index_file_not_found(mocker, tmp_path):
    """Test that FileNotFoundError is logged and returns None."""
    mock_logger = mocker.Mock()
    mocker.patch("faiss.read_index", side_effect=FileNotFoundError("not found"))
    path = tmp_path / "missing_index.faiss"

    result = vsu.load_faiss_index(str(path), mock_logger)

    mock_logger.error.assert_called_once()
    assert "File error while loading FAISS index" in mock_logger.error.call_args[0][0]
    assert result is None


def test_load_faiss_index_oserror(mocker, tmp_path):
    """Test that OSError is logged and returns None."""
    mock_logger = mocker.Mock()
    mocker.patch("faiss.read_index", side_effect=OSError("corrupt file"))
    path = tmp_path / "bad_index.faiss"

    result = vsu.load_faiss_index(str(path), mock_logger)

    mock_logger.error.assert_called_once()
    assert result is None


def test_save_metadata_success(mocker, tmp_path):
    """Test that metadata is pickled successfully and logs info."""
    metadata = {"some": "data"}
    mock_logger = mocker.Mock()
    path = tmp_path / "metadata.pkl"

    vsu.save_metadata(metadata, str(path), mock_logger)

    assert path.exists()
    mock_logger.info.assert_called_once_with("Metadata saved to %s", str(path))

def test_save_metadata_logs_error_on_exception(mocker, tmp_path):
    """Test that error during pickle dumping is logged."""
    metadata = {"bad": "data"}
    mock_logger = mocker.Mock()
    # Mock open() to raise OSError
    mocker.patch("builtins.open", side_effect=OSError("permission denied"))
    path = tmp_path / "metadata.pkl"

    vsu.save_metadata(metadata, str(path), mock_logger)

    mock_logger.error.assert_called_once()
    assert "Failed to save metadata" in mock_logger.error.call_args[0][0]


def test_load_metadata_success(mocker, tmp_path):
    """Test loading metadata successfully logs info and returns data."""
    data = {"a": 1}
    path = tmp_path / "metadata.pkl"
    with open(path, "wb") as f:
        pickle.dump(data, f)

    mock_logger = mocker.Mock()

    result = vsu.load_metadata(str(path), mock_logger)

    mock_logger.info.assert_any_call("Loading metadata from %s...", str(path))
    mock_logger.info.assert_any_call("Metadata loaded successfully.")
    assert result == data

def test_load_metadata_file_not_found(mocker, tmp_path):
    """Test FileNotFoundError during metadata load."""
    mock_logger = mocker.Mock()
    path = tmp_path / "no_metadata.pkl"

    result = vsu.load_metadata(str(path), mock_logger)

    mock_logger.error.assert_called_once()
    assert "Metadata file not found" in mock_logger.error.call_args[0][0]
    assert result is None

def test_load_metadata_unpickling_error(mocker, tmp_path):
    """Test unpickling error during metadata load."""
    path = tmp_path / "corrupt_metadata.pkl"
    with open(path, "wb") as f:
        f.write(b"not a pickle")
    mock_logger = mocker.Mock()

    result = vsu.load_metadata(str(path), mock_logger)

    mock_logger.error.assert_called_once()
    assert "Failed to load metadata" in mock_logger.error.call_args[0][0]
    assert result is None
