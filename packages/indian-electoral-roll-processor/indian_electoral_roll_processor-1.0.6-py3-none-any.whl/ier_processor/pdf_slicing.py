from PIL import Image
import glob
import os.path
import pytesseract
import pdf2image
from ier_processor.utils import *
import shutil

from datetime import datetime


class PDFSlicingMachine:

    """
    # a pdf document contains records that we want to extract
    # the first page contains contains general info
    # the second page contains photos
    # records start rom the third page onwards
    # each record is printed in a rectangular slot
    """

    def __init__(self, debug=False):
        self.debug = debug



    def split_whole_pdf_into_pages(self, src_pdf_file, dest_dir):
        """each page of the pdf file is an image
        the pdf has been created in this fashion to prevent parsing of the pdf using pdf parsing libraries
        we need to split the pdf into its constituent images and then process each of the page-image"""

        # the pdf file has a name like Aldona/Part01.pdf.
        # We want to extract "Aldona" as constituency and "01" as the constituency_file_id
        path_regex = re.compile(r'\W(\w+?)\WPart(\d\d).pdf')
        matching = path_regex.search(src_pdf_file)
        split_files = []
        if not matching:
            raise ValueError(f'Could not get constituency and constituency_page_id from path {src_pdf_file}. '
                             f'Expecting a file like Aldona\\Part01.pdf')
        else:
            constituency, constituency_file_id = (matching.group(1), matching.group(2)) if matching else (None, None)

            # the pdf might be located on aws s3 or local file system
            # create a local working dir and copy the pdf to it
            time_prefix = datetime.now().strftime('%Y%m%d_%H%M%S')
            working_dir_prefix = f'z_pdf_split_{time_prefix}_{constituency}_{constituency_file_id}'
            working_dir = create_working_directory(working_dir_prefix)

            pdf_path_in_working_directory = os.path.join(working_dir, os.path.basename(src_pdf_file))
            copy_across_file_systems(src_pdf_file, pdf_path_in_working_directory)

            # split pdf into images
            split_results_dir = working_dir + os.sep
            #import subprocess
            #subprocess.call([r'c:\Program Files\poppler-0.68.0\bin\pdfimages.exe',
            #                 '-png',
            #                 pdf_path_in_working_directory,
            #                 split_results_dir])


            split_params = { 'output_folder': split_results_dir, 'fmt': 'png', 'thread_count': 4 }
            if os.name == 'nt':
                split_params['poppler_path'] = r'c:\Program Files\poppler-0.68.0\bin'
            pdf2image.convert_from_path(pdf_path_in_working_directory, **split_params)

            # rename the pdf page images and copy the split pages to the destination
            # files should be renamed as {constituency}_F{file_no}_P{page_no}.png
            page_id_regex = re.compile(r'(\d+).png$')
            for split_image in glob.glob(os.path.join(working_dir, '*.png')):
                matching = page_id_regex.search(split_image)
                if matching:
                    page_id = matching.group(1)
                    file_dest_dir = os.path.join(dest_dir, 'pdf_pages_as_images', constituency, constituency_file_id,
                                            page_id)
                    dest_path = os.path.join(file_dest_dir, f'{constituency}_F{constituency_file_id}_P{page_id}.png')
                    copy_across_file_systems(split_image, dest_path)
                    split_files.append(dest_path)
                else:
                    print(f'ignoring file {split_image} in split directory. could not extract file_id')
        # split_dir.cleanup();
            #remove working dir
            if not self.debug:
                shutil.rmtree(working_dir)
        return split_files

    def assembly_image_boundaries(self):
        """the coordinates on the image that contain assembly information(e.g. Aldona)"""
        #return 50, 10, 790, 35
        return 60, 15, 880, 50

    def section_image_boundaries(self):
        """the coordinates of the image that contain section information(e.g. Portais)"""
        # return 50, 50, 790, 80
        return 60, 70, 880, 108

    #  (0,0)--------------------------> x
    #   |              ^
    #   |              | offset from top of page
    #   |              |
    #   |              V
    #   |         ---------------------------------------
    #   |        |  Record 0   |  Record 1  | Record 2   |
    #   |        |             |            |            |
    #   |        |             |            |            |
    #   |         ---------------------------------------
    #   |        |  Record 3   |  Record 4  |  Record 5  |
    #   |        |             |            |            |
    #   |        |             |            |            |
    #   |         ---------------------------------------
    #   |        |  Record 6   |  Record 7  | Record 8   |
    #   |        |             |            |            |
    #   V        |             |            |            |
    #   y        ---------------------------------------
    #            |  Record 9   |  Record 10 | Record 11  |
    #            |             |            |            |
    #            |             |            |            |
    #             ---------------------------------------
    #            |  Record 12  | Record 13 | Record 14   |
    #            |             |            |            |
    #            |             |            |            |
    #             ---------------------------------------

    def record_boundaries(self, record_number, page_number=2):
        """" a pdf file has multiple pages.
         first page contains general info, and pages 2 to 30 contain records.
         the layout on page 2 is slightly different from rest of the pages.
         on page 2, the margin from the top of the page is more than other pages."""
        row = record_number // 3
        column = record_number % 3

        offset_from_top = 141 if page_number == 3 else 68
        #offset_from_top = 115
        #offset_from_top = 84

        row_height = 195

        # this value is from trial and error
        #row_height_adjustment_factor = 0.8 if row < 3 else 1.5
        row_height_adjustment_factor = 0

        y_top = offset_from_top + row * (row_height + row_height_adjustment_factor)
        y_bottom = y_top + row_height + 2

        # the record width is not the same for each column
        columns = [
            (68, y_top, 569, y_bottom),
            (570, y_top, 1071, y_bottom),
            (1072, y_top, 1572, y_bottom)]

        return columns[column]

    #   def get_voter_page_voter_boundaries(i, page_number=2):
    #       i = i - 1
    #       row = i // 3
    #       column = i % 3

    #       y_index = row
    #       y_length = 140
    #       y_offset = (y_index * y_length)

    #       start_y = 102 if page_number == 2 else 84

    #       y_top = start_y + y_index * (145 + (0.8 if y_index < 3 else 1.5))
    #       y_bottom = y_top + 147

    #       columns = [
    #           (50, y_top, 428, y_bottom), (426, y_top, 808, y_bottom), (803, y_top, 1183, y_bottom)]

    #       p = columns[column]
    #       return p

    def polling_area_boundaries_fin(self):
        #return 534, 562, 1050, 787
        return 712, 764, 1218, 988

    def crop_image(self, img, image_coordinates):
        return img.crop(image_coordinates)

    def extract_image_text(self, image):
        custom_oem_psm_config = r'--oem 3 --psm 6'
        return pytesseract.image_to_string(image, config=custom_oem_psm_config)

    def save_image_as(self, image_object, image_name, working_dir, dest_dir):
        save_image_path = os.path.join(working_dir, image_name)
        image_object.save(save_image_path)
        dest_image_path = os.path.join(dest_dir, image_name)
        copy_across_file_systems(save_image_path, dest_image_path)

    def split_pdf_page_image_into_record_images(self, pdf_page_image_path, dest_base):
        """the image h"""

        # the image has a name like Aldona_F1_P2.png where Aldona is the name of the constituency , F1 refers to File 1 of
        # Aldona constituency and P1 refers to page 1 of file 1

        file_name_regex = re.compile(r'(\w+)_F(\d+)_P(\d+).png$')
        matching = file_name_regex.search(pdf_page_image_path)
        if not matching:
            raise ValueError("Cannot extract constituency , file and page number from {pdf_page_image} . "
                             "Expecting a file name like Aldona_F3_P2.png")
        else:
            constituency, constituency_file_id, page_id = matching.group(1), matching.group(2), matching.group(3)
            time_prefix = datetime.now().strftime('%Y%m%d_%H%M%S')
            prefix = f'z_pdf_page_split_{time_prefix}_{constituency}_{constituency_file_id}_{page_id}'
            working_dir = create_working_directory(prefix, debug=self.debug)
            local_pdf_page_image_path = os.path.join(working_dir, os.path.basename(pdf_page_image_path))
            copy_across_file_systems(pdf_page_image_path, local_pdf_page_image_path)

            dest_dir = os.path.join(dest_base, 'pdf_pages_as_images', constituency, constituency_file_id, page_id)
            if page_id == '01' or page_id == '000':
                return self.process_header_page(constituency, constituency_file_id, dest_dir, local_pdf_page_image_path, page_id, working_dir)
            elif page_id == '02':
                pass
                return []
            else:
                return self.process_records_page(constituency, constituency_file_id, dest_dir, local_pdf_page_image_path, page_id, working_dir)
            if not self.debug:
                shutil.rmtree(working_dir)

    def process_header_page(self, constituency, constituency_file_id, dest_dir, local_pdf_page_image_path, page_id, working_dir):
        first_page = Image.open(local_pdf_page_image_path)
        polling_area_boundaries = self.polling_area_boundaries_fin()
        polling_area_image = self.crop_image(first_page, polling_area_boundaries)
        image_name = f'{constituency}_F{constituency_file_id}_P{page_id}_TPDFHeader_0.png'
        self.save_image_as(polling_area_image, image_name, working_dir, dest_dir)
        return [os.path.join(dest_dir, image_name)]

    def process_records_page(self, constituency, constituency_file_id, dest_dir, local_pdf_page_image_path, page_id,
                             working_dir):
        record_images = []
        page_image = Image.open(local_pdf_page_image_path)
        assembly_image = self.crop_image(page_image, self.assembly_image_boundaries())
        assembly_image_name = f'{constituency}_F{constituency_file_id}_P{page_id}_TAssembly_0.png'
        record_images.append(os.path.join(dest_dir, assembly_image_name))
        self.save_image_as(assembly_image, assembly_image_name, working_dir, dest_dir)
        section_image = self.crop_image(page_image, self.section_image_boundaries())
        section_image_name = f'{constituency}_F{constituency_file_id}_P{page_id}_TSection_0.png'
        record_images.append(os.path.join(dest_dir, section_image_name))
        self.save_image_as(section_image, section_image_name, working_dir, dest_dir)
        for i in range(30):
            page = page_id
            preceding_zeroes = re.compile('^0*')
            page = int(re.sub(preceding_zeroes, '', page))
            boundaries = self.record_boundaries(i, page_number=page)
            record_image = self.crop_image(page_image, boundaries)
            record_image_name = f'{constituency}_F{constituency_file_id}_P{page_id}_TRecord_{i}.png'
            self.save_image_as(record_image, record_image_name, working_dir, dest_dir)
            record_images.append(os.path.join(dest_dir, record_image_name))
        return record_images


