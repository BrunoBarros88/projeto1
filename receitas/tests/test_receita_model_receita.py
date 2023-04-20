import tempfile

from PIL import Image

from .test_receita_base import ReceitaTestBase


class ReceitaModelTest(ReceitaTestBase):
    def setUp(self) -> None:
        self.image = tempfile.NamedTemporaryFile(suffix=".jpg").name
        with open(self.image, 'w') as f:
            Image.new('RGB', (100, 100)).save(f, 'jpeg')
        self.receita = self.make_receita()
        return super().setUp()
