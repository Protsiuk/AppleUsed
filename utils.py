import os
import uuid


def get_file_path(instance, filename):
    """
    Upload image
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(instance.__class__.__name__.lower(), filename)


# Created paginations list
def gen_page_list(page_current, page_count):

    my_page = []
    if page_count > 10:
        if page_current <=4:
            for key in range(1, 5):
                my_page.append(key)
            my_page.append("...")
            my_page.append(page_count)
        elif page_current >= (page_count-4):
            my_page.append(1)
            my_page.append("...")
            for key in range((page_count-5), (page_count+1)):
                my_page.append(key)
        else:
            my_page.append(1)
            my_page.append("...")
            for key in range((page_current-2), (page_current+2)):
                my_page.append(key)
            my_page.append("...")
            my_page.append(page_count)
    else:
        for key in range(0, page_count):
            my_page.append(key+1)
    return my_page
