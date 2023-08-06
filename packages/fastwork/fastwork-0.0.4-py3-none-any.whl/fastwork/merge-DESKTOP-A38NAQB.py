import os
import pandas as pd


class MergeExcel(object):
    def __init__(self, excel_filepath, keep_sheetname_lst=None):
        """
        : df_dict: df组成的字典，key为sheetname
        : keep_sheetname_lst: 需要合并的sheetname列为，默认为空，即不指定则合并所有
        """
        self.excel_filepath = excel_filepath
        self.keep_sheetname_lst = keep_sheetname_lst
        new_filename = "%s_处理完成.xlsx" % os.path.basename(excel_filepath)
        abs_filepath = os.path.abspath(excel_filepath)
        self.new_filepath = os.path.join(os.path.dirname(abs_filepath), new_filename)

    def read_excel(self, excel_filepath, sheet_name=None):
        """
        读取excel等本地文件数据路径，返回Pandas.DataFrame结构化数据
        :param excel_filepath:文件路径
        :sheet_name: 设置读取的工作表范围，默认为None，即读取所有的sheet
        :return:Pandas.DataFrame 字典对象，key：sheet_name,values:pandas.df

        """

        try:
            df_dict = pd.read_excel(excel_filepath, sheet_name=sheet_name)
            return df_dict
        except Exception as err:
            print(err)

    @classmethod
    def df_concat(self, df_sheet_dict):
        # try:
        df = pd.concat(df_sheet_dict)
        print(df.index.values)
        df.index = [x[0] for x in df.index]
        print(df.index)
        df.columns = [x for x in df.columns]
        df.index.name = '工作表名称'
        return df

    def merge_worksheet(self):
        if type(self.keep_sheetname_lst) in [str, list] or self.keep_sheetname_lst is None:
            df_dict = self.read_excel(excel_filepath=self.excel_filepath,
                                      sheet_name=self.keep_sheetname_lst)
            print("【注意】当前共有%s个工作表需要合并!" % len(df_dict))
            for sheet_name, df in df_dict.items():
                print("工作表名称【%s】: 共%s行" % (sheet_name, df.shape[0]))
            df_merge = pd.concat(df_dict)
            df_merge.index = [x[0] for x in df_merge.index]
            df_merge.index.name = '工作表名称'

        else:
            print("当前指定的参数有误！，请检查后重新输入！")
            df_merge = None

        if df_merge is not None:
            return df_merge
        else:
            return None

    def to_excel(self, df, sheet_name="sheet1"):

        writer = pd.ExcelWriter('%s' % self.new_filepath, engine='xlsxwriter')
        df.to_excel(writer, sheet_name=sheet_name,
                    startrow=0,
                    index=False)
        workbook = writer.book
        # 统计部分内容部分样式
        txt_cell_format = workbook.add_format({'bold': False, 'italic': False, 'font_size': 10, 'border': 1})
        txt_cell_format.set_align('left')
        worksheet = writer.sheets[sheet_name]
        # worksheet1.set_column(起始列,结束列，列宽，格式)
        worksheet.set_column(0, df.shape[1], 15, txt_cell_format)
        writer.save()

