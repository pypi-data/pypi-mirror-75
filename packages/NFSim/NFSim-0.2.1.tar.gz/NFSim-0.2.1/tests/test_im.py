import os

def im_test(image):
    with pytest.raises(FileNotFoundError):
        assert os.path.exists(image)