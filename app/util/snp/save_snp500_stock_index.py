import pandas as pd
import urllib.request
import ssl, zipfile, os
from pandas import DataFrame

curr_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = [curr_dir,'datafiles']
base_dir = os.path.join(*save_dir)

def save_snp500_stock_index(base_dir : str = base_dir) -> DataFrame:
    """
    해외 주식 기초정보를 파일로 다운 받고 DF 로 반환 및 xlsx 파일로 저장
    Args:
        base_dir (str, optional): app/util/snp/datafiles

    Returns:
        DataFrame: 
            - column = 구분코드,심볼,영문명,한글명,종목업종코드,다우30 편입종목여부,나스닥100 편입종목여부, S&P 500 편입종목여부,거래소코드,국가구분코드
    """

    # download file
    print('Downloading Foreign')
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve("https://new.real.download.dws.co.kr/common/master/frgn_code.mst.zip",
                                os.path.join(base_dir,"frgn_code.mst.zip"))
    os.chdir(base_dir)
    frgn_code_zip = zipfile.ZipFile('frgn_code.mst.zip')
    frgn_code_zip.extractall()
    frgn_code_zip.close()

    # df1 : '구분코드','심볼','영문명','한글명'
    file_name = os.path.join(base_dir,"frgn_code.mst")
    tmp_fil1 = os.path.join(base_dir,"frgn_code_part1.tmp")
    tmp_fil2 = os.path.join(base_dir,"frgn_code_part2.tmp")

    wf1 = open(tmp_fil1, mode="w")
    wf2 = open(tmp_fil2, mode="w")

    with open(file_name, mode="r", encoding="cp949") as f:
        for row in f:
            if row[0:1] == 'X':
                rf1 = row[0:len(row) - 14]
                rf1_1 = rf1[0:1]
                rf1_2 = rf1[1:11]
                rf1_3 = rf1[11:40].replace(",","")
                rf1_4 = rf1[40:80].replace(",","").strip()
                wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + ',' + rf1_4 + '\n')
                rf2 = row[-15:]
                wf2.write(rf2+'\n')
                continue
            rf1 = row[0:len(row) - 14]
            rf1_1 = rf1[0:1]
            rf1_2 = rf1[1:11]
            rf1_3 = rf1[11:50].replace(",","")
            rf1_4 = row[50:75].replace(",","").strip()
            wf1.write(rf1_1 + ',' + rf1_2 + ',' + rf1_3 + ',' + rf1_4 + '\n')
            rf2 = row[-15:]
            wf2.write(rf2+'\n')

    wf1.close()
    wf2.close()
    
    part1_columns = ['구분코드','심볼','영문명','한글명']
    df1 = pd.read_csv(tmp_fil1, header=None, names=part1_columns)

    # df2 : '종목업종코드','다우30 편입종목여부','나스닥100 편입종목여부', 'S&P 500 편입종목여부','거래소코드','국가구분코드'
    
    field_specs = [4, 1, 1, 1, 4, 3]
    part2_columns = ['종목업종코드','다우30 편입종목여부','나스닥100 편입종목여부',
                    'S&P 500 편입종목여부','거래소코드','국가구분코드']
    df2 = pd.read_fwf(tmp_fil2, widths=field_specs, names=part2_columns, encoding='cp949')
    
    df2['종목업종코드'] = df2['종목업종코드'].str.replace(pat=r'[^A-Z]', repl= r'', regex=True) # 종목업종코드는 잘못 기입되어 있을 수 있으니 참고할 때 반드시 mst 파일과 비교 참고
    df2['다우30 편입종목여부'] = df2['다우30 편입종목여부'].str.replace(pat=r'[^0-1]+', repl= r'', regex=True) # 한글명 길이가 길어서 생긴 오타들 제거
    df2['나스닥100 편입종목여부'] = df2['나스닥100 편입종목여부'].str.replace(pat=r'[^0-1]+', repl= r'', regex=True)
    df2['S&P 500 편입종목여부'] = df2['S&P 500 편입종목여부'].str.replace(pat=r'[^0-1]+', repl= r'', regex=True)

    DF = pd.concat([df1,df2],axis=1) # 데이터 프레임 병합
    DF = DF[DF['S&P 500 편입종목여부'] == '1']    # 필터링 S&P 500 
    DF.to_excel('frgn_code.xlsx',index=False)   # datafiles 에 엑셀파일로 저장
    # clean temporary file and dataframe
    del (df1)
    del (df2)
    os.remove(tmp_fil1)
    os.remove(tmp_fil2)
    print("Download Done")
    return DF
if __name__ == '__main__':
    save_snp500_stock_index()