if __name__ == "__main__":
    local_src_benaulim = r'test_data/whole_pdf/Benaulim/Part01.pdf'
    aws_src_benaulim = 's3://epicfiles/GER_2020/Benaulim/Part01.pdf'
    local_dest = r'.\pdf_processing_workspace_3'
    aws_dest = 's3://epicfiles/splits/'

    record_processor = PDFSlicingMachine()

    ###################### split into pages
    # local src and local dest
    record_processor.split_whole_pdf_into_pages(local_src_benaulim, local_dest)
    # aws src and aws dest
    # record_processor.split_whole_pdf_into_pages(aws_src_benaulim, aws_dest)


    #################### split page in records
    #local_header_page = 'pdf_processing_workspace_3/pdf_pages_as_images/Benaulim/01/01/Benaulim_F01_P01.png'
    #record_processor.split_pdf_page_image_into_record_images(local_header_page, local_dest)
    #local_record_page = 'pdf_processing_workspace_3/pdf_pages_as_images/Benaulim/01/07/Benaulim_F01_P07.png'
    #local_record_page = 'pdf_processing_workspace_3/pdf_pages_as_images/Benaulim/01/03/Benaulim_F01_P03.png'
    #local_record_page = 'pdf_processing_workspace_3/pdf_pages_as_images/Benaulim/01/007/Benaulim_F01_P007.png'
    #record_processor.split_pdf_page_image_into_record_images(local_record_page, local_dest)
