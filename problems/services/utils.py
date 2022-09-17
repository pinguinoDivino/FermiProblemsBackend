import os
import base64
from django.core.files.storage import default_storage
from django.db.models import FileField, ImageField
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def file_cleanup(sender, **kwargs):
    """
    File cleanup callback used to emulate the old delete
    behavior using signals. Initially django deleted linked
    files when an object containing a File/ImageField was deleted.
    """
    for field_name, field in [[x.name, x] for x in sender._meta.get_fields()]:
        if field and (isinstance(field, FileField) or isinstance(field, ImageField)):
            inst = kwargs["instance"]
            f = getattr(inst, field_name)
            m = inst.__class__._default_manager
            if f.__bool__() and (hasattr(f, "path")
                                 and os.path.exists(f.path)
                                 and not m.filter(
                        **{"%s__exact" % field_name: getattr(inst, field_name)}
                    ).exclude(pk=inst._get_pk_val())
            ):
                try:
                    default_storage.delete(f.path)
                except:
                    pass


def recursive_glob(treeroot, pattern):
    results = []
    for base, dirs, files in os.walk(treeroot):
        good_files = [filename for filename in files if pattern in filename]
        results.extend([os.path.join(base, f), f] for f in good_files)
    return results


def create_problem_user_answer_distribution(data, image_path):
    plt.hist(data, bins=60)
    plt.xlabel('Answers')
    plt.ylabel('Count')
    plt.savefig(image_path, format="png")
    plt.close()


def get_problem_distribution_graph_base64(image_path):
    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
    return img_base64
