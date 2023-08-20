import fitz  # PyMuPDF
import os
import OcrToTableTool as ottt
import TableExtractor as te
import TableLinesRemover as tlr
import cv2


#  extract images from pdf and save them in output_images 
def extract_images_from_pdf(pdf_path, output_folder, target_dpi=200):
    pdf_document = fitz.open(pdf_path)

    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        pix = page.get_pixmap(matrix=fitz.Matrix(target_dpi/72, target_dpi/72))

        image_bytes = pix.samples
        image_format = "png"  # Save images in PNG format

        image_filename = f"page_{page_number + 1}.{image_format}"
        image_path = os.path.join(output_folder, image_filename)

        with open(image_path, "wb") as image_file:
            image_file.write(image_bytes)

        # print to test 
        print(f"Extracted image {image_filename} from page {page_number + 1}")

    pdf_document.close()

if __name__ == "__main__":
    pdf_file_path = "/Users/raoom/ocr-extract-table-from-image-python/pdf/imagesExamplePDF.pdf" # the pdf with images 
    output_folder_path = "output_images"
    
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    extract_images_from_pdf(pdf_file_path, output_folder_path)


# Processing loop for each image from output_images
output_images_folder = "output_images"
image_files = [f for f in os.listdir(output_images_folder) if f.endswith(".png")]

for image_file in image_files:
    image_path = os.path.join(output_images_folder, image_file)
    
    # Perform the processing steps for each image
    table_extractor = te.TableExtractor(image_path)
    perspective_corrected_image = table_extractor.execute()
    cv2.imshow("perspective_corrected_image", perspective_corrected_image)


    lines_remover = tlr.TableLinesRemover(perspective_corrected_image)
    image_without_lines = lines_remover.execute()
    cv2.imshow("image_without_lines", image_without_lines)

    ocr_tool = ottt.OcrToTableTool(image_without_lines, perspective_corrected_image)
    ocr_tool.execute()

    cv2.waitKey(0)
    cv2.destroyAllWindows()

