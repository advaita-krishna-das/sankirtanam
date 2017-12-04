from app.parser import parse


def validate(html):
    result = []

    table = parse(html)

    if table:
        for ridx, row in enumerate(table):
            columns_cnt = len(row)

            if columns_cnt not in [5, 36]:
                __error(result, "Row should contain 5 or 36 column", row=ridx, column=0)

            if not row[0]:
                __error(result, "Name is not provided", row=ridx, column=0)
            for i in range(1, columns_cnt):
                if not isinstance(row[i], int):
                    __error(result, "Not a numeric value {}".format(row[i]), row=ridx, column=i)
    else:
        __error(result, "Report should contain one table")

    return {
        "isValid": len(result) == 0,
        "errors": result
    }


def __error(result, message, row=None, column=None):
    result.append({"msg": message, "row": row, "column": column})


