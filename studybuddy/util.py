def get_user_agents():
    return [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
    ]

def file_name_from_url(url):
    url_length = len(url)

    file_name_slug_start_idx = url.find("problems/")
    if file_name_slug_start_idx == -1:
        return None

    file_name_slug_start_idx += 9  # len("problems/") = 9

    file_name_slug_end_idx = file_name_slug_start_idx
    while file_name_slug_end_idx < url_length:
        if url[file_name_slug_end_idx] == '/':
            break
        file_name_slug_end_idx += 1

    if file_name_slug_start_idx == file_name_slug_end_idx:
        return None

    file_name_slug = url[file_name_slug_start_idx:file_name_slug_end_idx]
    # Convert slugs native snake-case to CapCase
    file_name = "".join([x.capitalize() for x in file_name_slug.split("-")])
    return file_name


def parse_file_to_list(file_path):
    try:
        with open(file_path, 'r') as file:
            # Read lines and remove trailing newlines
            lines = [line.rstrip('\n') for line in file]
        return lines
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} was not found")
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")