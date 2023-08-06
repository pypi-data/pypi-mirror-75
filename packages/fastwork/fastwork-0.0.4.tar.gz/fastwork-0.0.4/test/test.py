from fastwork import MergeExcel

if __name__ == "__main__":
    excel_filepath = "豆瓣书籍分类列表.xlsx"
    merge_excel = MergeExcel(excel_filepath, keep_sheetname_lst=None)
    merge_excel.merge_worksheet()

