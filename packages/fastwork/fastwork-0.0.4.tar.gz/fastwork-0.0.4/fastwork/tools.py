'''
@File    :   tools.py
@Contact :   951683309@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/5/14 17:26   GongliXu     1.0
'''
import os
import pandas as pd
from sqlalchemy import create_engine
import configparser


def to_excel(df, filepath, sheet_name="sheet1"):
    new_filename = "%s_处理完成.xlsx" % os.path.basename(filepath)
    abs_filepath = os.path.abspath(filepath)
    new_filepath = os.path.join(os.path.dirname(abs_filepath), new_filename)
    writer = pd.ExcelWriter('%s' % new_filepath, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name,
                startrow=0,
                index=False)
    workbook = writer.book
    # 统计部分内容部分样式
    txt_cell_format = workbook.add_format({'bold': False, 'italic': False, 'font_size': 10, 'border': 1})
    txt_cell_format.set_align('left')
    worksheet = writer.sheets['合并']
    # worksheet1.set_column(起始列,结束列，列宽，格式)
    worksheet.set_column(0, df.shape[1], 15, txt_cell_format)
    writer.save()


def mysql_engine(**kwargs):
    engine = create_engine("mysql+pymysql://%s:%s@%s/%s?charset=%s"
                           % (kwargs['user'],
                              kwargs['password'],
                              kwargs['host'],
                              kwargs['database'],
                              kwargs['charset']))
    return engine


def mssql_engine(**kwargs):
    engine = create_engine("mssql+pymssql://%s:%s@%s/%s?charset=%s"
                           % (kwargs['user'],
                              kwargs['password'],
                              kwargs['server'],
                              kwargs['database'],
                              kwargs['charset']
                              ), encoding='UTF-8')
    return engine


def read_cfg(filepath):
    db_cfg = configparser.ConfigParser()
    db_cfg.read('%s' % filepath, encoding='utf8')
    return db_cfg


def read_excel(excel_filepath, sheet_name=None):
    """
    读取excel等本地文件数据路径，返回Pandas.DataFrame结构化数据
    :param excel_filepath:文件路径
    :sheet_name: 设置读取的工作表范围，默认为None，即读取所有的sheet
    :return:Pandas.DataFrame 字典对象，key：sheet_name,values:pandas.df

    """

    df_dict = pd.read_excel(excel_filepath, sheet_name=sheet_name)
    return df_dict


def read_excel_files(folder_path=None, read_all_sheets=False, end_str_lst=['.xlsx', '.xls']):
    '''
    :param folder_path: 文件夹路径
    :param end_str_lst: 指定读取的文件扩展名列表
    :return: pd.DataFrame
    '''
    end_str_tuble = tuple(end_str_lst)
    # 判断是否为绝对路径，如果不是，则转换为绝对路径
    if not os.path.isabs(folder_path):
        folder_path = os.path.abspath(folder_path)
    df_all_lst = []
    for root, dirs, files in os.walk(folder_path, topdown=True):
        '''
        root：当前正在遍历的这个文件夹
        dirs ：list ，root目录中所有的文件夹的名字(不包括文件夹中的子目录)
        files：list , root目录中所有的文件名称(不包括子目录)
        '''
        excel_files = [file for file in files if file.endswith(end_str_tuble) and not file.startswith(("~$"))]
        print(root)
        print(dirs)
        print(files)
        print(excel_files)
        # 如果excel_files列表不为空
        if excel_files:
            for excel_file in excel_files:
                df_dict = pd.read_excel(os.path.join(root, excel_file), sheet_name=None)
                if read_all_sheets is False:
                    df_dict = {k: df_dict[k] for k in list(df_dict.keys())}

                df_merge = pd.concat(df_dict)
                df_merge.index = [x[0] for x in df_merge.index]
                df_merge.index.name = '工作表名称'
                col_name = list(df_merge.columns)
                df_merge['excel文件名称'] = excel_file
                df_merge['工作表名称'] = df_merge.index
                df_merge = pd.DataFrame(df_merge, columns=['excel文件名称', '工作表名称'] + col_name)
                df_all_lst.append(df_merge)
        df_all = pd.concat(df_all_lst)
        return pd.concat(df_all)


if __name__ == "__main__":
    folder_path = r"C:\Users\soari\Desktop\excel"
    df_all = read_excel_files(folder_path, read_all_sheets=False)
    # excel_files = r"C:\Users\soari\Desktop\excel\豆瓣书籍分类列表1.xlsx"
    # df_dict = read_excel(excel_files, sheet_name=None)
    print(df_all)
    print(type(df_all))
    df_all.to_excel("df_all_test.xlsx", index=False)
    # for k, v in df_dict.items():
    #     print(k)
    #     print(v)
