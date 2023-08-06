from ier_processor.pdf_slicing import PDFSlicingMachine
from ier_processor.image_record_processing import ImageProcessor
from pathlib import Path
import pytesseract
import os


def main():
    print("testing split functionality")
    slicer = PDFSlicingMachine(debug=False)
    test_pdf_file = os.path.join(Path(__file__).parent, 'test_data', 'whole_pdf', 'Benaulim', 'Part01.pdf')
    print(f"trying to split {test_pdf_file}..............")
    page_images = slicer.split_whole_pdf_into_pages(test_pdf_file, ".")
    for page_image in page_images:
        print(page_image)

    print('Now trying to further split one of the page images........')
    # we want to avoid page 2(this has photos etc.... )
    page_images.sort()
    some_page = page_images[4]
    print(f'Working with {some_page}')
    record_images = slicer.split_pdf_page_image_into_record_images(pdf_page_image_path=some_page, dest_base=".")
    for record_image in record_images:
        print(record_image)

    print("Now trying to extract text from one of the record images ......")
    some_record_image = record_images[8]
    print(f"Working with {some_record_image}")
    image_processor = ImageProcessor()

    record_type, extracted_data = image_processor.process_image(some_record_image)
    print(f'Image data is {record_type} :: {extracted_data}')

    assembly_image = list(filter(lambda x: "Assembly" in x, record_images))
    record_type, extracted_data = image_processor.process_image(assembly_image[0])
    print(f'Image data is {record_type} :: {extracted_data}')

    section_image = list(filter(lambda x: "Section" in x, record_images))
    record_type, extracted_data = image_processor.process_image(section_image[0])
    print(f'Image data is {record_type} :: {extracted_data}')





if __name__ == '__main__':
    if os.name == 'nt':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    main()

