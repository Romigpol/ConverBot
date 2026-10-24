import os
from abc import ABC, abstractmethod
from PIL import Image
from pdf2docx import Converter as PdfConverter
from docx2pdf import convert as docx_to_pdf_convert
from pydub import AudioSegment

class BaseConverter(ABC):
    @abstractmethod
    def can_handle(self, input_ext: str, output_ext: str) -> bool:
        pass
    @abstractmethod
    def convert(self, input_path: str, output_path: str) -> None:
        pass

class ImageConverter(BaseConverter):
    SUPPORTED = ['png', 'jpg', 'jpeg', 'webp', 'bmp']
    def can_handle(self, input_ext: str, output_ext: str) -> bool:
        return input_ext in self.SUPPORTED and output_ext in self.SUPPORTED
    def convert(self, input_path: str, output_path: str) -> None:
        output_ext = output_path.split('.')[-1].lower()
        with Image.open(input_path) as img:
            if output_ext in ['jpg', 'jpeg']:
                img = img.convert('RGB')
            img.save(output_path)

class DocumentConverter(BaseConverter):
    def can_handle(self, input_ext: str, output_ext: str) -> bool:
        return (input_ext == 'pdf' and output_ext == 'docx') or \
               (input_ext == 'docx' and output_ext == 'pdf')
    def convert(self, input_path: str, output_path: str) -> None:
        input_ext = input_path.split('.')[-1].lower()
        output_ext = output_path.split('.')[-1].lower()
        if input_ext == 'pdf' and output_ext == 'docx':
            cv = PdfConverter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
        elif input_ext == 'docx' and output_ext == 'pdf':
            docx_to_pdf_convert(input_path, output_path)

class AudioConverter(BaseConverter):
    SUPPORTED = ['mp3', 'wav', 'ogg', 'flac', 'm4a', 'aac']
    def can_handle(self, input_ext: str, output_ext: str) -> bool:
        return input_ext in self.SUPPORTED and output_ext in self.SUPPORTED
    def convert(self, input_path: str, output_path: str) -> None:
        output_ext = output_path.split('.')[-1].lower()
        audio = AudioSegment.from_file(input_path)
        audio.export(output_path, format=output_ext)

CONVERTERS = [
    ImageConverter(),
    DocumentConverter(),
    AudioConverter()
]

def find_converter(input_ext: str, output_ext: str) -> BaseConverter:
    for conv in CONVERTERS:
        if conv.can_handle(input_ext, output_ext):
            return conv
    return None