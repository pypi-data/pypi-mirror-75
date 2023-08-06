""""""


class FileCategory:
    def __init__(self, entries=None) -> None:
        if entries is None:
            entries = {}
        self.entries = entries


class SubjectFile:

    def __init__(self, subject: str, **file_groups) -> None:
        """Holds the file information of a subject.

        Args:
            subject (str): The subject identifier.
            **file_groups (dict): The groups of file types containing the file path entries.
        """
        self.subject = subject
        self.categories = {}
        for category_name, category_files in file_groups.items():
            self.categories[category_name] = FileCategory(category_files)
        self._check_validity()

    def _check_validity(self):
        all_file_ids = []
        for file_category in self.categories.values():
            all_file_ids.extend(file_category.entries.keys())

        if len(all_file_ids) > len(set(all_file_ids)):
            raise ValueError('Identifiers must be unique')

    def get_all_files(self):
        """
        Returns:
            dict: All file path entries of a subject `flattened` (without groups/category).

        """
        all_files = {}
        for file_category in self.categories.values():
            for id_, filename in file_category.entries.items():
                all_files[id_] = filename
        return all_files
