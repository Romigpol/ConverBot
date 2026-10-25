import os
from abc import ABC, abstractmethod
from PIL import Image
from pdf2docx import Converter as PdfConverter
from docx2pdf import convert as docx_to_pdf_convert
from pydub import AudioSegment

class BaseConverter(ABC):
    @abstractmethod
    def checkup(self, input_check: str, check_output: str) -> bool:
        pass
    @abstractmethod
    def convert(self, file_input: str, file_output: str) -> None:
        pass

class ImageConverter(BaseConverter):
    admits = ['png', 'jpg', 'jpeg', 'webp', 'bmp']
    def checkup(self, input_check: str, check_output: str) -> bool:
        return input_check in self.admits and check_output in self.admits
    def convert(self, file_input: str, file_output: str) -> None:
        output_ext = file_output.split('.')[-1].lower()
        with Image.open(file_input) as img:
            if output_ext in ['jpg', 'jpeg']:
                img = img.convert('RGB')
            img.save(file_output)

class DocumentConverter(BaseConverter):
    def checkup(self, input_check: str, check_output: str) -> bool:
        return (input_check == 'pdf' and check_output == 'docx') or \
               (input_check == 'docx' and check_output == 'pdf')
    def convert(self, file_input: str, file_output: str) -> None:
        input_ext = file_input.split('.')[-1].lower()
        output_ext = file_output.split('.')[-1].lower()
        if input_ext == 'pdf' and output_ext == 'docx':
            cv = PdfConverter(file_input)
            cv.convert(file_output, start=0, end=None)
            cv.close()
        elif input_ext == 'docx' and output_ext == 'pdf':
            docx_to_pdf_convert(file_input, file_output)

class AudioConverter(BaseConverter):
    admits = ['mp3', 'wav', 'ogg', 'flac', 'm4a', 'aac']
    def checkup(self, input_check: str, check_output: str) -> bool:
        return input_check in self.admits and check_output in self.admits
    def convert(self, file_input: str, file_output: str) -> None:
        output_ext = file_output.split('.')[-1].lower()
        audio = AudioSegment.from_file(file_input)
        audio.export(file_output, format=output_ext)

converters = [
    ImageConverter(),
    DocumentConverter(),
    AudioConverter()
]

def find_converter(input_check: str, check_output: str) -> BaseConverter:
    for conv in converters:
        if conv.checkup(input_check, check_output):
            return conv
    return None