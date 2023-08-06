import os.path
from ier_processor.utils import *
import re
from PIL import Image
import pytesseract

class ExtractionResult:

    def __init__(self):
        self.error = False
        self.success = False
        self.error_count = 0
        self.success_count = 0


class ExtractionSuccess(ExtractionResult):

    def __init__(self, extracted_data):
        self.extracted_data = extracted_data
        self.success = True


    @property
    def data(self):
        return self.extracted_data


class ExtractionFailure(ExtractionResult):

    def __init__(self, original_data, error_message):
        self.original_data = original_data
        self.error_message = error_message
        self.success = False

    @property
    def data(self):
        return "E:" + self.error_message


class RegexExtractor:

    def __init__(self, r_exp, regex_group_to_extract=1, extracting_field_name=None):
        self.r_exp = r_exp
        self.compiled_regex = re.compile(self.r_exp)
        self.regex_group_to_extract = regex_group_to_extract
        self.extracting_field_name = extracting_field_name

    def apply_to(self, data):
        matching = self.compiled_regex.search(data)
        if matching:
            return ExtractionSuccess(matching.group(self.regex_group_to_extract))
        else:
            return ExtractionFailure(data, f"Could not extract [{self.extracting_field_name}] from [{data}] using [{self.r_exp}]")


class HeaderPage(ExtractionSuccess):

    def __init__(self, **kwargs):
        self.main_town_or_village = kwargs.get('main_town_or_village', ExtractionFailure("", "Could not extract main_town_or_village"))
        self.post_office = kwargs.get('post_office', ExtractionFailure("", "Could not extract post_office"))
        self.village_council = kwargs.get('village_council', ExtractionFailure("", "Could not extract village_council"))
        self.block = kwargs.get('block', ExtractionFailure("", "Could not extract block"))
        self.police_station = kwargs.get('police_station', ExtractionFailure("", "Could not extract police_station"))
        self.sub_division = kwargs.get('sub_division', ExtractionFailure("", "Could not extract sub_division"))
        self.district = kwargs.get('district', ExtractionFailure("", "Could not extract district"))
        self.pin_code = kwargs.get('pin_code', ExtractionFailure("", "Could not extract pin_code"))
        self.components = [
            self.main_town_or_village,
            self.post_office,
            self.village_council,
            self.block,
            self.police_station,
            self.sub_division,
            self.district,
            self.pin_code,
        ]

        success = [x.success for x in self.components]
        self.success_count = len(success)
        self.success = all(success)
        errors = [x.error_message for x in self.components if not x.success]
        self.errors = errors
        self.error_count = len(self.errors)

    @property
    def data(self):
        return_data = [str(self.error_count), str(self.success_count)]
        for field in self.components:
            if field.success:
                return_data.append(field.extracted_data)
            else:
                return_data.append(field.error_message)
        return "\t".join(return_data)


class VoterRecord(ExtractionSuccess):

    def __init__(self, **kwargs):

        self.name = kwargs.get('name', ExtractionFailure("", "Could not extract name"))
        self.father = kwargs.get('father', ExtractionFailure("", "Could not extract fathers name"))
        self.husband = kwargs.get('husband', ExtractionFailure("", "Could not extract husbands name"))
        self.house_number = kwargs.get('house_number', ExtractionFailure("", "Could not extract house_number"))
        self.epic = kwargs.get('epic', ExtractionFailure("", "Could not extract epic"))
        self.age = kwargs.get('age', ExtractionFailure("", "Could not extract age"))
        self.gender = kwargs.get('gender', ExtractionFailure("", "Could not extract gender"))

        father = self.father
        husband = self.husband
        if father.success or husband.success:
            if not father.success:
                self.father = ExtractionSuccess("")
            elif not husband.success:
                self.husband = ExtractionSuccess("")

        self.components = [
            self.name,
            self.father,
            self.husband,
            self.house_number,
            self.epic,
            self.age,
            self.gender,]
        success = [x.success for x in self.components]
        self.success_count = len(success)
        errors = [x.error_message for x in self.components if not x.success]
        self.errors = errors
        self.error_count = len(self.errors)


    @property
    def data(self):
        return_data = [str(self.error_count), str(self.success_count)]
        for field in self.components:
            if field.success:
                return_data.append(field.extracted_data)
            else:
                return_data.append(field.error_message)
        return "\t".join(return_data)

