import openpyxl

from typing import Tuple, Optional


class Excel(object):
    def __init__(self, file: str):
        self._file = file
        self._wb = openpyxl.load_workbook(filename=self._file)

    def find(self, user_id: int) -> Optional[Tuple[str, str, str, bool]]:
        sheet = next(iter(self._wb))

        for row in sheet.rows:
            if row[0].value == user_id:
                name = row[1].value
                info = row[2].value
                comment = row[3].value
                registered_cell = row[4]
                if registered_cell.value != '*':
                    sheet.cell(row=registered_cell.row, column=registered_cell.column).value = '*'
                    self._wb.save(self._file)

                    return name, info, comment, False
                else:
                    return name, info, comment, True

        return None
