import os
import shutil

from functions import generate_page


def copy_tree(src_folder_path, dest_folder_path):
    # List all files in the src directory
    working_dir = os.getcwd()

    src_files = os.listdir(src_folder_path)

    for filename in src_files:
        item_path = os.path.join(src_folder_path, filename)
        dest_item_path = os.path.join(dest_folder_path, filename)
        if os.path.isdir(item_path):
            copy_tree(item_path, dest_item_path)
        else:
            shutil.copy(item_path, dest_item_path)


def generate_pages(src_content_path, dest_html_path, template_path):
    files_md = os.listdir(src_content_path)
    for filename in files_md:
        src_md_path = os.path.join(src_content_path, filename)
        dest_html_path = os.path.join(
            dest_html_path, "\n".join(filename.split(".")[:-1]) + ".html"
        )
        if os.path.isdir(src_md_path):
            generate_pages(src_md_path)
        else:
            generate_page(src_md_path, template_path, dest_html_path)


def main():
    working_directory = os.getcwd()
    print("Working directory: ", working_directory)

    if not os.path.exists(os.path.join(working_directory, "public")):
        os.mkdir("public")

    try:
        # Delete all files in the public directory
        for filename in os.listdir(os.path.join(working_directory, "public")):
            file_path = os.path.join(working_directory, "public", filename)
            print(f"Removing file: {filename} in the public directory")
            os.remove(file_path)
    except FileNotFoundError:
        print(f"Error: The directory public does not exist.")
    except PermissionError:
        print(f"Error: You do not have permission to read or write to the file.")
    except Exception as e:
        print(f"Error: {e}")

    print("Attempting tree copy from static to public")
    src_path = os.path.join(working_directory, "static")
    public_path = os.path.join(working_directory, "public")

    copy_tree(src_path, public_path)
    print("Files copied successfully.")

    content_path = os.path.join(working_directory, "content")
    generate_pages(
        content_path, public_path, os.path.join(working_directory, "template.html")
    )


main()