class ImageData:

    def __init__(self, file):
        self.file = file
        self.constituency = None
        self.file_no = None
        self.page_no = None
        self.type = None
        self.record_no = None
        self.valid = False
        file_type_regex = re.compile(r'(\w+)_F(\d+)_P(\d+)_T(\w+)_(\d+).png$')
        matching = file_type_regex.search(file)
        if matching:
            self.valid = True
            self.constituency = matching.group(1)
            self.file_no = matching.group(2)
            self.page_no = matching.group(3)
            self.type = matching.group(4)
            self.record_no = matching.group(5)

    @property
    def data(self):
        image_valid = 'ImageTypeValid' if self.valid else 'ImageTypeInvalid'
        components = [image_valid,
                      str(self.type),
                      str(self.constituency),
                      str(self.file_no),
                      str(self.page_no),
                      str(self.record_no) ]
        return "\t".join(components)

    def is_header(self):
        return self.valid and self.type == 'PDFHeader'

    def is_assembly(self):
        return self.valid and self.type == 'Assembly'

    def is_section(self):
        return self.valid and self.type == 'Section'

    def is_record(self):
        return self.valid and self.type == 'Record'


class ImageProcessor:

    def __init__(self, debug=False):
        from datetime import datetime
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        prefix = f'z_image_processing_{ts}'
        self.debug = debug
        self.working_dir = create_working_directory(debug=self.debug, prefix= prefix)


    def _open_image_in_working_dir(self, image_path):
        file_location = os.path.join(self.working_dir, os.path.basename(image_path))
        copy_across_file_systems(image_path, file_location)
        return Image.open(file_location)


    def extract_image_text(self, image):
        custom_oem_psm_config = r'--oem 3 --psm 6'
        return pytesseract.image_to_string(image, config=custom_oem_psm_config)

    def extract_polling_area_text(self, file):
        polling_area_image = self._open_image_in_working_dir(file)
        polling_area_text = self.extract_image_text(polling_area_image)
        lines = polling_area_text.split("\n")
        lines = [x.strip() for x in lines if x.strip() != '']
        return lines

    def process_pdf_header_image(self, image_data):
        lines = self.extract_polling_area_text(image_data.file)
        if len(lines) < 8:
            lines.append([""] * 8 - len(lines))

        main_town_or_village, post_office, village_council, block, police_station, sub_division, district, pin_code = lines

        not_alphabets = '[^A-Z^a-z]'
        r_main_town_or_village = RegexExtractor(re.compile(f"Main Town or Village{not_alphabets}+(.*)"), extracting_field_name='main_town_or_village')
        r_post_office = RegexExtractor(re.compile(f"Post Office{not_alphabets}+(.*)"), extracting_field_name='post_office')
        r_village_council = RegexExtractor(re.compile(f"Village Council{not_alphabets}+(.*)"), extracting_field_name='village_council')
        r_block = RegexExtractor(re.compile(f"Block{not_alphabets}+(.*)"), extracting_field_name='block')
        r_police_station = RegexExtractor(re.compile(f"Police Station{not_alphabets}+(.*)"), extracting_field_name='police_station')
        r_sub_division = RegexExtractor(re.compile(f"Sub Division{not_alphabets}+(.*)"), extracting_field_name='sub_division')
        r_district = RegexExtractor(re.compile(f"District{not_alphabets}+(.*)"), extracting_field_name='district')
        r_pin_code = RegexExtractor(re.compile(f"Pin Code.*?([0-9]+)$"), extracting_field_name='pin_code')

        main_town_or_village = r_main_town_or_village.apply_to(main_town_or_village)
        post_office = r_post_office.apply_to(post_office)
        village_council = r_village_council.apply_to(village_council)
        block = r_block.apply_to(block)
        police_station = r_police_station.apply_to(police_station)
        sub_division = r_sub_division.apply_to(sub_division)
        district = r_district.apply_to(district)
        pin_code = r_pin_code.apply_to(pin_code)

        header_page = HeaderPage(main_town_or_village=main_town_or_village,
                                 post_office=post_office,
                                 village_council=village_council,
                                 block=block,
                                 police_station=police_station,
                                 sub_division=sub_division,
                                 district=district,
                                 pin_code=pin_code)
        return header_page

    def extract_epic_from_voter_box_image(self, voter_box_image):
        width, height = voter_box_image.size
        epic_box = 200, 2, width - 4, height + 24
        epic_box_image = voter_box_image.crop(epic_box)
        epic_text = self.extract_image_text(epic_box_image).strip()
        epic = epic_text
        epic = epic.replace("$", "S")
        epic = epic.replace("§", "S")
        epic = re.sub('[^A-Z0-9]', '', epic)
        return ExtractionSuccess(epic)


    def extract_voter_text(self, voter_box_image):
        voter_data = self.extract_image_text(voter_box_image)
        voter_lines = [v.replace("Photo is", "").replace("Available", "") for v in voter_data.split("\n")]
        voter_lines = [v for v in voter_lines if v.strip()]
        return voter_lines

    def process_voter_image(self, image_data):
        name_regex = RegexExtractor(re.compile(r'Name[^A-Z^a-z)]*(.*)'), regex_group_to_extract=1, extracting_field_name='name')
        house_number_regex = RegexExtractor(re.compile(r'House Number[^A-Z^a-z^0-9]*(.*)'), extracting_field_name='house_number')
        age_regex = RegexExtractor(re.compile(r"Age: (\d+)"), extracting_field_name='age')
        gender_regex = RegexExtractor(re.compile(r"Gender: (MALE|FEMALE)"), extracting_field_name='gender')


        voter_box_image = self._open_image_in_working_dir(image_data.file)
        epic = self.extract_epic_from_voter_box_image(voter_box_image)
        voter_lines = self.extract_voter_text(voter_box_image)
        collected_fields = {}
        for line in voter_lines:
            if "Father" in line:
                collected_fields['father'] = name_regex.apply_to(line)
            elif "Husband" in line:
                collected_fields['husband'] = name_regex.apply_to(line)
            elif "Name" in line:
                collected_fields['name'] = name_regex.apply_to(line)
            elif "House Number" in line:
                collected_fields['house_number'] = house_number_regex.apply_to(line)
            elif "Age" in line or "Gender" in line:
                collected_fields['age'] = age_regex.apply_to(line)
                collected_fields['gender'] = gender_regex.apply_to(line)

        collected_fields['epic'] = epic
        voter_record = VoterRecord(**collected_fields)
        return voter_record


    def process_assembly_image(self, image_data):
        assembly_extractor = RegexExtractor(re.compile("Assembly Constituency No and Name : (\\d+-)?(.*)"), 2, extracting_field_name='assembly')
        assembly_image = self._open_image_in_working_dir(image_data.file)
        assembly_image_text = self.extract_image_text(assembly_image)
        return assembly_extractor.apply_to(assembly_image_text)

    def process_section_header(self, image_data):
        section_extractor = RegexExtractor(re.compile("Section No and Name : (\\d+-)?(.*)"), 2, extracting_field_name='section')
        section_image = self._open_image_in_working_dir(image_data.file)
        section_image_text = self.extract_image_text(section_image)
        return section_extractor.apply_to(section_image_text)

    def process_image(self, file):
        image_data = ImageData(file)
        result = None
        if image_data.is_header():
            result = self.process_pdf_header_image(image_data)
        elif image_data.is_assembly():
            result = self.process_assembly_image(image_data)
        elif image_data.is_section():
            result = self.process_section_header(image_data)
        elif image_data.is_record():
            result = self.process_voter_image(image_data)
        else:
            raise Exception(f'Unknown File type {file}')
        return image_data.type, "\t".join([image_data.data, result.data, image_data.file])


if __name__ == '__main__':
    if os.name == 'nt':
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pdf_header_image = r"pdf_processing_workspace_3/pdf_pages_as_images/Benaulim/01/01/Benaulim_F01_P01_TPDFHeader_0.png"
    assembly_image = r"pdf_processing_workspace_3/pdf_pages_as_images/Benaulim/01/03/Benaulim_F01_P03_TAssembly_0.png"
    section_image = r"pdf_processing_workspace_3/pdf_pages_as_images/Benaulim/01/03/Benaulim_F01_P03_TSection_0.png"
    voter_image = r"pdf_processing_workspace_3/pdf_pages_as_images/Benaulim/01/03/Benaulim_F01_P03_TRecord_0.png"
    image_processor = ImageProcessor()
    result = image_processor.process_image(pdf_header_image)
    print(f'header_data is [{result.data}]')
    result = image_processor.process_image(assembly_image)
    print(f'assembly_data is [{result.data}]')
    result = image_processor.process_image(section_image)
    print(f'section_data is [{result.data}]')
    result = image_processor.process_image(voter_image)
    print(f'voter_data is [{result.data}]')

