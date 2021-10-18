from crawling import channel_name,query_list, createQueryListCsv, parse_html
from create import API_KEY, createResultFile

if __name__ == '__main__':

    createQueryListCsv(query_list,channel_name)
    createResultFile(API_KEY,channel_name)
    # file_list = createFileList()
